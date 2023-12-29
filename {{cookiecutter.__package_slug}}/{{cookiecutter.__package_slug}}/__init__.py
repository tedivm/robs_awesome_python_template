try:
    from . import _version

    __version__ = _version.__version__
except: # noqa: E722
    __version__ = "0.0.0-dev"
