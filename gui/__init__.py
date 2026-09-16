"""GUI module - lazy imports since Kivy is an optional dependency."""

from typing import Any

__all__ = ['GocodeApp', 'run']


def __getattr__(name: str) -> Any:
    if name not in ('GocodeApp', 'run'):
        raise AttributeError(f"module 'gui' has no attribute {name!r}")
    from . import main_window
    cls = getattr(main_window, name)
    globals()[name] = cls
    return cls
