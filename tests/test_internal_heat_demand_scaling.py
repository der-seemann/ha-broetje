"""Regression check for the percent scaling of GTW-08 register 416."""

import ast
import logging
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
IWR_SOURCE = ROOT / "custom_components/broetje_heating/devices/iwr.py"
COORDINATOR_SOURCE = ROOT / "custom_components/broetje_heating/coordinator.py"


def _register_416_scale() -> float:
    tree = ast.parse(IWR_SOURCE.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.AnnAssign):
            targets = (node.target,)
        elif isinstance(node, ast.Assign):
            targets = tuple(node.targets)
        else:
            continue
        if not any(
            isinstance(target, ast.Name)
            and target.id == "_IWR_STATIC_REGISTER_MAP"
            for target in targets
        ):
            continue
        assert isinstance(node.value, ast.Dict)
        for key, value in zip(node.value.keys, node.value.values, strict=True):
            if ast.literal_eval(key) != "internal_heat_demand_power":
                continue
            assert isinstance(value, ast.Dict)
            for field, field_value in zip(
                value.keys, value.values, strict=True
            ):
                if ast.literal_eval(field) == "scale":
                    return ast.literal_eval(field_value)
    raise AssertionError("register 416 is missing from the IWR register map")


class RegisterProcessor:
    @staticmethod
    def _get_sentinel_values(_config: dict[str, Any], _data_type: str) -> set[int]:
        return set()


class InternalHeatDemandScalingTest(unittest.TestCase):
    def test_register_416_preserves_percent_values(self) -> None:
        tree = ast.parse(COORDINATOR_SOURCE.read_text(encoding="utf-8"))
        method = next(
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)
            and node.name == "_process_register_value"
        )
        namespace: dict[str, Any] = {
            "Any": Any,
            "_LOGGER": logging.getLogger(__name__),
        }
        module = ast.Module(body=[method], type_ignores=[])
        exec(
            compile(ast.fix_missing_locations(module), str(COORDINATOR_SOURCE), "exec"),
            namespace,
        )

        scale = _register_416_scale()
        config = {"address": 416, "data_type": "uint16", "scale": scale}
        process_value = namespace["_process_register_value"]

        for raw, expected in ((0, 0), (20, 20), (100, 100)):
            with self.subTest(raw=raw):
                self.assertEqual(
                    process_value(RegisterProcessor(), [raw], config), expected
                )


if __name__ == "__main__":
    unittest.main()
