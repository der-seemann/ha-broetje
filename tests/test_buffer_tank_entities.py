"""Source-backed checks for the newly mapped BufferTank entities."""

import ast
import csv
import __future__
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IWR_PATH = ROOT / "custom_components/broetje_heating/devices/iwr.py"
REGISTER_CSV = ROOT / "custom_components/broetje_heating/register_map.csv"
COORDINATOR_PATH = ROOT / "custom_components/broetje_heating/coordinator.py"

NUMBER_KEYS = {
    "buffer_hysteresis_start",
    "buffer_hysteresis_stop",
    "buffer_pump_post_run",
    "buffer_fixed_setpoint_heating",
    "buffer_fixed_setpoint_cooling",
    "buffer_slope",
    "buffer_setpoint_offset",
}
SENSOR_KEYS = {
    "buffer_tank_requested_power",
    "buffer_tank_requested_setpoint",
    "buffer_tank_heat_demand_type",
}


def _mapping_keys(tree: ast.Module, mapping_name: str) -> set[str]:
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.target.id == mapping_name
            and isinstance(node.value, ast.Dict)
        ):
            return {
                key.value
                for key in node.value.keys
                if isinstance(key, ast.Constant) and isinstance(key.value, str)
            }
    raise AssertionError(f"mapping {mapping_name} not found")


def _mapping_entry(tree: ast.Module, mapping_name: str, wanted: str) -> dict:
    constants = {
        "IWR_SCALE_TEMP": 0.01,
        "REG_HOLDING": "holding",
        "SUBDEV_BUFFER_TANK": "buffer_tank",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.target.id != mapping_name or not isinstance(node.value, ast.Dict):
                continue
            for key, value in zip(node.value.keys, node.value.values, strict=True):
                if isinstance(key, ast.Constant) and key.value == wanted:

                    class ResolveConstants(ast.NodeTransformer):
                        def visit_Name(self, name: ast.Name) -> ast.AST:
                            return ast.copy_location(
                                ast.Constant(value=constants[name.id]), name
                            )

                    expression = ResolveConstants().visit(ast.Expression(value))
                    return ast.literal_eval(ast.fix_missing_locations(expression))
    raise AssertionError(f"{mapping_name}[{wanted!r}] not found")


def _source_register_decoder():
    tree = ast.parse(COORDINATOR_PATH.read_text())
    method = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
        and node.name == "_process_register_value"
    )
    stub = ast.parse(
        "def _get_sentinel_values(self, config, data_type):\n    return set()\n"
    ).body[0]
    decoder = ast.ClassDef(
        name="SourceRegisterDecoder",
        bases=[],
        keywords=[],
        body=[stub, method],
        decorator_list=[],
    )
    module = ast.Module(body=[decoder], type_ignores=[])
    ast.fix_missing_locations(module)
    namespace: dict = {}
    exec(
        compile(
            module,
            str(COORDINATOR_PATH),
            "exec",
            flags=__future__.annotations.compiler_flag,
        ),
        namespace,
    )
    return namespace["SourceRegisterDecoder"]()


def test_all_buffer_controls_and_diagnostics_are_generated() -> None:
    tree = ast.parse(IWR_PATH.read_text())
    assert NUMBER_KEYS <= _mapping_keys(tree, "_IWR_STATIC_NUMBERS")
    assert SENSOR_KEYS <= _mapping_keys(tree, "_IWR_STATIC_SENSORS")
    assert {"buffer_control_strategy"} <= _mapping_keys(tree, "_IWR_STATIC_SELECTS")

    all_controls = NUMBER_KEYS | {"buffer_control_strategy"}
    for key in all_controls:
        register = _mapping_entry(tree, "_IWR_STATIC_REGISTER_MAP", key)
        assert register["writable"] is True
        assert register["type"] == "holding"
        assert register["address"] in range(7500, 7508)
    assert (
        _mapping_entry(tree, "_IWR_STATIC_SELECTS", "buffer_control_strategy")[
            "enum_map"
        ]
        == "iwr_buffer_control_strategy"
    )

    expected_sensors = {
        "buffer_tank_requested_power": (7604, "uint8", 1),
        "buffer_tank_requested_setpoint": (7605, "int16", 0.01),
        "buffer_tank_heat_demand_type": (7606, "uint8", 1),
    }
    for key, expected in expected_sensors.items():
        register = _mapping_entry(tree, "_IWR_STATIC_REGISTER_MAP", key)
        assert (
            register["address"],
            register["data_type"],
            register["scale"],
        ) == expected
        assert (
            _mapping_entry(tree, "_IWR_STATIC_SENSORS", key)["sub_device"]
            == "buffer_tank"
        )

    power_register = _mapping_entry(
        tree, "_IWR_STATIC_REGISTER_MAP", "buffer_tank_requested_power"
    )
    power_sensor = _mapping_entry(
        tree, "_IWR_STATIC_SENSORS", "buffer_tank_requested_power"
    )
    assert 20 * power_register["scale"] == 20
    assert power_sensor["unit"] == "%"


def test_buffer_requested_power_raw_value_decodes_as_percent() -> None:
    tree = ast.parse(IWR_PATH.read_text())
    register = _mapping_entry(tree, "_IWR_STATIC_REGISTER_MAP", "buffer_tank_requested_power")
    decoder = _source_register_decoder()
    assert decoder._process_register_value([20], register) == 20
    assert decoder._process_register_value([20], {**register, "scale": 0.01}) == 0.2


def test_buffer_register_metadata_matches_documented_ranges_and_access() -> None:
    rows = {
        row["register"]: row
        for row in csv.DictReader(REGISTER_CSV.open(newline="", encoding="utf-8"))
    }
    expected = {
        "7500": ("int16", "0.01", "RW", "°C"),
        "7501": ("int16", "0.01", "RW", "°C"),
        "7502": ("uint8", "", "RW", "min"),
        "7503": ("enum8", "", "RW", ""),
        "7504": ("uint16", "0.01", "RW", "°C"),
        "7505": ("uint16", "0.01", "RW", "°C"),
        "7506": ("uint8", "0.1", "RW", ""),
        "7507": ("uint16", "0.01", "RW", "°C"),
        "7604": ("uint8", "1", "R", "%"),
        "7605": ("int16", "0.01", "R", "°C"),
        "7606": ("enum8", "", "R", ""),
    }
    for address, (datatype, scale, access, unit) in expected.items():
        row = rows[address]
        assert row["datatype"].lower() == datatype
        assert row["scaling_factor"] == scale
        assert row["rw_implemented"] == access
        assert row["unit"] == unit
    assert rows["7502"]["min_max"] == "0–255"
    assert rows["7506"]["min_max"] == "0–25.5"
    assert rows["7503"]["min_max"] == "0–2"
    assert rows["7606"]["min_max"] == "0–10"

    coordinator_tree = ast.parse(COORDINATOR_PATH.read_text())
    sentinel_node = next(
        node.value
        for node in ast.walk(coordinator_tree)
        if isinstance(node, ast.AnnAssign)
        and isinstance(node.target, ast.Name)
        and node.target.id == "_SENTINEL_VALUES"
    )
    sentinels = ast.literal_eval(sentinel_node)
    assert sentinels["uint8"] == {0x00FF, 0xFFFF}
    assert sentinels["enum8"] == {0x00FF, 0xFFFF}
    assert sentinels["int16"] == {-1, -32768}
