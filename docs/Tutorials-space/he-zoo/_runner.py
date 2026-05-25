"""In-process notebook runner (no kernel subprocess).

Avoids the nbclient/kernel subprocess pipeline by executing each code
cell directly in the current Python process and capturing stdout +
displayed figures into the notebook output cells. This makes the build
deterministic, fast (no fork/sleep), and easy to inspect from the
console.
"""
from __future__ import annotations

import base64
import io
import sys
import traceback
from typing import Iterable

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import nbformat as nbf


def _capture_figs() -> list:
    outs = []
    nums = plt.get_fignums()
    for n in nums:
        fig = plt.figure(n)
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=110, bbox_inches="tight")
        buf.seek(0)
        outs.append(nbf.v4.new_output(
            output_type="display_data",
            data={"image/png": base64.b64encode(buf.read()).decode("ascii")},
            metadata={},
        ))
        plt.close(fig)
    return outs


def _capture_value(value, execution_count: int):
    if value is None:
        return None
    repr_html = None
    try:
        repr_html = value._repr_html_() if hasattr(value, "_repr_html_") else None
    except Exception:
        repr_html = None
    text = repr(value)
    data = {"text/plain": text}
    if repr_html:
        data["text/html"] = repr_html
    return nbf.v4.new_output(
        output_type="execute_result",
        data=data,
        metadata={},
        execution_count=execution_count,
    )


def run_cells(cells: Iterable[nbf.NotebookNode], *, namespace: dict | None = None) -> list[nbf.NotebookNode]:
    namespace = namespace if namespace is not None else {}
    out_cells: list[nbf.NotebookNode] = []
    execution_count = 0
    for cell in cells:
        if cell.cell_type != "code":
            out_cells.append(cell)
            continue
        execution_count += 1
        cell["execution_count"] = execution_count
        outputs: list[dict] = []
        stdout = io.StringIO()
        src = cell.source
        last_expr = _split_last_expression(src)
        body, tail_expr = last_expr
        old_stdout = sys.stdout
        sys.stdout = stdout
        try:
            if body:
                exec(compile(body, f"<cell {execution_count}>", "exec"), namespace, namespace)
            value = None
            if tail_expr is not None:
                value = eval(compile(tail_expr, f"<cell {execution_count}-tail>", "eval"), namespace, namespace)
        except Exception:
            sys.stdout = old_stdout
            tb = traceback.format_exc()
            outputs.append(nbf.v4.new_output(
                output_type="error",
                ename="Exception",
                evalue="see traceback",
                traceback=tb.splitlines(),
            ))
            cell["outputs"] = outputs
            out_cells.append(cell)
            raise
        finally:
            sys.stdout = old_stdout
        text = stdout.getvalue()
        if text:
            outputs.append(nbf.v4.new_output(output_type="stream", name="stdout", text=text))
        outputs.extend(_capture_figs())
        rep = _capture_value(value, execution_count)
        if rep is not None:
            outputs.append(rep)
        cell["outputs"] = outputs
        out_cells.append(cell)
    return out_cells


def _split_last_expression(src: str) -> tuple[str, str | None]:
    import ast
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return src, None
    if not tree.body:
        return src, None
    last = tree.body[-1]
    if isinstance(last, ast.Expr):
        body_tree = ast.Module(body=tree.body[:-1], type_ignores=tree.type_ignores)
        body_src = ast.unparse(body_tree)
        tail_src = ast.unparse(ast.Expression(body=last.value))
        return body_src, tail_src
    return src, None
