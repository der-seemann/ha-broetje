"""Sync selected Home Assistant temperature sensors into Brötje room-temperature registers."""

from __future__ import annotations

import logging
from collections.abc import Callable
from datetime import timedelta
from statistics import fmean
from typing import Any

from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.event import (
    async_track_state_change_event,
    async_track_time_interval,
)
from homeassistant.helpers.storage import Store
from homeassistant.util import dt as dt_util

from .const import (
    CONF_EXTERNAL_ROOM_SENSORS,
    CONF_EXTERNAL_ROOM_SENSOR_AGGREGATION,
    CONF_EXTERNAL_ROOM_SENSOR_ENTITY_IDS,
    CONF_EXTERNAL_ROOM_SENSOR_TIMEOUT,
    CONF_EXTERNAL_ROOM_SENSOR_WRITE_INTERVAL,
    DEFAULT_EXTERNAL_ROOM_SENSOR_TIMEOUT,
    DEFAULT_EXTERNAL_ROOM_SENSOR_WRITE_INTERVAL,
    EXTERNAL_ROOM_SENSOR_AGGREGATION_AVERAGE,
    EXTERNAL_ROOM_SENSOR_AGGREGATION_MAX,
    EXTERNAL_ROOM_SENSOR_AGGREGATION_MIN,
)

_LOGGER = logging.getLogger(__name__)
_DIVERGENCE_WARNING_THRESHOLD = 1.0
_STORAGE_VERSION = 1


