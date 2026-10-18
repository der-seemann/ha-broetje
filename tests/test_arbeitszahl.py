"""Tests for the guarded cumulative working ratio."""

import asyncio
import importlib.util
import sys
from pathlib import Path

_MODULE_PATH = (
    Path(__file__).parents[1]
    / "custom_components"
    / "broetje_heating"
    / "arbeitszahl.py"
)
_SPEC = importlib.util.spec_from_file_location("arbeitszahl", _MODULE_PATH)
assert _SPEC is not None and _SPEC.loader is not None
_MODULE = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _MODULE
_SPEC.loader.exec_module(_MODULE)
ArbeitszahlTracker = _MODULE.ArbeitszahlTracker
valid_baseline_pair = _MODULE.valid_baseline_pair
source_values_available = _MODULE.source_values_available
async_restore_tracker = _MODULE.async_restore_tracker
async_save_tracker = _MODULE.async_save_tracker


def test_ratio_requires_valid_baselines_and_counters() -> None:
    tracker = ArbeitszahlTracker(None, None)
    assert tracker.observe(20, 30) is None
    for value in (None, float("nan"), float("inf"), -1, "bad"):
        assert ArbeitszahlTracker(10, 15).observe(value, 30) is None
    assert ArbeitszahlTracker(10, 15).observe(9, 30) is None
    assert ArbeitszahlTracker(10, 15).observe(10.005, 15.005) is None
    assert ArbeitszahlTracker(10, 15).observe(12, 19) == 2.0


def test_counter_decrease_latches_reset_until_baseline_changes() -> None:
    tracker = ArbeitszahlTracker(10, 15)
    assert tracker.observe(12, 19) == 2.0
    assert tracker.observe(None, 30) is None
    assert tracker.observe(11, 20) is None
    assert tracker.observe(20, 30) is None

    new_baseline = ArbeitszahlTracker(11, 20)
    new_baseline.restore(tracker.dump())
    assert new_baseline.observe(20, 30) == 10 / 9


def test_reset_latch_survives_restore_and_stays_set_above_baseline() -> None:
    tracker = ArbeitszahlTracker(10, 15)
    assert tracker.observe(12, 19) == 2.0
    assert tracker.observe(11, 20) is None

    restored = ArbeitszahlTracker(10, 15)
    restored.restore(tracker.dump())
    assert restored.observe(20, 30) is None
    assert restored.dump()["reset_latched"] is True


def test_store_adapter_restores_reset_latch_after_restart() -> None:
    class MemoryStore:
        def __init__(self) -> None:
            self.value = None

        async def async_load(self):
            return self.value

        async def async_save(self, value):
            self.value = value

    async def scenario() -> None:
        store = MemoryStore()
        first = ArbeitszahlTracker(10, 15)
        first.observe(12, 19)
        assert first.observe(11, 20) is None
        await async_save_tracker(store, first)

        after_restart = ArbeitszahlTracker(10, 15)
        await async_restore_tracker(store, after_restart)
        assert after_restart.observe(20, 30) is None
        assert after_restart.dump()["reset_latched"] is True

    asyncio.run(scenario())


def test_options_baseline_pair_validation() -> None:
    assert valid_baseline_pair(None, None)
    assert valid_baseline_pair(10, 15)
    assert valid_baseline_pair(10.25, 15.75)
    assert not valid_baseline_pair(10, None)
    assert not valid_baseline_pair(None, 15)
    assert not valid_baseline_pair(float("nan"), 15)
    assert not valid_baseline_pair(-1, 15)


def test_stale_source_values_are_unavailable() -> None:
    assert source_values_available(None, None)
    assert source_values_available({"status": "ok"}, {"status": "ok"})
    assert not source_values_available({"status": "sentinel_no_data"}, {"status": "ok"})
    assert not source_values_available({"status": "ok"}, {"status": "read_error"})


def test_restore_rejects_mismatched_baseline_and_unavailable_pair() -> None:
    tracker = ArbeitszahlTracker(10, 15)
    tracker.restore(
        {
            "electrical_baseline": 9,
            "thermal_baseline": 15,
            "last_electrical": 20,
            "last_thermal": 30,
            "reset_latched": True,
        }
    )
    assert tracker.observe(20, 30) == 1.5

    tracker.restore(
        {
            "electrical_baseline": 10,
            "thermal_baseline": 15,
            "last_electrical": 20,
            "last_thermal": None,
            "reset_latched": False,
        }
    )
    assert tracker.observe(19, 31) == 16 / 9
