"""Source and builder checks for manufacturer-documented optional modules."""

import ast
import csv
import importlib.util
import json
import logging
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "custom_components.broetje_heating"


def _load_optional_module():
    package = types.ModuleType(PACKAGE)
    package.__path__ = [str(ROOT / "custom_components/broetje_heating")]
    sys.modules[PACKAGE] = package
    devices = types.ModuleType(f"{PACKAGE}.devices")
    devices.__path__ = [str(ROOT / "custom_components/broetje_heating/devices")]
    sys.modules[devices.__name__] = devices
    spec = importlib.util.spec_from_file_location(
        f"{PACKAGE}.devices.iwr_optional",
        ROOT / "custom_components/broetje_heating/devices/iwr_optional.py",
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_optional_specs_build_source_backed_read_only_sensor_maps() -> None:
    module = _load_optional_module()
    registers, sensors, enums = module.build_optional_iwr_maps()
    assert len(module.OPTIONAL_IWR_SENSOR_SPECS) == 101
    assert len(registers) == len(sensors) == 101
    assert len({spec["address"] for spec in module.OPTIONAL_IWR_SENSOR_SPECS}) == 101
    assert all(config["register"] in registers for config in sensors.values())
    assert all("writable" not in config for config in registers.values())
    assert all(registers[key]["source_access"] in {"R", "R/W"} for key in registers)
    assert all(spec["data_type"] in {"uint8", "int8", "int16", "uint16", "uint32", "enum8", "bool"} for spec in module.OPTIONAL_IWR_SENSOR_SPECS)
    assert all(sensors[key]["enum_map"] in enums for key in sensors if "enum_map" in sensors[key])


def test_optional_register_csv_rows_match_generated_maps() -> None:
    module = _load_optional_module()
    addresses = {spec["address"]: spec for spec in module.OPTIONAL_IWR_SENSOR_SPECS}
    with (ROOT / "custom_components/broetje_heating/register_map.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    for address, spec in addresses.items():
        matches = [row for row in rows if row["register"] == str(address)]
        assert matches, address
        row = next((item for item in matches if item["ha_sensor_name"] == spec["key"]), None)
        assert row is not None, address
        assert row["datatype"] == spec["data_type"], address
        assert row["rw_spec"] == spec["source_access"], address
        assert row["rw_implemented"] == "R", address


def test_optional_translation_keys_exist_in_both_locales() -> None:
    module = _load_optional_module()
    keys = {spec["key"] for spec in module.OPTIONAL_IWR_SENSOR_SPECS}
    for locale in ("en", "de"):
        translations = json.loads(
            (ROOT / f"custom_components/broetje_heating/translations/{locale}.json").read_text()
        )
        sensor_keys = translations["entity"]["sensor"]
        assert keys <= sensor_keys.keys()


def test_optional_features_are_filtered_independently() -> None:
    source = (ROOT / "custom_components/broetje_heating/devices/iwr.py").read_text()
    tree = ast.parse(source)
    wanted = {"_feature_for_register", "_filter_iwr_register_map"}
    methods = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name in wanted
    ]
    namespace = {
        "FEATURE_CASCADE": "cascade",
        "FEATURE_HYBRID": "hybrid",
        "FEATURE_BUFFER_TANK": "buffer_tank",
        "FEATURE_SOLAR": "solar",
        "FEATURE_THERMODYNAMIC_WATER_HEATER": "thermodynamic_water_heater",
        "FEATURE_BMS": "bms",
        "FEATURE_COOLING": "cooling",
        "SUBDEV_CASCADE": "cascade",
        "SUBDEV_BUFFER_TANK": "buffer_tank",
        "SUBDEV_SOLAR": "solar",
        "SUBDEV_THERMODYNAMIC_WATER_HEATER": "thermodynamic_water_heater",
        "SUBDEV_BMS": "bms",
        "SUBDEV_HYBRID": "hybrid",
        "_is_zone_key_allowed": lambda *_args, **_kwargs: True,
    }
    module = ast.Module(body=methods, type_ignores=[])
    exec(compile(ast.fix_missing_locations(module), "iwr.py", "exec"), namespace)  # noqa: S102
    classify = namespace["_feature_for_register"]
    filter_map = namespace["_filter_iwr_register_map"]
    fixtures = {
        "manufacturer_cascade_7001": {"address": 7001, "sub_device": "cascade"},
        "manufacturer_hybrid_462": {"address": 462, "sub_device": "hybrid"},
        "manufacturer_solar_8114": {"address": 8114, "sub_device": "solar"},
        "manufacturer_thermodynamic_water_heater_9006": {"address": 9006, "sub_device": "thermodynamic_water_heater"},
        "manufacturer_bms_21024": {"address": 21024, "sub_device": "bms"},
    }
    assert filter_map(fixtures, {}, None) == {}
    for key, config in fixtures.items():
        feature = classify(key, config)
        assert feature
        assert set(filter_map(fixtures, {feature: True}, None)) == {key}


def _load_iwr_module():
    package_name = PACKAGE
    package = types.ModuleType(package_name)
    package.__path__ = [str(ROOT / "custom_components/broetje_heating")]
    sys.modules[package_name] = package
    devices = types.ModuleType(f"{package_name}.devices")
    devices.__path__ = [str(ROOT / "custom_components/broetje_heating/devices")]
    sys.modules[devices.__name__] = devices

    const_spec = importlib.util.spec_from_file_location(
        f"{package_name}.const", ROOT / "custom_components/broetje_heating/const.py"
    )
    assert const_spec and const_spec.loader
    const_module = importlib.util.module_from_spec(const_spec)
    sys.modules[const_spec.name] = const_module
    const_spec.loader.exec_module(const_module)

    optional_spec = importlib.util.spec_from_file_location(
        f"{package_name}.devices.iwr_optional",
        ROOT / "custom_components/broetje_heating/devices/iwr_optional.py",
    )
    assert optional_spec and optional_spec.loader
    optional_module = importlib.util.module_from_spec(optional_spec)
    sys.modules[optional_spec.name] = optional_module
    optional_spec.loader.exec_module(optional_module)

    iwr_spec = importlib.util.spec_from_file_location(
        f"{package_name}.devices.iwr",
        ROOT / "custom_components/broetje_heating/devices/iwr.py",
    )
    assert iwr_spec and iwr_spec.loader
    iwr_module = importlib.util.module_from_spec(iwr_spec)
    sys.modules[iwr_spec.name] = iwr_module
    iwr_spec.loader.exec_module(iwr_module)
    return iwr_module


def test_defrost_sensor_is_independent_of_hybrid_feature_gate() -> None:
    module = _load_iwr_module()
    hybrid_entities = {
        "sensors": {"hybrid_cop", "hybrid_cop_threshold"},
        "selects": {"hybrid_mode_selected"},
        "numbers": {"hybrid_electricity_cost_high_tariff"},
    }

    without_hybrid = module.get_iwr_device_config(zones=[], features={"hybrid": False})
    assert "heat_pump_defrost" in without_hybrid["register_map"]
    assert "heat_pump_defrost" in without_hybrid["sensors"]
    hybrid_registers = set().union(*hybrid_entities.values())
    assert not (hybrid_registers & without_hybrid["register_map"].keys())
    for entity_type, keys in hybrid_entities.items():
        assert not (keys & without_hybrid[entity_type].keys())

    with_hybrid = module.get_iwr_device_config(zones=[], features={"hybrid": True})
    assert "heat_pump_defrost" in with_hybrid["sensors"]
    assert hybrid_registers <= with_hybrid["register_map"].keys()
    for entity_type, keys in hybrid_entities.items():
        assert keys <= with_hybrid[entity_type].keys()


def test_optional_default_features_and_solar_autodetection_gate() -> None:
    iwr_tree = ast.parse(
        (ROOT / "custom_components/broetje_heating/devices/iwr.py").read_text()
    )
    config_builder = next(
        node for node in ast.walk(iwr_tree)
        if isinstance(node, ast.FunctionDef) and node.name == "get_iwr_device_config"
    )
    default_features = next(
        node.value for node in ast.walk(config_builder)
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "features" for target in node.targets)
        and isinstance(node.value, ast.Dict)
    )
    optional_defaults = {
        ast.unparse(key): ast.literal_eval(value)
        for key, value in zip(default_features.keys, default_features.values, strict=True)
        if ast.unparse(key) in {
            "FEATURE_SOLAR", "FEATURE_THERMODYNAMIC_WATER_HEATER", "FEATURE_BMS"
        }
    }
    assert optional_defaults == {
        "FEATURE_SOLAR": False,
        "FEATURE_THERMODYNAMIC_WATER_HEATER": False,
        "FEATURE_BMS": False,
    }

    coordinator_tree = ast.parse(
        (ROOT / "custom_components/broetje_heating/coordinator.py").read_text()
    )
    detect = next(
        node for node in ast.walk(coordinator_tree)
        if isinstance(node, ast.AsyncFunctionDef) and node.name == "_detect_sub_devices"
    )
    calls = [node for node in ast.walk(detect) if isinstance(node, ast.Call)]
    probe = next(
        call.lineno for call in calls
        if isinstance(call.func, ast.Attribute)
        and call.func.attr == "_read_registers"
        and call.args and ast.literal_eval(call.args[0]) == 8114
    )
    apply_config = next(
        call.lineno for call in calls
        if isinstance(call.func, ast.Attribute) and call.func.attr == "_apply_device_config"
    )
    assert apply_config > probe
    assert not any(
        isinstance(call.func, ast.Attribute)
        and call.func.attr == "_read_registers"
        and call.args and ast.literal_eval(call.args[0]) in {9001, 21020}
        for call in calls
    )


