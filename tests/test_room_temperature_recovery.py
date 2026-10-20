"""Focused regression tests for room-temperature freshness and register recovery."""

import ast
import logging
import math
from datetime import UTC, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXT_SENSOR = ROOT / "custom_components/broetje_heating/external_room_sensor.py"
COORDINATOR = ROOT / "custom_components/broetje_heating/coordinator.py"


def _methods(path: Path, names: set[str], namespace: dict):
    tree = ast.parse(path.read_text())
    methods = [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name in names
    ]
    assert {method.name for method in methods} == names
    module = ast.Module(body=methods, type_ignores=[])
    exec(compile(ast.fix_missing_locations(module), str(path), "exec"), namespace)  # noqa: S102
    return namespace


def test_fresh_unchanged_reports_remain_eligible_and_min_strategy_is_preserved() -> None:
    now = datetime(2026, 10, 20, 10, tzinfo=UTC)
    namespace = _methods(
        EXT_SENSOR,
        {"_collect_samples", "_aggregate", "_invalid_reason", "_aggregation_suspect_reason"},
        {
            "Any": object,
            "STATE_UNKNOWN": "unknown",
            "STATE_UNAVAILABLE": "unavailable",
            "EXTERNAL_ROOM_SENSOR_AGGREGATION_MIN": "min",
            "EXTERNAL_ROOM_SENSOR_AGGREGATION_MAX": "max",
            "_DIVERGENCE_WARNING_THRESHOLD": 1.0,
            "_LOGGER": logging.getLogger(__name__),
            "math": math,
            "dt_util": type("DT", (), {"utcnow": staticmethod(lambda: now)}),
            "fmean": lambda values: sum(values) / len(values),
        },
    )
    reported = now - timedelta(minutes=89)
    unchanged = now - timedelta(hours=8)

    class State:
        def __init__(self, value, report):
            self.state = str(value)
            self.last_changed = unchanged
            self.last_updated = report
            self.last_reported = report

    class States:
        def get(self, entity_id):
            return {
                "sensor.cold": State(18.0, reported),
                "sensor.warm": State(20.2, now - timedelta(minutes=2)),
                "sensor.expired": State(17.0, now - timedelta(minutes=91)),
                "sensor.future": State(18.0, now + timedelta(minutes=1)),
                "sensor.nan": State(float("nan"), now),
                "sensor.infinity": State(float("inf"), now),
            }.get(entity_id)

    sync = type("Sync", (), {"hass": type("Hass", (), {"states": States()})()})()
    samples = namespace["_collect_samples"](
        sync,
        [
            "sensor.cold",
            "sensor.warm",
            "sensor.expired",
            "sensor.future",
            "sensor.nan",
            "sensor.infinity",
        ],
        3,
        90 * 60,
    )
    assert [sample["entity_id"] for sample in samples] == ["sensor.cold", "sensor.warm"]
    assert namespace["_invalid_reason"](sync, 3, samples, "min", 90 * 60) is None
    assert namespace["_aggregate"](samples, "min") == (18.0, "sensor.cold")
    assert namespace["_aggregation_suspect_reason"](sync, samples, "min", 90 * 60)


def test_register_recovery_is_scoped_to_the_successfully_read_register() -> None:
    namespace = _methods(
        COORDINATOR,
        {"_handle_successful_register_read"},
        {"SENTINEL_AUTO_DISABLE_THRESHOLD": 3},
    )
    class Coordinator:
        _handle_successful_register_read = namespace["_handle_successful_register_read"]

        def __init__(self):
            self._sentinel_fail_counts = {"zone3_room_temp_measured": 3}
            self._exception10_fail_counts = {}
            self._exception3_fail_counts = {}
            self._register_poll_state = {
                "zone3_room_temp_measured": {"mode": "sentinel_temp"},
                "zone3_room_temp": {"mode": "sentinel_temp"},
            }
            self.recovered = []

        @staticmethod
        def _is_sentinel_value(registers, *_args):
            return registers == [0xFFFF]

        def _enable_registry_entities_after_register_recovery(self, key):
            self.recovered.append(key)

    coordinator = Coordinator()
    valid_config = {"data_type": "int16"}
    coordinator._handle_successful_register_read(
        "zone3_room_temp_measured", [188], valid_config
    )
    assert "zone3_room_temp_measured" not in coordinator._register_poll_state
    assert coordinator._register_poll_state["zone3_room_temp"]["mode"] == "sentinel_temp"
    assert coordinator.recovered == ["zone3_room_temp_measured"]

    coordinator._register_poll_state["zone3_room_temp_measured"] = {
        "mode": "sentinel_temp"
    }
    coordinator._handle_successful_register_read(
        "zone3_room_temp_measured", [0xFFFF], valid_config
    )
    assert coordinator._register_poll_state["zone3_room_temp_measured"]["mode"] == "sentinel_temp"
    assert coordinator.recovered == ["zone3_room_temp_measured"]


def test_write_readback_recovery_is_guarded_by_exact_match() -> None:
    tree = ast.parse(COORDINATOR.read_text())
    write_method = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.AsyncFunctionDef)
        and node.name == "async_write_register"
    )
    recovery_calls = [
        node
        for node in ast.walk(write_method)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "_handle_successful_register_read"
    ]
    assert len(recovery_calls) == 1
    guard = next(
        node
        for node in ast.walk(write_method)
        if isinstance(node, ast.If)
        and isinstance(node.test, ast.Compare)
        and isinstance(node.test.left, ast.Name)
        and node.test.left.id == "readback_words"
    )
    assert "_handle_successful_register_read" not in ast.unparse(guard.body)
    assert "_handle_successful_register_read" in ast.unparse(guard.orelse)


def test_registry_recovery_only_reenables_integration_disabled_matching_entities() -> None:
    class Entry:
        def __init__(self, entity_id, unique_id, disabled_by):
            self.entity_id = entity_id
            self.unique_id = unique_id
            self.disabled_by = disabled_by
            self.platform = "broetje_heating"

    entries = [
        Entry("sensor.auto", "entry_zone3_room_temp_measured", "integration"),
        Entry("sensor.user", "entry_zone3_room_temp_measured", "user"),
        Entry("sensor.other", "entry_zone3_room_temp", "integration"),
    ]
    updates = []

    class Registry:
        def async_update_entity(self, entity_id, **kwargs):
            updates.append((entity_id, kwargs))

    class RegistryAPI:
        RegistryEntryDisabler = type("Disabler", (), {"INTEGRATION": "integration"})

        @staticmethod
        def async_get(_hass):
            return Registry()

        @staticmethod
        def async_entries_for_config_entry(_registry, _entry_id):
            return entries

    namespace = _methods(
        COORDINATOR,
        {"_enable_registry_entities_after_register_recovery"},
        {"er": RegistryAPI, "DOMAIN": "broetje_heating", "_LOGGER": logging.getLogger(__name__)},
    )

    class Coordinator:
        _enable_registry_entities_after_register_recovery = namespace[
            "_enable_registry_entities_after_register_recovery"
        ]
        hass = object()
        config_entry = type("Config", (), {"unique_id": "entry", "entry_id": "cfg"})()

        def __init__(self):
            self._register_entities = {
                "zone3_room_temp_measured": ["zone3_room_temp_measured"]
            }

    assert Coordinator()._enable_registry_entities_after_register_recovery(
        "zone3_room_temp_measured"
    ) == 1
    assert updates == [("sensor.auto", {"disabled_by": None})]
