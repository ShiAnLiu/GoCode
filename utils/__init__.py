"""Utils module - lazy imports to avoid hard dependency chains."""

from typing import Any

__all__ = ['AIClient', 'APIConfig', 'APIProvider', 'SecurityManager']

_MODULE_MAP = {
    'AIClient': '.ai_client',
    'APIConfig': '.api_config',
    'APIProvider': '.api_config',
    'SecurityManager': '.security',
}


def __getattr__(name: str) -> Any:
    if name not in _MODULE_MAP:
        raise AttributeError(f"module 'utils' has no attribute {name!r}")
    import importlib
    submodule = importlib.import_module(_MODULE_MAP[name], __name__)
    cls = getattr(submodule, name)
    globals()[name] = cls
    return cls