class ExternalRoomSensorSync:
    """Mirror selected Home Assistant temperatures into writable room-temperature registers."""

    def __init__(self, hass: HomeAssistant, entry: Any, coordinator: Any) -> None:
        """Initialize the sync helper."""
        self.hass = hass
        self.entry = entry
        self.coordinator = coordinator
        self._unsubscribers: list[Callable[[], None]] = []
        self._zone_status: dict[int, str] = {}
        self._store = Store(
            hass,
            _STORAGE_VERSION,
            f"{self.entry.domain}.{self.entry.entry_id}.external_room_sensor",
        )

    async def async_setup(self) -> None:
        """Attach listeners and push initial values for configured heating zones."""
        self.async_unload()
        await self._async_restore_zone_status()

        for zone, config in self._configured_sources().items():
            entity_ids = config[CONF_EXTERNAL_ROOM_SENSOR_ENTITY_IDS]
            register_key = f"zone{zone}_room_temp_measured"
            if register_key not in self.coordinator.register_map:
                _LOGGER.debug(
                    "Skipping external room sensor sync for zone %s: register missing",
                    zone,
                )
                continue

            self._unsubscribers.append(
                async_track_state_change_event(
                    self.hass,
                    entity_ids,
                    self._build_listener(zone, register_key, config),
                )
            )
            self._unsubscribers.append(
                async_track_time_interval(
                    self.hass,
                    self._build_periodic_listener(zone, register_key, config),
                    timedelta(seconds=config[CONF_EXTERNAL_ROOM_SENSOR_WRITE_INTERVAL]),
                )
            )
            self.hass.async_create_task(
                self._async_push_aggregate(
                    zone=zone,
                    register_key=register_key,
                    config=config,
                    reason="startup_recheck",
                    force_status_log=True,
                )
            )

    def async_unload(self) -> None:
        """Detach all state listeners."""
        while self._unsubscribers:
            self._unsubscribers.pop()()

    def _configured_sources(self) -> dict[int, dict[str, Any]]:
        """Return normalized zone configuration."""
        configured = self.entry.options.get(
            CONF_EXTERNAL_ROOM_SENSORS,
            self.entry.data.get(CONF_EXTERNAL_ROOM_SENSORS, {}),
        )
        if not isinstance(configured, dict):
            return {}

        normalized: dict[int, dict[str, Any]] = {}
        for key, zone_config in configured.items():
            try:
                zone = int(key)
            except (TypeError, ValueError):
                continue

            if isinstance(zone_config, str):
                zone_config = {
                    CONF_EXTERNAL_ROOM_SENSOR_ENTITY_IDS: [zone_config],
                    CONF_EXTERNAL_ROOM_SENSOR_AGGREGATION: EXTERNAL_ROOM_SENSOR_AGGREGATION_AVERAGE,
                }
            if not isinstance(zone_config, dict):
                continue

            raw_entity_ids = zone_config.get(CONF_EXTERNAL_ROOM_SENSOR_ENTITY_IDS, [])
            if isinstance(raw_entity_ids, str):
                raw_entity_ids = [raw_entity_ids]
            if not isinstance(raw_entity_ids, list):
                continue

            entity_ids = [
                entity_id.strip()
                for entity_id in raw_entity_ids
                if isinstance(entity_id, str) and entity_id.strip()
            ]
            if not entity_ids:
                continue

            aggregation = zone_config.get(
                CONF_EXTERNAL_ROOM_SENSOR_AGGREGATION,
                EXTERNAL_ROOM_SENSOR_AGGREGATION_AVERAGE,
            )
            if aggregation not in {
                EXTERNAL_ROOM_SENSOR_AGGREGATION_AVERAGE,
                EXTERNAL_ROOM_SENSOR_AGGREGATION_MIN,
                EXTERNAL_ROOM_SENSOR_AGGREGATION_MAX,
            }:
                aggregation = EXTERNAL_ROOM_SENSOR_AGGREGATION_AVERAGE

            normalized[zone] = {
                CONF_EXTERNAL_ROOM_SENSOR_ENTITY_IDS: entity_ids,
                CONF_EXTERNAL_ROOM_SENSOR_AGGREGATION: aggregation,
                CONF_EXTERNAL_ROOM_SENSOR_WRITE_INTERVAL: int(
                    zone_config.get(
                        CONF_EXTERNAL_ROOM_SENSOR_WRITE_INTERVAL,
                        DEFAULT_EXTERNAL_ROOM_SENSOR_WRITE_INTERVAL,
                    )
                ),
                CONF_EXTERNAL_ROOM_SENSOR_TIMEOUT: int(
                    zone_config.get(
                        CONF_EXTERNAL_ROOM_SENSOR_TIMEOUT,
                        DEFAULT_EXTERNAL_ROOM_SENSOR_TIMEOUT,
                    )
                ),
            }

        return normalized

    def _build_listener(
        self, zone: int, register_key: str, config: dict[str, Any]
    ) -> Callable[[Event], None]:
        """Create a state-change callback for a zone/source configuration."""

        @callback
        def _listener(event: Event) -> None:
            if event.data.get("new_state") is None:
                return
            self.hass.async_create_task(
                self._async_push_aggregate(
                    zone=zone,
                    register_key=register_key,
                    config=config,
                    reason="state_changed",
                )
            )

        return _listener

    def _build_periodic_listener(
        self, zone: int, register_key: str, config: dict[str, Any]
    ) -> Callable[[Any], None]:
        """Create a periodic callback for a zone/source configuration."""

        @callback
        def _listener(_: Any) -> None:
            self.hass.async_create_task(
                self._async_push_aggregate(
                    zone=zone,
                    register_key=register_key,
                    config=config,
                    reason="interval",
                )
            )

        return _listener

    def _collect_samples(
        self, entity_ids: list[str], zone: int, timeout_seconds: int
    ) -> list[dict[str, Any]]:
        """Collect fresh numeric temperatures from the configured source entities."""
        samples: list[dict[str, Any]] = []
        now = dt_util.utcnow()
        for entity_id in entity_ids:
            state = self.hass.states.get(entity_id)
            if state is None:
                continue
            raw_state = state.state
            if raw_state in {STATE_UNKNOWN, STATE_UNAVAILABLE, ""}:
                continue
            try:
                value = float(raw_state)
            except (TypeError, ValueError):
                _LOGGER.debug(
                    "Ignoring non-numeric external room sensor state for zone %s from %s: %s",
                    zone,
                    entity_id,
                    raw_state,
                )
                continue
            age_seconds = (now - state.last_updated).total_seconds()
            if age_seconds > timeout_seconds:
                continue
            samples.append(
                {
                    "entity_id": entity_id,
                    "value": value,
                    "last_changed": state.last_changed,
                    "last_updated": state.last_updated,
                    "age_seconds": age_seconds,
                }
            )
        return samples

    @staticmethod
    def _aggregate(samples: list[dict[str, Any]], aggregation: str) -> tuple[float, str | None]:
        """Aggregate multiple sensor values according to the selected strategy."""
        if aggregation == EXTERNAL_ROOM_SENSOR_AGGREGATION_MIN:
            winner = min(samples, key=lambda sample: sample["value"])
            return winner["value"], winner["entity_id"]
        if aggregation == EXTERNAL_ROOM_SENSOR_AGGREGATION_MAX:
            winner = max(samples, key=lambda sample: sample["value"])
            return winner["value"], winner["entity_id"]
        return fmean(sample["value"] for sample in samples), None

    def _invalid_reason(
        self,
        zone: int,
        samples: list[dict[str, Any]],
        aggregation: str,
        timeout_seconds: int,
    ) -> str | None:
        """Return an invalidation reason when the aggregate should not be written."""
        if not samples:
            return "timeout_or_all_sources_invalid"

        if aggregation not in {
            EXTERNAL_ROOM_SENSOR_AGGREGATION_MIN,
            EXTERNAL_ROOM_SENSOR_AGGREGATION_MAX,
        }:
            return None

        if len(samples) < 2:
            return None

        values = [sample["value"] for sample in samples]
        spread = max(values) - min(values)
        if spread < _DIVERGENCE_WARNING_THRESHOLD:
            return None

        winner = (
            min(samples, key=lambda sample: sample["value"])
            if aggregation == EXTERNAL_ROOM_SENSOR_AGGREGATION_MIN
            else max(samples, key=lambda sample: sample["value"])
        )
        stale_winner_seconds = (
            dt_util.utcnow() - winner["last_changed"]
        ).total_seconds()
        if stale_winner_seconds >= max(timeout_seconds / 2, 1800):
            return (
                f"aggregation_suspect:{winner['entity_id']}:"
                f"unchanged_for={int(stale_winner_seconds)}s:spread={spread:.2f}"
            )
        return None

    async def _async_restore_zone_status(self) -> None:
        """Restore the last known per-zone sync status from storage."""
        stored = await self._store.async_load()
        if not isinstance(stored, dict):
            return
        zone_status = stored.get("zone_status")
        if not isinstance(zone_status, dict):
            return
        restored: dict[int, str] = {}
        for key, value in zone_status.items():
            try:
                zone = int(key)
            except (TypeError, ValueError):
                continue
            if isinstance(value, str):
                restored[zone] = value
        self._zone_status = restored

    def _schedule_status_persist(self) -> None:
        """Persist the current zone status map in the background."""
        self.hass.async_create_task(
            self._store.async_save(
                {
                    "zone_status": {
                        str(zone): status for zone, status in self._zone_status.items()
                    }
                }
            )
        )

    def _set_zone_status(
        self,
        zone: int,
        status: str,
        log_message: str,
        level: str,
        *,
        force_log: bool = False,
    ) -> None:
        """Log only on status transitions for a zone."""
        previous = self._zone_status.get(zone)
        if previous == status and not force_log:
            return
        self._zone_status[zone] = status
        if previous != status:
            self._schedule_status_persist()
        getattr(_LOGGER, level)(log_message)

    async def _async_push_aggregate(
        self,
        *,
        zone: int,
        register_key: str,
        config: dict[str, Any],
        reason: str,
        force_status_log: bool = False,
    ) -> None:
        """Compute the aggregated source value and write it periodically to the zone register."""
        entity_ids = config[CONF_EXTERNAL_ROOM_SENSOR_ENTITY_IDS]
        aggregation = config[CONF_EXTERNAL_ROOM_SENSOR_AGGREGATION]
        timeout_seconds = int(config[CONF_EXTERNAL_ROOM_SENSOR_TIMEOUT])
        samples = self._collect_samples(entity_ids, zone, timeout_seconds)
        invalid_reason = self._invalid_reason(zone, samples, aggregation, timeout_seconds)
        if invalid_reason is not None:
            self._set_zone_status(
                zone,
                f"invalid:{invalid_reason}",
                (
                    "External room sensor sync paused for zone %s (%s). "
                    "No write to %s; IWR can fall back to its internal strategy."
                )
                % (zone, invalid_reason, register_key),
                "warning",
                force_log=force_status_log,
            )
            return

        value, _ = self._aggregate(samples, aggregation)
        value = round(value, 1)

        try:
            # Register 2129 (`zone3_room_temp_measured` on the verified BLW 12.1
            # reference installation) can quantize injected room temperatures
            # internally. During live verification, raw `1960` (19.6 °C) was
            # read back as raw `2000` (20.0 °C). Treat this as appliance
            # behavior, not as an integration-side write defect.
            await self.coordinator.async_write_register(register_key, value)
        except Exception:
            self._set_zone_status(
                zone,
                "write_error",
                (
                    "External room sensor sync write failed for zone %s -> %s. "
                    "Writes paused until the next successful cycle."
                )
                % (zone, register_key),
                "warning",
                force_log=force_status_log,
            )
            _LOGGER.exception(
                "Failed to sync external room sensors %s to %s (zone %s)",
                entity_ids,
                register_key,
                zone,
            )
            return

        self._set_zone_status(
            zone,
            "active",
            (
                "External room sensor sync active again for zone %s -> %s "
                "(aggregation=%s, sources=%s)"
            )
            % (zone, register_key, aggregation, entity_ids),
            "info",
            force_log=force_status_log,
        )
        _LOGGER.info(
            "External room sensor sync %s -> %s (zone %s, aggregation=%s, value=%s, reason=%s)",
            entity_ids,
            register_key,
            zone,
            aggregation,
            value,
            reason,
        )
