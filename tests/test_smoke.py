import importlib

import pytest

MODULES = [
    "aisense",
    "aisense.constants",
    "aisense.maths",
    "aisense.generative_model",
    "aisense.env",
    "aisense.agent",
    "aisense.baselines",
]


@pytest.mark.parametrize("name", MODULES)
def test_module_imports(name: str) -> None:
    importlib.import_module(name)
