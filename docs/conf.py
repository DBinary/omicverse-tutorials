import importlib.util
import inspect
import os
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime

HERE = Path(__file__).parent
sys.path[:0] = [str(HERE / "extensions")]

# Try to locate the omicverse package.
# Layout 1 (local dev): HERE.parent.parent is the omicverse-core repo root,
#   which contains the omicverse/ package directory.
# Layout 2 (legacy sibling): a directory named "omicverse-core" lives next to
#   the docs checkout (the old arrangement).
_repo_root = HERE.parent.parent  # omicverse-core repo root when guide is a submodule
if (_repo_root / "omicverse").is_dir():
    sys.path.insert(0, str(_repo_root))
else:
    _core_path = _repo_root / "omicverse-core"
    if _core_path.exists():
        sys.path.insert(0, str(_core_path))

# -- Project information -------------------------------------------------------
project = "omicverse"
author = "Zehua Zeng"
copyright = f"{datetime.now():%Y}, 112 Lab, USTB"
release = "2.1.1"
version = release
repository_url = "https://github.com/Starlitnightly/omicverse"
default_github_ref = "master"


def _fallback_github_ref() -> str:
    for key in ("READTHEDOCS_GIT_IDENTIFIER", "GITHUB_REF_NAME", "READTHEDOCS_VERSION_NAME"):
        value = os.environ.get(key)
        if value and value not in {"latest", "stable"}:
            return value
    return default_github_ref

try:
    from importlib.metadata import metadata as _pkg_meta
    _info = _pkg_meta("omicverse")
    release = version = _info["Version"]
    _author = _info.get("Author") or author
    author = _author
except Exception:
    pass

html_context = {
    "display_github": True,
    "github_user": "Starlitnightly",
    "github_repo": project,
    "github_version": _fallback_github_ref(),
    "conf_py_path": "/docs/",
}

# -- Extensions ---------------------------------------------------------------
extensions = [
    "myst_nb",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx.ext.extlinks",
    "sphinx.ext.autosummary",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinxext.opengraph",
    "hoverxref.extension",
]

# Load custom extensions from docs/extensions/
_ext_dir = HERE / "extensions"
if _ext_dir.exists():
    sys.path.insert(0, str(_ext_dir))
    for _p in sorted(_ext_dir.glob("*.py")):
        extensions.append(_p.stem)

# -- Autodoc / Napoleon -------------------------------------------------------
autosummary_generate = True
autodoc_member_order = "bysource"

# Packages that may be absent in the Read-the-Docs build environment (either
# because they need compilation or are heavy optional extras).  Sphinx will
# create lightweight stub modules so that `import omicverse.space` and friends
# succeed even when these packages aren't installed.
autodoc_mock_imports = [
    "skmisc",
    "torch",
    "torch_geometric",
    "tangram",
    "cell2location",
    "starfysh",
    "spatrio",
    "commot",
    "stlearn",
    "STAGATE_pyG",
    "STAligner",
    "flashdeconv",
]
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_use_rtype = True
napoleon_use_param = True
napoleon_custom_sections = [("Params", "Parameters")]
todo_include_todos = False

# -- MyST / myst-nb -----------------------------------------------------------
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "html_image",
    "html_admonition",
    "substitution",
    "linkify",
]
myst_url_schemes = ("http", "https", "mailto")
nb_output_stderr = "remove"
nb_execution_mode = "off"
nb_merge_streams = True
typehints_defaults = "braces"

# -- Source files -------------------------------------------------------------
source_suffix = {
    ".rst": "restructuredtext",
    ".ipynb": "myst-nb",
    ".myst": "myst-nb",
    ".md": "myst-nb",
}
templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**.ipynb_checkpoints",
    "overrides.mkdocs.backed",
    "css.mkdocs.backed",
    "site",
]
needs_sphinx = "4.0"
# Don't treat unresolved citations/references as build failures
nitpicky = False

