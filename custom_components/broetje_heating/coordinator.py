"""DataUpdateCoordinator for the Brötje Heatpump integration."""

from __future__ import annotations

import asyncio
import logging
import time
from datetime import date, timedelta
from typing import Any

from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    ALWAYS_PRESENT_SUBDEVICES,
    CONF_SCAN_INTERVAL,
    CONF_UNIT_ID,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_UNIT_ID,
    DOMAIN,
    EXCEPTION_CODE10_AUTO_DISABLE_THRESHOLD,
    EXCEPTION_CODE3_BACKOFF_SECONDS,
    EXCEPTION_CODE3_BACKOFF_THRESHOLD,
    MANUFACTURER,
    REG_HOLDING,
    REG_INPUT,
    SENTINEL_AUTO_DISABLE_THRESHOLD,
    SENTINEL_RETRY_INTERVAL_SECONDS,
    SUBDEV_BUFFER_TANK,
    SUBDEV_HYBRID,
    SUBDEV_SOLAR,
)
from .devices import CONF_DEVICE_TYPE, DEVICE_MODELS, DeviceType, get_device_config

_LOGGER = logging.getLogger(__name__)
_APPLIANCE_TIME_EPOCH = date(1984, 1, 1)
_MODBUS_EXCEPTION_NAMES: dict[int, str] = {
    1: "illegal_function",
    2: "illegal_data_address",
    3: "illegal_data_value",
    4: "slave_device_failure",
    5: "acknowledge",
    6: "slave_device_busy",
    8: "memory_parity_error",
    10: "gateway_path_unavailable",
    11: "gateway_target_no_response",
}
POLL_PROFILE_FAST = "fast"
POLL_PROFILE_NORMAL = "normal"
POLL_PROFILE_SLOW = "slow"
POLL_PROFILE_OFF = "off"
POLL_PROFILES: dict[str, int | None] = {
    POLL_PROFILE_FAST: 30,
    POLL_PROFILE_NORMAL: DEFAULT_SCAN_INTERVAL,
    POLL_PROFILE_SLOW: 600,
    POLL_PROFILE_OFF: None,
}
FAST_POLL_REGISTER_ADDRESSES: frozenset[int] = frozenset(
    {
        384,
        400,
        401,
        409,
        1612,
        1613,
        1619,
        1620,
        2128,
        2129,
        2131,
        2133,
    }
)
SLOW_POLL_REGISTER_ADDRESSES: frozenset[int] = frozenset({1177, 1178, 1179})
SLOW_POLL_REGISTER_RANGES: tuple[tuple[int, int], ...] = (
    (0, 199),
    (1700, 1799),
)


class BroetjeModbusCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for fetching data from Brötje Heatpump via Modbus."""

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        scan_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        self._poll_profiles = dict(POLL_PROFILES)
        self._poll_profiles[POLL_PROFILE_NORMAL] = scan_interval
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            config_entry=entry,
            update_interval=timedelta(seconds=self._coordinator_tick_seconds()),
        )
        self._host = entry.data[CONF_HOST]
        self._port = entry.data[CONF_PORT]
        self._unit_id = entry.data.get(CONF_UNIT_ID, DEFAULT_UNIT_ID)
        self._client: AsyncModbusTcpClient | None = None
        self._lock = asyncio.Lock()

        # Load device-specific configuration
        device_type_str = entry.data.get(CONF_DEVICE_TYPE, DeviceType.ISR.value)
        self._device_type = DeviceType(device_type_str)
        zones = entry.data.get("zones", [1])
        device_config = get_device_config(self._device_type, zones=zones)
        self.register_map: dict[str, Any] = device_config["register_map"]
        self.sensors: dict[str, Any] = device_config["sensors"]
        self.binary_sensors: dict[str, Any] = device_config["binary_sensors"]
        self.numbers: dict[str, Any] = device_config.get("numbers", {})
        self.selects: dict[str, Any] = device_config.get("selects", {})
        self.times: dict[str, Any] = device_config.get("times", {})
        self.climates: dict[str, Any] = device_config.get("climates", {})
        self.enum_maps: dict[str, dict[int, str]] = device_config["enum_maps"]
        self.entity_classification: dict[str, tuple[str | None, bool]] = (
            device_config.get("entity_classification", {})
        )
        self.last_read_details: dict[str, dict[str, Any]] = {}
        self._last_read_error_detail: dict[str, Any] | None = None
        self._sentinel_fail_counts: dict[str, int] = {}
        self._exception10_fail_counts: dict[str, int] = {}
        self._exception3_fail_counts: dict[str, int] = {}
        self._register_poll_state: dict[str, dict[str, Any]] = {}
        self._last_poll_monotonic: dict[str, float] = {}
        self._register_entities = self._build_register_entities()
        self._entity_registers = self._build_entity_registers()

        # Device info
        self.device_serial: str | None = None
        self.device_model: str = DEVICE_MODELS.get(self._device_type, "Heatpump")
        self.device_manufacturer: str = MANUFACTURER
        self.device_firmware: str | None = None

        # Sub-devices active for this installation; populated during _async_setup
        self.active_sub_devices: set[str] = set()

    def update_scan_interval(self, scan_interval: int) -> None:
        """Update the polling interval (called when options change)."""
        self._poll_profiles[POLL_PROFILE_NORMAL] = scan_interval
        self.update_interval = timedelta(seconds=self._coordinator_tick_seconds())
        _LOGGER.info("Scan interval updated to %d seconds", scan_interval)

    def _coordinator_tick_seconds(self) -> int:
        """Return the fastest enabled profile interval for coordinator wakeups."""
        return min(
            interval
            for interval in self._poll_profiles.values()
            if interval is not None
        )

    async def _async_setup(self) -> None:
        """Set up the coordinator (called during first refresh)."""
        await self._connect()
        await self._read_device_info()
        await self._detect_sub_devices()

    async def _connect(self) -> None:
        """Establish connection to the Modbus device."""
        if self._client is not None and self._client.connected:
            return

        self._client = AsyncModbusTcpClient(
            host=self._host,
            port=self._port,
        )

        if not await self._client.connect():
            raise UpdateFailed(f"Failed to connect to {self._host}:{self._port}")

        _LOGGER.debug("Connected to Modbus device at %s:%s", self._host, self._port)

    async def _disconnect(self) -> None:
        """Disconnect from the Modbus device."""
        if self._client is not None:
            self._client.close()
            self._client = None
            _LOGGER.debug("Disconnected from Modbus device")

    async def _read_device_info(self) -> None:
        """Read device identification information."""
        # TODO: Implement reading device info from Modbus registers
        # This will be populated once we have the register addresses from the PDF
        pass

    # Sentinel values that indicate a register/subsystem is not present.
    # 0xFF   (255)   — UINT8 / ENUM8 "no data" sentinel
    # 0xFFFF (65535) — UINT16 "no data" sentinel (also returned by some devices
    #                  for registers that exist in the spec but are not wired up)
    _DETECTION_SENTINELS: frozenset[int] = frozenset({0xFF, 0xFFFF})

    async def _detect_sub_devices(self) -> None:
        """Detect which optional sub-devices are present on this installation.

        Always-present sub-devices (boiler, service) are added unconditionally
        for IWR devices. Conditional sub-devices are detected by probing a
        characteristic register: a non-sentinel, non-zero response means the
        subsystem is present.
        """
        if self._device_type != DeviceType.IWR:
            return

        # Always-present sub-devices for IWR
        self.active_sub_devices = set(ALWAYS_PRESENT_SUBDEVICES)

        # Buffer Tank: reg 197 (UINT8) — value 1 means active; 0 means not active
        result = await self._read_registers(197, 1, REG_HOLDING)
        if result is not None and result[0] == 1:
            self.active_sub_devices.add(SUBDEV_BUFFER_TANK)
            _LOGGER.debug("Sub-device detected: Buffer Tank (reg 197 = %d)", result[0])

        # Solar: reg 8114 (ENUM8 solar boiler status) — present if not a sentinel value
        result = await self._read_registers(8114, 1, REG_HOLDING)
        if result is not None and result[0] not in self._DETECTION_SENTINELS:
            self.active_sub_devices.add(SUBDEV_SOLAR)
            _LOGGER.debug("Sub-device detected: Solar (reg 8114 = 0x%X)", result[0])

        # Hybrid: reg 9204 (UINT8 appliance status) — present if not a sentinel value
        result = await self._read_registers(9204, 1, REG_HOLDING)
        if result is not None and result[0] not in self._DETECTION_SENTINELS:
            self.active_sub_devices.add(SUBDEV_HYBRID)
            _LOGGER.debug("Sub-device detected: Hybrid (reg 9204 = 0x%X)", result[0])

        _LOGGER.info("Active sub-devices: %s", sorted(self.active_sub_devices))

    async def _read_registers(
        self,
        address: int,
        count: int,
        register_type: str,
    ) -> list[int] | None:
        """Read registers from the Modbus device."""
        self._last_read_error_detail = None
        async with self._lock:
            try:
                await self._connect()

                if register_type == REG_INPUT:
                    result = await self._client.read_input_registers(
                        address=address, count=count, device_id=self._unit_id
                    )
                elif register_type == REG_HOLDING:
                    result = await self._client.read_holding_registers(
                        address=address, count=count, device_id=self._unit_id
                    )
                else:
                    _LOGGER.error("Unknown register type: %s", register_type)
                    self._last_read_error_detail = {
                        "status": "read_error",
                        "error_kind": "unknown_register_type",
                        "register_type": register_type,
                    }
                    return None

                if result.isError():
                    error_detail: dict[str, Any] = {
                        "status": "read_error",
                        "error_kind": "modbus_exception_response",
                        "register_address": address,
                        "register_count": count,
                        "register_type": register_type,
                        "response": str(result),
                    }
                    if hasattr(result, "function_code"):
                        error_detail["function_code"] = result.function_code
                    if hasattr(result, "exception_code"):
                        error_detail["exception_code"] = result.exception_code
                        error_detail["exception_name"] = _MODBUS_EXCEPTION_NAMES.get(
                            result.exception_code, "unknown_exception"
                        )
                    self._last_read_error_detail = error_detail
                    _LOGGER.warning(
                        "Modbus error reading address %s: %s",
                        address,
                        result,
                    )
                    return None

                return list(result.registers)

            except ModbusException as err:
                self._last_read_error_detail = {
                    "status": "read_error",
                    "error_kind": "modbus_exception",
                    "register_address": address,
                    "register_count": count,
                    "register_type": register_type,
                    "message": str(err),
                }
                _LOGGER.error("Modbus exception: %s", err)
                await self._disconnect()
                return None

    def _get_needed_registers(self) -> set[str]:
        """Get the set of register keys needed by enabled entities.

        This checks the entity registry to determine which entities are enabled.
        If an entity is not yet in the registry (first refresh), it's assumed needed.
        Only entities explicitly disabled by the user are skipped.
        """
        entity_registry = er.async_get(self.hass)
        device_id = self.config_entry.unique_id or self.config_entry.entry_id

        needed_registers: set[str] = set()

        # Check sensors
        for sensor_key, sensor_config in self.sensors.items():
            unique_id = f"{device_id}_{sensor_key}"
            entity_id = entity_registry.async_get_entity_id(
                Platform.SENSOR, DOMAIN, unique_id
            )

            # If entity doesn't exist in registry yet, assume we need it
            if entity_id is None:
                needed_registers.add(sensor_config["register"])
                continue

            entry = entity_registry.async_get(entity_id)
            # If entity exists and is NOT disabled, we need this register
            if entry and not entry.disabled:
                needed_registers.add(sensor_config["register"])

        # Check binary sensors
        for sensor_key, sensor_config in self.binary_sensors.items():
            unique_id = f"{device_id}_{sensor_key}"
            entity_id = entity_registry.async_get_entity_id(
                Platform.BINARY_SENSOR, DOMAIN, unique_id
            )

            # If entity doesn't exist in registry yet, assume we need it
            if entity_id is None:
                needed_registers.add(sensor_config["register"])
                continue

            entry = entity_registry.async_get(entity_id)
            # If entity exists and is NOT disabled, we need this register
            if entry and not entry.disabled:
                needed_registers.add(sensor_config["register"])

        # Check number entities
        for entity_key, entity_config in self.numbers.items():
            unique_id = f"{device_id}_{entity_key}"
            entity_id = entity_registry.async_get_entity_id(
                Platform.NUMBER, DOMAIN, unique_id
            )

            if entity_id is None:
                needed_registers.add(entity_config["register"])
                continue

            entry = entity_registry.async_get(entity_id)
            if entry and not entry.disabled:
                needed_registers.add(entity_config["register"])

        # Check select entities
        for entity_key, entity_config in self.selects.items():
            unique_id = f"{device_id}_{entity_key}"
            entity_id = entity_registry.async_get_entity_id(
                Platform.SELECT, DOMAIN, unique_id
            )

            if entity_id is None:
                needed_registers.add(entity_config["register"])
                continue

            entry = entity_registry.async_get(entity_id)
            if entry and not entry.disabled:
                needed_registers.add(entity_config["register"])

        # Check time entities
        for entity_key, entity_config in self.times.items():
            unique_id = f"{device_id}_{entity_key}"
            entity_id = entity_registry.async_get_entity_id(
                Platform.TIME, DOMAIN, unique_id
            )

            if entity_id is None:
                needed_registers.add(entity_config["register"])
                continue

            entry = entity_registry.async_get(entity_id)
            if entry and not entry.disabled:
                needed_registers.add(entity_config["register"])

        # Check climate entities — each uses multiple registers
        for entity_key, climate_config in self.climates.items():
            unique_id = f"{device_id}_{entity_key}"
            entity_id = entity_registry.async_get_entity_id(
                Platform.CLIMATE, DOMAIN, unique_id
            )

            climate_registers = {
                climate_config["temperature_register"],
                climate_config["setpoint_register"],
                climate_config["control_mode_register"],
                climate_config["heating_mode_register"],
            }

            if entity_id is None:
                needed_registers.update(climate_registers)
                continue

            entry = entity_registry.async_get(entity_id)
            if entry and not entry.disabled:
                needed_registers.update(climate_registers)

        filtered_registers: set[str] = set()
        skipped_registers: set[str] = set()
        now_monotonic = time.monotonic()

        for register_key in needed_registers:
            state = self._register_poll_state.get(register_key)
            if state is None:
                filtered_registers.add(register_key)
                continue

            mode = state.get("mode")
            retry_at = state.get("retry_at_monotonic")

            if mode == "sentinel_permanent":
                skipped_registers.add(register_key)
                continue

            if mode == "exception10_permanent":
                skipped_registers.add(register_key)
                continue

            if mode in {"sentinel_temp", "exception3_backoff"}:
                if retry_at is not None and now_monotonic < retry_at:
                    skipped_registers.add(register_key)
                    continue

                state["reprobe_active"] = mode == "sentinel_temp"
                state["reprobe_attempted"] = mode == "sentinel_temp"
                filtered_registers.add(register_key)
                continue

            filtered_registers.add(register_key)

        for register_key in skipped_registers:
            self.last_read_details[register_key] = self._build_disabled_detail(register_key)

        return self._get_due_registers(filtered_registers)

    def _resolve_poll_profile(self, register_key: str) -> str:
        """Return the polling profile for a register."""
        state = self._register_poll_state.get(register_key)
        if state is not None:
            mode = state.get("mode")
            if mode in {"sentinel_permanent", "exception10_permanent"}:
                return POLL_PROFILE_OFF
            if mode == "exception3_backoff":
                return POLL_PROFILE_SLOW

        config = self.register_map.get(register_key, {})
        profile = config.get("poll_profile", POLL_PROFILE_NORMAL)
        if (
            profile == POLL_PROFILE_NORMAL
            and config.get("address") in FAST_POLL_REGISTER_ADDRESSES
        ):
            profile = POLL_PROFILE_FAST
        if profile == POLL_PROFILE_NORMAL and self._is_static_slow_register(config):
            profile = POLL_PROFILE_SLOW
        if profile == POLL_PROFILE_NORMAL and self._is_diagnostic_register(
            register_key
        ):
            profile = POLL_PROFILE_SLOW
        if profile not in self._poll_profiles:
            _LOGGER.warning(
                "Unknown poll profile %s for register %s; using normal",
                profile,
                register_key,
            )
            return POLL_PROFILE_NORMAL
        return profile

    @staticmethod
    def _is_static_slow_register(config: dict[str, Any]) -> bool:
        """Return true for static register ranges that do not need fast polling."""
        address = config.get("address")
        if not isinstance(address, int):
            return False
        if address in SLOW_POLL_REGISTER_ADDRESSES:
            return True
        return any(
            start_address <= address <= end_address
            for start_address, end_address in SLOW_POLL_REGISTER_RANGES
        )

    def _is_diagnostic_register(self, register_key: str) -> bool:
        """Return true if all entities using a register are diagnostic."""
        entity_keys = self._register_entities.get(register_key, [])
        if not entity_keys:
            return False

        for entity_key in entity_keys:
            category, _enabled = self.entity_classification.get(entity_key, (None, True))
            if category != "diagnostic":
                return False
        return True

    def _get_due_registers(self, register_keys: set[str]) -> set[str]:
        """Filter registers to those due for this coordinator tick."""
        due_registers: set[str] = set()
        now_monotonic = time.monotonic()

        for register_key in register_keys:
            profile = self._resolve_poll_profile(register_key)
            interval = self._poll_profiles[profile]
            if interval is None:
                self.last_read_details[register_key] = self._build_disabled_detail(
                    register_key
                )
                continue

            last_poll = self._last_poll_monotonic.get(register_key)
            if last_poll is not None and now_monotonic - last_poll < interval:
                continue

            due_registers.add(register_key)
            self._last_poll_monotonic[register_key] = now_monotonic

        return due_registers

    def _build_register_entities(self) -> dict[str, list[str]]:
        """Map register keys to the entity keys that depend on them."""
        register_entities: dict[str, list[str]] = {}

        def add(register_key: str, entity_key: str) -> None:
            register_entities.setdefault(register_key, []).append(entity_key)

        for entity_key, sensor_config in self.sensors.items():
            add(sensor_config["register"], entity_key)

        for entity_key, sensor_config in self.binary_sensors.items():
            add(sensor_config["register"], entity_key)

        for entity_key, entity_config in self.numbers.items():
            add(entity_config["register"], entity_key)

        for entity_key, entity_config in self.selects.items():
            add(entity_config["register"], entity_key)

        for entity_key, entity_config in self.times.items():
            add(entity_config["register"], entity_key)

        for entity_key, climate_config in self.climates.items():
            add(climate_config["temperature_register"], entity_key)
            add(climate_config["setpoint_register"], entity_key)
            add(climate_config["control_mode_register"], entity_key)
            add(climate_config["heating_mode_register"], entity_key)

        return register_entities

    def _build_entity_registers(self) -> dict[str, set[str]]:
        """Map entity keys to the register keys they depend on."""
        entity_registers: dict[str, set[str]] = {}
        for register_key, entity_keys in self._register_entities.items():
            for entity_key in entity_keys:
                entity_registers.setdefault(entity_key, set()).add(register_key)
        return entity_registers

    def is_register_permanently_disabled(self, register_key: str) -> bool:
        """Return true if a register is permanently auto-disabled."""
        state = self._register_poll_state.get(register_key, {})
        return state.get("mode") in {
            "sentinel_permanent",
            "exception10_permanent",
        }

    def is_entity_permanently_disabled(self, entity_key: str) -> bool:
        """Return true if any register backing an entity is permanently disabled."""
        register_keys = self._entity_registers.get(entity_key, set())
        return any(
            self.is_register_permanently_disabled(register_key)
            for register_key in register_keys
        )

    def sync_permanently_disabled_registry_entities(self) -> int:
        """Disable registry entries for permanently auto-disabled registers."""
        disabled = 0
        for register_key in self._register_entities:
            if not self.is_register_permanently_disabled(register_key):
                continue
            disabled += self._disable_registry_entities_for_register(register_key)
        return disabled

    def _disable_registry_entities_for_register(self, register_key: str) -> int:
        """Disable all registry entries backed by a permanently disabled register."""
        entity_keys = self._register_entities.get(register_key, [])
        if not entity_keys:
            return 0

        entity_registry = er.async_get(self.hass)
        unique_root = self.config_entry.unique_id or self.config_entry.entry_id
        disabled = 0

        for registry_entry in er.async_entries_for_config_entry(
            entity_registry, self.config_entry.entry_id
        ):
            if registry_entry.platform != DOMAIN:
                continue
            if not registry_entry.unique_id.startswith(f"{unique_root}_"):
                continue

            entity_key = registry_entry.unique_id[len(unique_root) + 1 :]
            if entity_key not in entity_keys:
                continue
            if registry_entry.disabled_by == er.RegistryEntryDisabler.INTEGRATION:
                continue
            if registry_entry.disabled_by is not None:
                continue

            entity_registry.async_update_entity(
                registry_entry.entity_id,
                disabled_by=er.RegistryEntryDisabler.INTEGRATION,
            )
            disabled += 1
            _LOGGER.warning(
                "Disabled entity registry entry %s because register %s entered %s",
                registry_entry.entity_id,
                register_key,
                self._register_poll_state.get(register_key, {}).get("mode"),
            )

        return disabled

    def _describe_register(self, register_key: str) -> tuple[int | None, str]:
        """Return register address and related entity keys for logging."""
        reg_config = self.register_map.get(register_key, {})
        address = reg_config.get("address")
        entity_keys = ", ".join(self._register_entities.get(register_key, [register_key]))
        return address, entity_keys

    def _log_register_auto_disable(
        self,
        register_key: str,
        *,
        reason: str,
        state: str,
        count: int,
        retry_after_seconds: int | None = None,
    ) -> None:
        """Write a warning for an automatic register state change."""
        address, entity_keys = self._describe_register(register_key)
        retry_text = ""
        if retry_after_seconds is not None:
            retry_text = f", retry_after={retry_after_seconds}s"
        _LOGGER.warning(
            "Auto-disabling register %s (address=%s, entities=%s): reason=%s, state=%s, count=%d%s",
            register_key,
            address,
            entity_keys,
            reason,
            state,
            count,
            retry_text,
        )

    def _build_disabled_detail(self, register_key: str) -> dict[str, Any]:
        """Expose skipped/disabled register state as read detail."""
        state = self._register_poll_state.get(register_key, {})
        reg_config = self.register_map.get(register_key, {})
        detail: dict[str, Any] = {
            "status": state.get("detail_status", "auto_disabled"),
            "error_kind": state.get("reason", "auto_disabled"),
            "register_address": reg_config.get("address"),
            "register_type": reg_config.get("type"),
        }
        if entity_keys := self._register_entities.get(register_key):
            detail["entity_keys"] = list(entity_keys)
        detail["sentinel_fail_count"] = self._sentinel_fail_counts.get(register_key, 0)
        detail["exception10_fail_count"] = self._exception10_fail_counts.get(
            register_key, 0
        )
        detail["exception3_fail_count"] = self._exception3_fail_counts.get(
            register_key, 0
        )
        if poll_mode := state.get("mode"):
            detail["poll_mode"] = poll_mode
        detail["poll_profile"] = self._resolve_poll_profile(register_key)
        if exception_code := state.get("exception_code"):
            detail["exception_code"] = exception_code
            detail["exception_name"] = _MODBUS_EXCEPTION_NAMES.get(
                exception_code, "unknown_exception"
            )
        if retry_after_seconds := state.get("retry_after_seconds"):
            detail["retry_after_seconds"] = retry_after_seconds
        return detail

    def _apply_register_poll_state_to_detail(
        self,
        register_key: str,
        detail: dict[str, Any],
    ) -> dict[str, Any]:
        """Overlay auto-disable state onto a read detail when applicable."""
        state = self._register_poll_state.get(register_key)
        if state is None:
            return detail
        if state.get("mode") not in {
            "sentinel_temp",
            "sentinel_permanent",
            "exception10_permanent",
            "exception3_backoff",
        }:
            return detail
        merged = dict(detail)
        merged.update(self._build_disabled_detail(register_key))
        return merged

    def _annotate_runtime_detail(
        self,
        register_key: str,
        detail: dict[str, Any],
    ) -> dict[str, Any]:
        """Attach live counter/state info to any detail payload."""
        merged = dict(detail)
        merged["sentinel_fail_count"] = self._sentinel_fail_counts.get(register_key, 0)
        merged["exception10_fail_count"] = self._exception10_fail_counts.get(
            register_key, 0
        )
        merged["exception3_fail_count"] = self._exception3_fail_counts.get(
            register_key, 0
        )
        if state := self._register_poll_state.get(register_key):
            if poll_mode := state.get("mode"):
                merged["poll_mode"] = poll_mode
            if retry_after_seconds := state.get("retry_after_seconds"):
                merged["retry_after_seconds"] = retry_after_seconds
        merged["poll_profile"] = self._resolve_poll_profile(register_key)
        return merged

    def _clear_register_poll_state(self, register_key: str) -> None:
        """Reset failure counters and temp state after a healthy read."""
        self._sentinel_fail_counts.pop(register_key, None)
        self._exception10_fail_counts.pop(register_key, None)
        self._exception3_fail_counts.pop(register_key, None)
        self._register_poll_state.pop(register_key, None)

    def _mark_register_sentinel_disabled(
        self,
        register_key: str,
        *,
        permanent: bool,
    ) -> None:
        """Disable a register after repeated 0xFFFF sentinel reads."""
        count = self._sentinel_fail_counts.get(register_key, 0)
        previous_mode = self._register_poll_state.get(register_key, {}).get("mode")
        state = {
            "mode": "sentinel_permanent" if permanent else "sentinel_temp",
            "reason": "sentinel_0xFFFF",
            "detail_status": (
                "auto_disabled_sentinel_permanent"
                if permanent
                else "auto_disabled_sentinel_retry_pending"
            ),
            "retry_after_seconds": SENTINEL_RETRY_INTERVAL_SECONDS,
            "reprobe_active": False,
            "reprobe_attempted": permanent,
        }
        if not permanent:
            state["retry_at_monotonic"] = time.monotonic() + SENTINEL_RETRY_INTERVAL_SECONDS
        self._register_poll_state[register_key] = state
        self._log_register_auto_disable(
            register_key,
            reason="sentinel_0xFFFF",
            state=state["mode"],
            count=count,
            retry_after_seconds=None if permanent else SENTINEL_RETRY_INTERVAL_SECONDS,
        )
        if permanent and previous_mode != "sentinel_permanent":
            self._disable_registry_entities_for_register(register_key)

    def _mark_register_exception10_disabled(self, register_key: str) -> None:
        """Disable a register after repeated exception_code=10 responses."""
        previous_mode = self._register_poll_state.get(register_key, {}).get("mode")
        count = self._exception10_fail_counts.get(register_key, 0)
        self._register_poll_state[register_key] = {
            "mode": "exception10_permanent",
            "reason": "exception_code_10",
            "detail_status": "auto_disabled_exception_code_10_permanent",
            "exception_code": 10,
        }
        self._log_register_auto_disable(
            register_key,
            reason="exception_code_10",
            state="exception10_permanent",
            count=count,
        )
        if previous_mode != "exception10_permanent":
            self._disable_registry_entities_for_register(register_key)

    def _mark_register_exception3_backoff(self, register_key: str) -> None:
        """Temporarily reduce polling frequency for exception_code=3 registers."""
        count = self._exception3_fail_counts.get(register_key, 0)
        self._register_poll_state[register_key] = {
            "mode": "exception3_backoff",
            "reason": "exception_code_3",
            "detail_status": "auto_disabled_exception_code_3_backoff",
            "exception_code": 3,
            "retry_at_monotonic": time.monotonic() + EXCEPTION_CODE3_BACKOFF_SECONDS,
            "retry_after_seconds": EXCEPTION_CODE3_BACKOFF_SECONDS,
            "reprobe_active": False,
            "reprobe_attempted": False,
        }
        self._log_register_auto_disable(
            register_key,
            reason="exception_code_3",
            state="exception3_backoff",
            count=count,
            retry_after_seconds=EXCEPTION_CODE3_BACKOFF_SECONDS,
        )

    def _handle_successful_register_read(
        self,
        register_key: str,
        registers: list[int],
        config: dict[str, Any],
    ) -> None:
        """Update register health state after a successful protocol read."""
        sentinel_detected = self._is_sentinel_value(
            registers, config.get("data_type", "int16")
        )
        self._exception10_fail_counts.pop(register_key, None)
        self._exception3_fail_counts.pop(register_key, None)

        state = self._register_poll_state.get(register_key)
        reprobe_active = bool(state and state.get("reprobe_active"))

        if sentinel_detected:
            self._sentinel_fail_counts[register_key] = (
                self._sentinel_fail_counts.get(register_key, 0) + 1
            )
            count = self._sentinel_fail_counts[register_key]
            if reprobe_active:
                self._mark_register_sentinel_disabled(register_key, permanent=True)
            elif count >= SENTINEL_AUTO_DISABLE_THRESHOLD:
                self._mark_register_sentinel_disabled(register_key, permanent=False)
            return

        self._sentinel_fail_counts.pop(register_key, None)
        if state is not None and state.get("mode") in {"sentinel_temp", "exception3_backoff"}:
            self._register_poll_state.pop(register_key, None)

    def _handle_failed_register_read(
        self,
        register_key: str,
        detail: dict[str, Any],
    ) -> None:
        """Update register health state after a failed protocol read."""
        self._sentinel_fail_counts.pop(register_key, None)
        exception_code = detail.get("exception_code")

        if exception_code == 10:
            self._exception3_fail_counts.pop(register_key, None)
            self._exception10_fail_counts[register_key] = (
                self._exception10_fail_counts.get(register_key, 0) + 1
            )
            if (
                self._exception10_fail_counts[register_key]
                >= EXCEPTION_CODE10_AUTO_DISABLE_THRESHOLD
            ):
                self._mark_register_exception10_disabled(register_key)
            return

        self._exception10_fail_counts.pop(register_key, None)

        if exception_code == 3:
            self._exception3_fail_counts[register_key] = (
                self._exception3_fail_counts.get(register_key, 0) + 1
            )
            if (
                self._exception3_fail_counts[register_key]
                >= EXCEPTION_CODE3_BACKOFF_THRESHOLD
            ):
                self._mark_register_exception3_backoff(register_key)
            return

        self._exception3_fail_counts.pop(register_key, None)

    def _group_registers_for_batch_read(
        self, register_keys: set[str]
    ) -> list[dict[str, Any]]:
        """Group registers into batches for efficient reading.

        Groups consecutive or near-consecutive registers to minimize
        the number of Modbus read operations. Reading a few unused
        registers between needed ones is much cheaper than making
        separate Modbus requests.
        """
        if not register_keys:
            return []

        # Modbus limits: max 125 registers per read, we use 100 for safety
        MAX_BATCH_SIZE = 100
        # Max gap between registers to still batch them together.
        # Must be 0 (truly consecutive only) because the Brötje device has gaps
        # in its register map (e.g., 24594 exists, 24595 doesn't, 24596 exists).
        # Reading non-existent addresses causes batch read failures.
        # Note: With the formula (addr <= end + MAX_GAP + 1), MAX_GAP=0 means
        # only consecutive addresses (gap of 1) are batched.
        MAX_GAP = 0

        # Build list of register info and sort by type, then address
        registers: list[dict[str, Any]] = []
        for key in register_keys:
            config = self.register_map.get(key)
            if config is None:
                _LOGGER.warning("Skipping unknown register key in batch read: %s", key)
                continue
            registers.append(
                {
                    "key": key,
                    "address": config["address"],
                    "count": config.get("count", 1),
                    "type": config["type"],
                    "config": config,
                }
            )

        # Sort by register type first (to group holding/input), then by address
        registers.sort(key=lambda x: (x["type"], x["address"]))

        # Group into batches
        batches: list[dict[str, Any]] = []
        current_batch: dict[str, Any] | None = None

        for reg in registers:
            reg_end = reg["address"] + reg["count"] - 1

            if current_batch is None:
                # Start new batch
                current_batch = {
                    "type": reg["type"],
                    "start_address": reg["address"],
                    "end_address": reg_end,
                    "registers": [reg],
                }
            elif (
                reg["type"] == current_batch["type"]
                and reg["address"] <= current_batch["end_address"] + MAX_GAP + 1
                and (reg_end - current_batch["start_address"] + 1) <= MAX_BATCH_SIZE
            ):
                # Add to current batch
                current_batch["registers"].append(reg)
                current_batch["end_address"] = max(
                    current_batch["end_address"], reg_end
                )
            else:
                # Finish current batch and start new one
                batches.append(current_batch)
                current_batch = {
                    "type": reg["type"],
                    "start_address": reg["address"],
                    "end_address": reg_end,
                    "registers": [reg],
                }

        if current_batch:
            batches.append(current_batch)

        return batches

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the Modbus device."""
        data: dict[str, Any] = dict(self.data or {})
        previous_read_details = self.last_read_details
        self.last_read_details = dict(previous_read_details)

        # Get only the registers needed by enabled entities
        needed_registers = self._get_needed_registers()

        if not needed_registers:
            _LOGGER.debug("No enabled entities, skipping Modbus read")
            return data

        # Group registers into batches for efficient reading
        batches = self._group_registers_for_batch_read(needed_registers)

        _LOGGER.debug(
            "Reading %d registers in %d batch(es) for enabled entities",
            len(needed_registers),
            len(batches),
        )

        # Disconnect before starting to clear any stale data in the buffer
        # This prevents transaction ID mismatch errors from leftover responses
        await self._disconnect()

        try:
            async with asyncio.timeout(30):
                for batch in batches:
                    start_addr = batch["start_address"]
                    count = batch["end_address"] - start_addr + 1

                    _LOGGER.debug(
                        "Batch read: type=%s, address=%d, count=%d (%d registers)",
                        batch["type"],
                        start_addr,
                        count,
                        len(batch["registers"]),
                    )

                    result = await self._read_registers(
                        start_addr, count, batch["type"]
                    )

                    if result is not None:
                        # Extract individual register values from batch response
                        for reg in batch["registers"]:
                            offset = reg["address"] - start_addr
                            reg_count = reg["count"]
                            reg_values = result[offset : offset + reg_count]

                            if len(reg_values) == reg_count:
                                processed = self._process_register_value(
                                    reg_values, reg["config"]
                                )
                                self._handle_successful_register_read(
                                    reg["key"], reg_values, reg["config"]
                                )
                                data[reg["key"]] = processed
                                detail = self._build_read_detail(
                                    reg_values,
                                    reg["config"],
                                    processed,
                                )
                                detail = self._annotate_runtime_detail(
                                    reg["key"], detail
                                )
                                self.last_read_details[reg["key"]] = (
                                    self._apply_register_poll_state_to_detail(
                                        reg["key"], detail
                                    )
                                )
                            else:
                                _LOGGER.warning(
                                    "Incomplete data for register %s at address %d; retrying individually",
                                    reg["key"],
                                    reg["address"],
                                )
                                reg_result = await self._read_registers(
                                    reg["address"], reg["count"], reg["type"]
                                )
                                if reg_result is None:
                                    data[reg["key"]] = None
                                    detail = self._consume_last_read_error_detail()
                                    detail["status"] = "incomplete_batch_retry_failed"
                                    self._handle_failed_register_read(
                                        reg["key"], detail
                                    )
                                    detail = self._annotate_runtime_detail(
                                        reg["key"], detail
                                    )
                                    self.last_read_details[reg["key"]] = (
                                        self._apply_register_poll_state_to_detail(
                                            reg["key"], detail
                                        )
                                    )
                                else:
                                    processed = self._process_register_value(
                                        reg_result, reg["config"]
                                    )
                                    self._handle_successful_register_read(
                                        reg["key"], reg_result, reg["config"]
                                    )
                                    data[reg["key"]] = processed
                                    detail = self._build_read_detail(
                                        reg_result,
                                        reg["config"],
                                        processed,
                                    )
                                    detail["status_source"] = (
                                        "single_retry_after_incomplete_batch"
                                    )
                                    detail = self._annotate_runtime_detail(
                                        reg["key"], detail
                                    )
                                    self.last_read_details[reg["key"]] = (
                                        self._apply_register_poll_state_to_detail(
                                            reg["key"], detail
                                        )
                                    )
                    else:
                        # Retry per register so one bad address does not blank
                        # the entire contiguous block.
                        for reg in batch["registers"]:
                            reg_result = await self._read_registers(
                                reg["address"], reg["count"], reg["type"]
                            )
                            if reg_result is None:
                                data[reg["key"]] = None
                                detail = self._consume_last_read_error_detail()
                                self._handle_failed_register_read(reg["key"], detail)
                                detail = self._annotate_runtime_detail(
                                    reg["key"], detail
                                )
                                self.last_read_details[reg["key"]] = (
                                    self._apply_register_poll_state_to_detail(
                                        reg["key"], detail
                                    )
                                )
                            else:
                                processed = self._process_register_value(
                                    reg_result, reg["config"]
                                )
                                self._handle_successful_register_read(
                                    reg["key"], reg_result, reg["config"]
                                )
                                data[reg["key"]] = processed
                                detail = self._build_read_detail(
                                    reg_result,
                                    reg["config"],
                                    processed,
                                )
                                detail = self._annotate_runtime_detail(
                                    reg["key"], detail
                                )
                                self.last_read_details[reg["key"]] = (
                                    self._apply_register_poll_state_to_detail(
                                        reg["key"], detail
                                    )
                                )

        except TimeoutError as err:
            raise UpdateFailed("Timeout communicating with device") from err
        except ModbusException as err:
            raise UpdateFailed(f"Modbus error: {err}") from err

        return data

    # Standard Modbus sentinel values indicating "not available" / "no data".
    # These are checked against the raw decoded value BEFORE scaling.
    _SENTINEL_VALUES: dict[str, set[int]] = {
        "uint8": {0xFFFF},
        "enum8": {0xFFFF},
        # GTW-08 returns both 0xFFFF and 0x8000 for signed "no data" registers.
        "int16": {-1, -32768},
        "uint16": {0xFFFF},  # 65535
        "int32": {-1},  # 0xFFFFFFFF signed
        "uint32": {0xFFFFFFFF},  # 4294967295
    }

    @staticmethod
    def _format_raw_registers(registers: list[int]) -> list[str]:
        """Return raw register words as zero-padded hex strings."""
        return [f"0x{value:04X}" for value in registers]

    def _consume_last_read_error_detail(self) -> dict[str, Any]:
        """Return the latest protocol/transport error for one register read."""
        detail = dict(self._last_read_error_detail or {"status": "read_error"})
        self._last_read_error_detail = None
        return detail

    def _build_read_detail(
        self,
        registers: list[int],
        config: dict[str, Any],
        processed_value: Any,
    ) -> dict[str, Any]:
        """Build per-register read diagnostics for the last refresh."""
        detail: dict[str, Any] = {
            "raw_registers": list(registers),
            "raw_registers_hex": self._format_raw_registers(registers),
        }

        data_type = config.get("data_type", "int16")

        if processed_value is None:
            if self._is_sentinel_value(registers, data_type):
                detail["status"] = "sentinel_no_data"
            else:
                detail["status"] = "invalid_value"
            return detail

        detail["status"] = "ok"
        return detail

    def _is_sentinel_value(self, registers: list[int], data_type: str) -> bool:
        """Return True if the raw register payload matches a known no-data sentinel."""
        if data_type in {"uint8", "enum8"}:
            return registers[0] in self._SENTINEL_VALUES.get(data_type, ())

        if data_type == "int16":
            value = registers[0]
            if value >= 32768:
                value -= 65536
            return value in self._SENTINEL_VALUES.get("int16", ())

        if data_type == "uint16":
            return registers[0] in self._SENTINEL_VALUES.get("uint16", ())

        if data_type == "int32":
            value = (registers[0] << 16) | registers[1]
            if value >= 2147483648:
                value -= 4294967296
            return value in self._SENTINEL_VALUES.get("int32", ())

        if data_type == "uint32":
            value = (registers[0] << 16) | registers[1]
            return value in self._SENTINEL_VALUES.get("uint32", ())

        return False

    def _process_register_value(
        self,
        registers: list[int],
        config: dict[str, Any],
    ) -> Any:
        """Process raw register values based on configuration."""
        data_type = config.get("data_type", "int16")
        scale = config.get("scale", 1.0)
        bit = config.get("bit")

        if data_type == "bool":
            value = registers[0]
            if bit is not None:
                return bool(value & (1 << bit))
            return bool(value)

        if data_type in {"uint8", "enum8"}:
            raw_word = registers[0]
            if raw_word in self._SENTINEL_VALUES.get(data_type, ()):
                return None
            return (raw_word & 0x00FF) * scale

        if data_type == "int16":
            value = registers[0]
            # Convert to signed if necessary
            if value >= 32768:
                value -= 65536
            if value in self._SENTINEL_VALUES.get("int16", ()):
                return None
            return value * scale

        if data_type == "uint16":
            value = registers[0]
            if value in self._SENTINEL_VALUES.get("uint16", ()):
                return None
            return value * scale

        if data_type == "int32":
            value = (registers[0] << 16) | registers[1]
            if value >= 2147483648:
                value -= 4294967296
            if value in self._SENTINEL_VALUES.get("int32", ()):
                return None
            return value * scale

        if data_type == "uint32":
            value = (registers[0] << 16) | registers[1]
            if value in self._SENTINEL_VALUES.get("uint32", ()):
                return None
            return value * scale

        if data_type == "string":
            # Decode registers as ASCII string
            chars = []
            for reg in registers:
                chars.append(chr((reg >> 8) & 0xFF))
                chars.append(chr(reg & 0xFF))
            return "".join(chars).rstrip("\x00").strip()

        if data_type == "appliance_time":
            raw = b"".join(reg.to_bytes(2, "big") for reg in registers)
            if len(raw) != 6:
                return None

            millis_since_midnight = int.from_bytes(raw[:4], "little")
            days_since_epoch = int.from_bytes(raw[4:], "little")

            total_seconds, milliseconds = divmod(millis_since_midnight, 1000)
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            if hours >= 24 or minutes >= 60 or seconds >= 60:
                return None

            appliance_date = _APPLIANCE_TIME_EPOCH + timedelta(days=days_since_epoch)
            return (
                f"{appliance_date.isoformat()} "
                f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
            )

        return registers[0] * scale

    @staticmethod
    def _encode_register_value(value: int, data_type: str) -> list[int]:
        """Encode a raw integer value into Modbus register word(s)."""
        if data_type in ("uint8", "uint16"):
            return [value & 0xFFFF]

        if data_type == "int16":
            if value < 0:
                value += 65536
            return [value & 0xFFFF]

        if data_type == "uint32":
            return [(value >> 16) & 0xFFFF, value & 0xFFFF]

        if data_type == "int32":
            if value < 0:
                value += 4294967296
            return [(value >> 16) & 0xFFFF, value & 0xFFFF]

        return [value & 0xFFFF]

    async def async_write_register(self, register_key: str, value: float | int) -> None:
        """Write a value to a writable register.

        Validates the writable flag and bounds, applies reverse scaling,
        encodes to register words, writes via Modbus, and verifies with
        a read-back.
        """
        if register_key not in self.register_map:
            raise HomeAssistantError(f"Unknown register: {register_key}")

        config = self.register_map[register_key]

        if not config.get("writable"):
            raise HomeAssistantError(f"Register {register_key} is not writable")

        if config["type"] != REG_HOLDING:
            raise HomeAssistantError(
                f"Register {register_key} is not a holding register"
            )

        # Bounds validation (min/max are in user-facing scaled units)
        min_val = config.get("min")
        max_val = config.get("max")
        if min_val is not None and value < min_val:
            raise HomeAssistantError(
                f"Value {value} below minimum {min_val} for {register_key}"
            )
        if max_val is not None and value > max_val:
            raise HomeAssistantError(
                f"Value {value} above maximum {max_val} for {register_key}"
            )

        # Reverse scaling: convert user-facing value to raw register value
        scale = config.get("scale", 1.0)
        raw_value = int(round(value / scale)) if scale != 1 else int(value)

        # Encode to register word(s)
        data_type = config.get("data_type", "uint16")
        register_words = self._encode_register_value(raw_value, data_type)
        address = config["address"]

        _LOGGER.info(
            "RW write start register=%s addr=%d value=%s raw=%d words=%s",
            register_key,
            address,
            value,
            raw_value,
            register_words,
        )

        async with self._lock:
            try:
                await self._connect()

                result = await self._client.write_registers(
                    address=address,
                    values=register_words,
                    device_id=self._unit_id,
                )

                if result.isError():
                    _LOGGER.info(
                        "RW write error register=%s addr=%d response=%s",
                        register_key,
                        address,
                        result,
                    )
                    raise HomeAssistantError(
                        f"Modbus write error for {register_key}: {result}"
                    )

                _LOGGER.info(
                    "RW write success register=%s addr=%d words=%s",
                    register_key,
                    address,
                    register_words,
                )

            except ModbusException as err:
                _LOGGER.info(
                    "RW write exception register=%s addr=%d error=%s",
                    register_key,
                    address,
                    err,
                )
                await self._disconnect()
                raise HomeAssistantError(
                    f"Modbus exception writing {register_key}: {err}"
                ) from err

        # Read-back verification
        readback = await self._read_registers(
            address, config.get("count", 1), REG_HOLDING
        )
        if readback is not None:
            readback_words = readback[: len(register_words)]
            _LOGGER.info(
                "RW readback register=%s addr=%d expected=%s actual=%s",
                register_key,
                address,
                register_words,
                readback_words,
            )
            if readback_words != register_words:
                _LOGGER.warning(
                    "Read-back mismatch for %s: wrote %s, read %s",
                    register_key,
                    register_words,
                    readback_words,
                )

            # Push the verified read-back value into coordinator state immediately
            # so writable config entities do not stay stale until their next
            # poll_profile interval becomes due.
            processed = self._process_register_value(readback, config)
            updated_data = dict(self.data or {})
            updated_data[register_key] = processed
            detail = self._build_read_detail(readback, config, processed)
            detail["status_source"] = "write_readback"
            detail = self._annotate_runtime_detail(register_key, detail)
            self.last_read_details[register_key] = (
                self._apply_register_poll_state_to_detail(register_key, detail)
            )
            self._last_poll_monotonic[register_key] = time.monotonic()
            self.async_set_updated_data(updated_data)
        else:
            _LOGGER.info(
                "RW readback missing register=%s addr=%d expected=%s",
                register_key,
                address,
                register_words,
            )

        await self.async_request_refresh()

    async def async_shutdown(self) -> None:
        """Shutdown the coordinator."""
        await self._disconnect()
        await super().async_shutdown()
