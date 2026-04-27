#!/usr/bin/env python3
"""Generate API overview pages from OmicVerse @register_function entries.

This script scans the sibling ``omicverse-core`` checkout with AST so the
documentation index stays aligned with the function registry without depending
on heavyweight imports during generation. When ``--validate-public`` is used,
the script also tries to resolve each generated path against ``import omicverse
as ov`` in the current interpreter and filters out unresolved symbols.
"""

from __future__ import annotations

import argparse
import ast
import importlib
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = (REPO_ROOT.parent / "omicverse-core" / "omicverse").resolve()

DOC_TARGETS = {
    "en": REPO_ROOT / "docs" / "api" / "user.md",
    "zh": REPO_ROOT / "docs_zh" / "api" / "user.md",
}

SECTION_ORDER = [
    "top",
    "settings",
    "io",
    "alignment",
    "pp",
    "single",
    "bulk",
    "metabol",
    "micro",
    "space",
    "bulk2single",
    "pl",
    "datasets",
    "external",
    "utils",
]

SECTION_META = {
    "en": {
        "title": "User API",
        "import_label": "Import OmicVerse as:",
        "generated_note": (
            "This page is auto-generated from `@register_function` entries in the "
            "OmicVerse registry."
        ),
        "all_registered": "Public registry entries listed here: {count}",
        "section_titles": {
            "top": "Top-Level API",
            "settings": "Settings",
            "io": "Data IO",
            "alignment": "Alignment",
            "pp": "Preprocessing (`pp`)",
            "single": "Single-cell (`single`)",
            "bulk": "Bulk RNA-seq (`bulk`)",
            "metabol": "Metabolomics (`metabol`)",
            "micro": "Microbiome (`micro`)",
            "space": "Spatial transcriptomics (`space`)",
            "bulk2single": "Bulk-to-Single (`bulk2single`)",
            "pl": "Plotting (`pl`)",
            "datasets": "Datasets",
            "external": "External Integrations (`external`)",
            "utils": "Utilities (`utils`)",
        },
    },
    "zh": {
        "title": "用户 API",
        "import_label": "导入 OmicVerse：",
        "generated_note": "本页根据 OmicVerse registry 中的 `@register_function` 自动生成。",
        "all_registered": "当前列出的公开 registry API 数量：{count}",
        "section_titles": {
            "top": "顶层 API",
            "settings": "设置",
            "io": "数据输入/输出",
            "alignment": "比对",
            "pp": "预处理 (`pp`)",
            "single": "单细胞 (`single`)",
            "bulk": "Bulk RNA-seq (`bulk`)",
            "metabol": "代谢组学 (`metabol`)",
            "micro": "微生物组 (`micro`)",
            "space": "空间转录组学 (`space`)",
            "bulk2single": "Bulk 转单细胞 (`bulk2single`)",
            "pl": "绘图 (`pl`)",
            "datasets": "数据集",
            "external": "外部集成 (`external`)",
            "utils": "工具函数 (`utils`)",
        },
    },
}

PUBLIC_PATH_OVERRIDES = {
    "omicverse.external.PyWGCNA.utils.readWGCNA": ["bulk.readWGCNA"],
    "omicverse.external.PyWGCNA.wgcna.pyWGCNA": ["bulk.pyWGCNA"],
    "omicverse.external.cnmf.cnmf.cNMF": ["single.cNMF"],
    "omicverse.io.single._rust.convert_adata_for_rust": ["utils.convert_adata_for_rust"],
    "omicverse.io.single._rust.convert_to_pandas": ["utils.convert_to_pandas"],
    "omicverse.io.single._rust.wrap_dataframe": ["utils.wrap_dataframe"],
    "omicverse.io.spatial._visium.read_visium": ["io.spatial.read_visium"],
}


