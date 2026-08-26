"""Core module - lazy imports to avoid hard dependency chains."""

from typing import Any

__all__ = [
    'ProjectInitializer',
    'RequirementAnalyzer',
    'ResourceAcquirer',
    'DevelopmentManager',
    'TestManager',
    'AcceptanceManager',
]

_MODULE_MAP = {
    'ProjectInitializer': '.project_init',
    'RequirementAnalyzer': '.requirement_analysis',
    'ResourceAcquirer': '.resource_acquisition',
    'DevelopmentManager': '.development',
    'TestManager': '.testing',
    'AcceptanceManager': '.acceptance',
}


def __getattr__(name: str) -> Any:
    if name not in _MODULE_MAP:
        raise AttributeError(f"module 'core' has no attribute {name!r}")
    import importlib
    submodule = importlib.import_module(_MODULE_MAP[name], __name__)
    cls = getattr(submodule, name)
    globals()[name] = cls
    return cls