def test_optional_signed_decoding_and_sentinels() -> None:
    source_path = ROOT / "custom_components/broetje_heating/coordinator.py"
    tree = ast.parse(source_path.read_text())
    method = next(
        node for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == "_process_register_value"
    )
    sentinels = next(
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.AnnAssign)
        and isinstance(node.target, ast.Name)
        and node.target.id == "_SENTINEL_VALUES"
    )
    sentinel_map = ast.literal_eval(sentinels)
    namespace = {
        "Any": object,
        "_LOGGER": logging.getLogger(__name__),
        "_SENTINEL_VALUES": sentinel_map,
    }
    exec(compile(ast.fix_missing_locations(ast.Module(body=[method], type_ignores=[])), "coordinator.py", "exec"), namespace)  # noqa: S102

    class Decoder:
        @staticmethod
        def _get_sentinel_values(config, data_type):
            return set(config.get("sentinel_values", sentinel_map[data_type]))

    decode = namespace["_process_register_value"]
    decoder = Decoder()
    assert decode(decoder, [0x00FF], {"data_type": "uint8", "scale": 1}) is None
    assert decode(decoder, [0x00FF], {"data_type": "enum8", "scale": 1}) is None
    assert decode(decoder, [0x00FE], {"data_type": "int8", "scale": 0.1}) == -0.2
    assert decode(decoder, [0xFFFF], {"data_type": "int8", "scale": 0.1}) is None
    assert decode(decoder, [0xFF9C], {"data_type": "int16", "scale": 0.1}) == -10.0
    assert decode(decoder, [7], {"data_type": "enum8", "scale": 1}) == 7
