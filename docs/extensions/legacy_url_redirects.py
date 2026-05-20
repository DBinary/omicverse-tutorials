"""Sphinx extension: keep legacy MkDocs-style trailing-slash URLs alive.

The omicverse documentation migrated from MkDocs to Sphinx.  MkDocs served
every page at a directory URL with a trailing slash, e.g.

    https://omicverse.readthedocs.io/en/latest/Tutorials-bulk/t_deg/

The Sphinx ``html`` builder instead serves pages as ``<page>.html``:

    https://omicverse.readthedocs.io/en/latest/Tutorials-bulk/t_deg.html

So every external link, bookmark, or citation that used the old
trailing-slash form 404s after the migration.

This extension closes the gap *without* a hand-maintained redirect map.
After the HTML build finishes, for every generated ``<page>.html`` it
writes a sibling ``<page>/index.html`` containing a ``<meta refresh>`` +
``rel=canonical`` pointing back at ``../<page>.html``.  A request for the
legacy URL ``.../t_deg/`` is served that ``index.html`` and bounces the
browser to ``.../t_deg.html``.

Both URL forms then resolve; the canonical link keeps search engines on
the ``.html`` form so there is no duplicate-content penalty.
"""

from __future__ import annotations

from pathlib import Path

from sphinx.util import logging

logger = logging.getLogger(__name__)


_REDIRECT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url={target}">
  <link rel="canonical" href="{target}">
  <meta name="robots" content="noindex">
  <title>Redirecting…</title>
</head>
<body>
  <p>This page moved to <a href="{target}">{target}</a>.</p>
</body>
</html>
"""


def _write_legacy_redirects(app, exception):
    """``build-finished`` hook — emit trailing-slash redirect stubs."""
    if exception is not None:
        return
    if app.builder.name not in ("html",):
        # dirhtml already serves trailing-slash URLs natively; nothing to do.
        return

    outdir = Path(app.outdir)
    written = 0
    for html_path in sorted(outdir.rglob("*.html")):
        rel = html_path.relative_to(outdir)
        # An index.html is already the directory form — skip.
        if html_path.name == "index.html":
            continue
        # Skip Sphinx-internal trees (_static, _sources, _images, …).
        if any(part.startswith("_") for part in rel.parts):
            continue

        stem_dir = html_path.with_suffix("")        # …/t_deg/
        legacy_index = stem_dir / "index.html"      # …/t_deg/index.html
        if legacy_index.exists():
            # A real dir-style page already lives here — don't clobber it.
            continue

        stem_dir.mkdir(parents=True, exist_ok=True)
        legacy_index.write_text(
            _REDIRECT_TEMPLATE.format(target=f"../{html_path.name}"),
            encoding="utf-8",
        )
        written += 1

    logger.info(
        "[legacy_url_redirects] wrote %d trailing-slash redirect stubs", written
    )


def setup(app):
    app.connect("build-finished", _write_legacy_redirects)
    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