@dataclass(frozen=True)
class RegistryEntry:
    full_name: str
    module_name: str
    short_name: str
    category: str
    description: str
    parent_classes: tuple[str, ...]
    source_file: Path

    @property
    def module_relative(self) -> str:
        prefix = "omicverse."
        if self.module_name.startswith(prefix):
            return self.module_name[len(prefix) :]
        return self.module_name

    def candidate_public_paths(self) -> list[str]:
        override = PUBLIC_PATH_OVERRIDES.get(self.full_name)
        if override is not None:
            return override

        rel = self.module_relative

        if rel == "utils.biocontext._tools":
            return [f"utils.biocontext.{self.short_name}"]

        if rel == "_settings":
            if self.parent_classes and self.parent_classes[0] == "omicverseConfig":
                return [f"settings.{self.short_name}", self.short_name]
            return [self.short_name]

        domain = rel.split(".", 1)[0]
        if domain:
            candidates = [f"{domain}.{self.short_name}"]
            if domain == "io" and self.short_name == "read":
                candidates.append("read")
            return candidates

        return [self.short_name]

    @property
    def absolute_import_path(self) -> str:
        if self.parent_classes:
            return ".".join((self.module_name, *self.parent_classes, self.short_name))
        return self.full_name

    @property
    def relative_import_path(self) -> str:
        prefix = "omicverse."
        absolute = self.absolute_import_path
        if absolute.startswith(prefix):
            return absolute[len(prefix) :]
        return absolute


def _is_register_function_decorator(node: ast.expr) -> bool:
    target = node.func if isinstance(node, ast.Call) else node
    if isinstance(target, ast.Name):
        return target.id == "register_function"
    if isinstance(target, ast.Attribute):
        return target.attr == "register_function"
    return False


def _find_register_decorator(node: ast.AST) -> ast.Call | None:
    decorators = getattr(node, "decorator_list", [])
    for decorator in decorators:
        if isinstance(decorator, ast.Call) and _is_register_function_decorator(decorator):
            return decorator
    return None


def _literal_string(node: ast.AST | None) -> str:
    if node is None:
        return ""
    try:
        value = ast.literal_eval(node)
    except Exception:
        return ""
    return value if isinstance(value, str) else ""


def _module_name_for_file(path: Path) -> str:
    relative = path.relative_to(PACKAGE_ROOT).with_suffix("")
    parts = ["omicverse", *relative.parts]
    return ".".join(parts)


def _scan_node(
    node: ast.AST,
    module_name: str,
    source_file: Path,
    parent_classes: tuple[str, ...],
    entries: list[RegistryEntry],
) -> None:
    if isinstance(node, ast.ClassDef):
        decorator = _find_register_decorator(node)
        if decorator is not None:
            entries.append(
                RegistryEntry(
                    full_name=f"{module_name}.{node.name}",
                    module_name=module_name,
                    short_name=node.name,
                    category=_literal_string(
                        next((kw.value for kw in decorator.keywords if kw.arg == "category"), None)
                    ),
                    description=_literal_string(
                        next((kw.value for kw in decorator.keywords if kw.arg == "description"), None)
                    ),
                    parent_classes=parent_classes,
                    source_file=source_file,
                )
            )
        for child in node.body:
            _scan_node(child, module_name, source_file, (*parent_classes, node.name), entries)
        return

    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        decorator = _find_register_decorator(node)
        if decorator is not None:
            entries.append(
                RegistryEntry(
                    full_name=f"{module_name}.{node.name}",
                    module_name=module_name,
                    short_name=node.name,
                    category=_literal_string(
                        next((kw.value for kw in decorator.keywords if kw.arg == "category"), None)
                    ),
                    description=_literal_string(
                        next((kw.value for kw in decorator.keywords if kw.arg == "description"), None)
                    ),
                    parent_classes=parent_classes,
                    source_file=source_file,
                )
            )
        for child in node.body:
            _scan_node(child, module_name, source_file, parent_classes, entries)