# -- extlinks / intersphinx ---------------------------------------------------
extlinks = {
    "issue": (f"{repository_url}/issues/%s", "#%s"),
    "pr": (f"{repository_url}/pull/%s", "#%s"),
    "ghuser": ("https://github.com/%s", "@%s"),
}

intersphinx_mapping = {
    "anndata": ("https://anndata.readthedocs.io/en/stable/", None),
    "ipython": ("https://ipython.readthedocs.io/en/stable/", None),
    "matplotlib": ("https://matplotlib.org/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "python": ("https://docs.python.org/3", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference/", None),
    "sklearn": ("https://scikit-learn.org/stable/", None),
    "torch": ("https://pytorch.org/docs/stable/", None),
    "scanpy": ("https://scanpy.readthedocs.io/en/stable/", None),
    "mudata": ("https://mudata.readthedocs.io/en/stable/", None),
    "huggingface_hub": ("https://huggingface.co/docs/huggingface_hub/main/en", None),
}

# -- HTML / sphinx_book_theme -------------------------------------------------
html_theme = "sphinx_book_theme"
html_title = project
html_logo = "_static/logo.png"
html_favicon = "_static/favicon.ico"

html_theme_options = {
    "repository_url": repository_url,
    "repository_branch": default_github_ref,
    "path_to_docs": "docs",
    "use_repository_button": True,
    "use_edit_page_button": True,
    "use_source_button": True,
    "use_issues_button": True,
    "use_download_button": True,
    "home_page_in_toc": True,
    "show_navbar_depth": 1,
    "navigation_with_keys": True,
    "logo": {
        "image_light": "_static/logo.png",
        "image_dark": "_static/logo.png",
        "text": project,
    },
}

# Pygments styles are overridden by custom.css token palette, but set sensible
# defaults in case the user disables custom.css.
pygments_style = "tango"
pygments_dark_style = "monokai"

html_static_path = ["_static"]
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
    "css/custom.css",
    "css/icons.css",
    "css/override.css",
]
html_show_sphinx = False

# -- Linkcode -----------------------------------------------------------------
def _git(*args):
    return subprocess.check_output(["git", *args]).strip().decode()

_git_ref = None
try:
    _git_ref = _git("name-rev", "--name-only", "--no-undefined", "HEAD")
    _git_ref = re.sub(r"^(remotes/[^/]+|tags)/", "", _git_ref)
except Exception:
    pass
if not _git_ref or re.search(r"[\^~]", _git_ref):
    try:
        _git_ref = _git("rev-parse", "HEAD")
    except Exception:
        _git_ref = _fallback_github_ref()

_omicverse_module_path = None
try:
    _spec = importlib.util.find_spec("omicverse")
    if _spec and _spec.origin:
        _omicverse_module_path = os.path.dirname(_spec.origin)
except Exception:
    pass


def linkcode_resolve(domain, info):
    """Resolve a Python object to its GitHub source URL."""
    if domain != "py":
        return None
    if not _omicverse_module_path:
        return None
    try:
        obj = sys.modules[info["module"]]
        for part in info["fullname"].split("."):
            obj = getattr(obj, part)
        obj = inspect.unwrap(obj)
        if isinstance(obj, property):
            obj = inspect.unwrap(obj.fget)
        path = os.path.relpath(inspect.getsourcefile(obj), start=_omicverse_module_path)
        src, lineno = inspect.getsourcelines(obj)
    except Exception:
        return None
    path = f"{path}#L{lineno}-L{lineno + len(src) - 1}"
    return f"{repository_url}/blob/{_git_ref}/omicverse/{path}"


# -- Hoverxref ----------------------------------------------------------------
hoverx_default_type = "tooltip"
hoverxref_domains = ["py"]
hoverxref_role_types = dict.fromkeys(
    ["ref", "class", "func", "meth", "attr", "exc", "data", "mod"],
    "tooltip",
)
hoverxref_intersphinx = ["python", "numpy", "scanpy", "anndata", "scipy", "pandas"]
if os.environ.get("READTHEDOCS"):
    hoverxref_api_host = "/_"
