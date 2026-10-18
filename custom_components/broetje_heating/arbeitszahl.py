"""Guarded cumulative heat-pump working ratio calculation."""

from __future__ import annotations

import math
from typing import Any


def finite_counter(value: Any) -> float | None:
    """Return a finite non-negative counter value, otherwise None."""
    if value is None or isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) and number >= 0 else None


def valid_baseline_pair(electrical: Any, thermal: Any) -> bool:
    """Accept both omitted baselines or a pair of finite non-negative values."""
    if electrical is None and thermal is None:
        return True
    return (
        finite_counter(electrical) is not None and finite_counter(thermal) is not None
    )


def source_values_available(electrical_detail: Any, thermal_detail: Any) -> bool:
    """Reject stale coordinator values when either current register read failed."""
    return all(
        detail is None or detail.get("status") == "ok"
        for detail in (electrical_detail, thermal_detail)
    )


class ArbeitszahlTracker:
    """Track two cumulative counters and latch counter resets until baseline changes."""

    def __init__(self, electrical_baseline: Any, thermal_baseline: Any) -> None:
        self.electrical_baseline = finite_counter(electrical_baseline)
        self.thermal_baseline = finite_counter(thermal_baseline)
        self.last_electrical: float | None = None
        self.last_thermal: float | None = None
        self.reset_latched = False

    @property
    def baseline_valid(self) -> bool:
        """Return whether both baselines are configured and valid."""
        return (
            self.electrical_baseline is not None and self.thermal_baseline is not None
        )

    def restore(self, saved: dict[str, Any] | None) -> None:
        """Restore last pair and latch only when saved baselines still match."""
        if not saved or not self.baseline_valid:
            return
        if (
            finite_counter(saved.get("electrical_baseline")) != self.electrical_baseline
            or finite_counter(saved.get("thermal_baseline")) != self.thermal_baseline
        ):
            return
        self.last_electrical = finite_counter(saved.get("last_electrical"))
        self.last_thermal = finite_counter(saved.get("last_thermal"))
        self.reset_latched = saved.get("reset_latched") is True

    def observe(self, electrical: Any, thermal: Any) -> float | None:
        """Observe counters and return guarded ratio, or None when invalid."""
        electrical_value = finite_counter(electrical)
        thermal_value = finite_counter(thermal)
        if electrical_value is None or thermal_value is None:
            return None

        if (
            self.last_electrical is not None
            and self.last_thermal is not None
            and (
                electrical_value < self.last_electrical
                or thermal_value < self.last_thermal
            )
        ):
            self.reset_latched = True
        self.last_electrical = electrical_value
        self.last_thermal = thermal_value

        if (
            not self.baseline_valid
            or self.reset_latched
            or electrical_value < self.electrical_baseline
            or thermal_value < self.thermal_baseline
        ):
            return None
        electrical_delta = electrical_value - self.electrical_baseline
        thermal_delta = thermal_value - self.thermal_baseline
        if electrical_delta <= 0.01:
            return None
        ratio = thermal_delta / electrical_delta
        return ratio if math.isfinite(ratio) else None

    def dump(self) -> dict[str, Any]:
        """Return minimal state for persistent reset detection."""
        return {
            "electrical_baseline": self.electrical_baseline,
            "thermal_baseline": self.thermal_baseline,
            "last_electrical": self.last_electrical,
            "last_thermal": self.last_thermal,
            "reset_latched": self.reset_latched,
        }


async def async_restore_tracker(store: Any, tracker: ArbeitszahlTracker) -> None:
    """Restore tracker state from a Home Assistant Store-compatible object."""
    tracker.restore(await store.async_load())


async def async_save_tracker(store: Any, tracker: ArbeitszahlTracker) -> None:
    """Persist only the tracker pair and reset latch through Store-compatible API."""
    await store.async_save(tracker.dump())