def scan_registry_entries() -> list[RegistryEntry]:
    entries: list[RegistryEntry] = []
    for path in sorted(PACKAGE_ROOT.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        if path.name == "__init__.py":
            continue
        source = path.read_text(encoding="utf-8")
        if "@register_function" not in source:
            continue
        tree = ast.parse(source, filename=str(path))
        module_name = _module_name_for_file(path)
        for node in tree.body:
            _scan_node(node, module_name, path, (), entries)
    return entries


def _resolve_public_symbol(path: str) -> bool:
    import omicverse as ov

    current = ov
    for part in path.split("."):
        current = getattr(current, part)
    return current is not None


def _resolve_absolute_symbol(path: str) -> bool:
    parts = path.split(".")
    for index in range(len(parts), 0, -1):
        module_name = ".".join(parts[:index])
        try:
            current = importlib.import_module(module_name)
        except Exception:
            continue

        try:
            for part in parts[index:]:
                current = getattr(current, part)
        except Exception:
            return False
        return current is not None
    return False


def choose_public_paths(
    entries: Iterable[RegistryEntry],
    *,
    validate_public: bool,
) -> tuple[dict[str, RegistryEntry], list[RegistryEntry]]:
    selected: dict[str, RegistryEntry] = {}
    unresolved: list[RegistryEntry] = []

    for entry in sorted(entries, key=lambda item: (item.module_name, item.short_name)):
        chosen_path = None
        for candidate in entry.candidate_public_paths():
            if validate_public:
                try:
                    if not _resolve_public_symbol(candidate):
                        continue
                except Exception:
                    continue
            chosen_path = candidate
            break

        if chosen_path is None and validate_public:
            absolute_candidate = entry.absolute_import_path
            if _resolve_absolute_symbol(absolute_candidate):
                chosen_path = entry.relative_import_path

        if chosen_path is None:
            unresolved.append(entry)
            continue

        selected.setdefault(chosen_path, entry)

    return selected, unresolved


def section_key_for_path(path: str) -> str:
    if path.startswith("omicverse."):
        relative = path[len("omicverse.") :]
        if relative.startswith("_settings."):
            return "settings"
        if "." not in relative:
            return "top"
        return relative.split(".", 1)[0]
    if "." not in path:
        return "top"
    prefix = path.split(".", 1)[0]
    if prefix == "settings":
        return "settings"
    return prefix


def render_autosummary(items: list[str]) -> str:
    lines = [
        "```{eval-rst}",
        ".. autosummary::",
        "   :toctree: reference/",
        "   :nosignatures:",
        "",
    ]
    lines.extend(f"   {item}" for item in items)
    lines.append("```")
    return "\n".join(lines)


def render_doc(locale: str, public_paths: list[str]) -> str:
    meta = SECTION_META[locale]
    grouped: dict[str, list[str]] = defaultdict(list)
    for path in public_paths:
        grouped[section_key_for_path(path)].append(path)

    lines = [
        f"# {meta['title']}",
        "",
        meta["import_label"],
        "",
        "```python",
        "import omicverse as ov",
        "```",
        "",
        meta["generated_note"],
        "",
        meta["all_registered"].format(count=len(public_paths)),
        "",
        "```{eval-rst}",
        ".. currentmodule:: omicverse",
        "```",
    ]

    for section in SECTION_ORDER:
        items = sorted(grouped.get(section, []), key=str.lower)
        if not items:
            continue
        lines.extend(
            [
                "",
                f"## {meta['section_titles'][section]}",
                "",
                render_autosummary(items),
            ]
        )

    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--validate-public",
        action="store_true",
        help="Import omicverse in the current interpreter and keep only resolvable public paths.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Do not write files; only print the planned counts and unresolved entries.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not PACKAGE_ROOT.is_dir():
        raise SystemExit(f"Could not find omicverse package at {PACKAGE_ROOT}")

    entries = scan_registry_entries()
    selected, unresolved = choose_public_paths(entries, validate_public=args.validate_public)
    public_paths = sorted(selected.keys(), key=str.lower)

    print(f"Scanned registry entries: {len(entries)}")
    print(f"Resolved public API entries: {len(public_paths)}")
    print(f"Unresolved entries: {len(unresolved)}")

    if unresolved:
        for entry in unresolved[:20]:
            print(f"  unresolved: {entry.full_name} -> {entry.candidate_public_paths()}")
        if len(unresolved) > 20:
            print(f"  ... and {len(unresolved) - 20} more")

    if args.check:
        return 0

    for locale, target in DOC_TARGETS.items():
        target.write_text(render_doc(locale, public_paths), encoding="utf-8")
        print(f"Wrote {target}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
