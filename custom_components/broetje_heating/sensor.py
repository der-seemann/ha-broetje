"""Sensor platform for the Brötje Heatpump integration."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfPressure,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.storage import Store

from .arbeitszahl import (
    ArbeitszahlTracker,
    async_restore_tracker,
    async_save_tracker,
    source_values_available,
)
from .const import (
    CONF_ARBEITSZAHL_ELECTRICAL_BASELINE,
    CONF_ARBEITSZAHL_THERMAL_BASELINE,
)
from .coordinator import BroetjeModbusCoordinator
from .entity import BroetjeEntity

# Map device class strings to actual classes
DEVICE_CLASS_MAP = {
    "temperature": SensorDeviceClass.TEMPERATURE,
    "pressure": SensorDeviceClass.PRESSURE,
    "power": SensorDeviceClass.POWER,
    "energy": SensorDeviceClass.ENERGY,
    "frequency": SensorDeviceClass.FREQUENCY,
    "duration": SensorDeviceClass.DURATION,
    "enum": SensorDeviceClass.ENUM,
}

# Map unit strings to actual units
UNIT_MAP = {
    "°C": UnitOfTemperature.CELSIUS,
    "bar": UnitOfPressure.BAR,
    "kWh": UnitOfEnergy.KILO_WATT_HOUR,
    "kW": UnitOfPower.KILO_WATT,
    "h": UnitOfTime.HOURS,
    "%": PERCENTAGE,
}

# Map state class strings to actual classes
STATE_CLASS_MAP = {
    "measurement": SensorStateClass.MEASUREMENT,
    "total": SensorStateClass.TOTAL,
    "total_increasing": SensorStateClass.TOTAL_INCREASING,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator: BroetjeModbusCoordinator = entry.runtime_data

    entities: list[BroetjeSensor] = []

    for sensor_key, sensor_config in coordinator.sensors.items():
        sub_device = sensor_config.get("sub_device")
        if sub_device is not None and sub_device not in coordinator.active_sub_devices:
            continue
        entities.append(
            BroetjeSensor(
                coordinator=coordinator,
                entity_key=sensor_key,
                sensor_config=sensor_config,
            )
        )

    if {
        "total_energy_consumed",
        "total_thermal_delivered",
    }.issubset(coordinator.register_map):
        entities.append(ArbeitszahlSensor(coordinator))

    async_add_entities(entities)


class BroetjeSensor(BroetjeEntity, SensorEntity):
    """Sensor entity for Brötje Heatpump."""

    def __init__(
        self,
        coordinator: BroetjeModbusCoordinator,
        entity_key: str,
        sensor_config: dict,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(
            coordinator,
            entity_key,
            zone_number=sensor_config.get("zone_number"),
            sub_device=sensor_config.get("sub_device"),
        )

        self._register_key = sensor_config["register"]
        self._apply_dynamic_enabled_default(self._register_key)
        self._attr_translation_key = sensor_config.get("translation_key", entity_key)
        self._value_format = sensor_config.get("value_format")
        self._device_categories = sensor_config.get("device_categories", {})

        # Support zone/board number placeholders in translation strings
        placeholders: dict[str, str] = {}
        if zone_number := sensor_config.get("zone_number"):
            placeholders["zone"] = str(zone_number)
        if board_number := sensor_config.get("board_number"):
            placeholders["board"] = str(board_number)
        if placeholders:
            self._attr_translation_placeholders = placeholders

        self._attr_device_class = None
        self._enum_map = None

        device_class = sensor_config.get("device_class")

        if device_class == "enum":
            self._attr_device_class = SensorDeviceClass.ENUM
            enum_map_name = sensor_config.get("enum_map", "operating_modes")
            self._enum_map = coordinator.enum_maps.get(enum_map_name, {})
            self._attr_options = list(self._enum_map.values())
        elif device_class:
            self._attr_device_class = DEVICE_CLASS_MAP.get(device_class)

        # Set unit
        unit = sensor_config.get("unit")
        if unit:
            self._attr_native_unit_of_measurement = UNIT_MAP.get(unit, unit)

        # Set state class
        state_class = sensor_config.get("state_class")
        if state_class:
            self._attr_state_class = STATE_CLASS_MAP.get(state_class)

        # Set icon if specified
        if icon := sensor_config.get("icon"):
            self._attr_icon = icon

    @property
    def available(self) -> bool:
        """Return entity availability."""
        if not super().available:
            return False

        detail = self.coordinator.last_read_details.get(self._register_key)
        if detail is None:
            return True

        status = detail.get("status")

        # Keep enum sensors available so mapped sentinel states like
        # "device_not_available" remain visible. Numeric sentinel-only sensors
        # should present as unavailable instead of generic "unknown".
        if status in {
            "sentinel_no_data",
            "auto_disabled_sentinel_retry_pending",
            "auto_disabled_sentinel_permanent",
        }:
            return self._attr_device_class == SensorDeviceClass.ENUM

        # Protocol/read failures should surface as unavailable instead of
        # generic HA "unknown" states.
        return status not in {
            "read_error",
            "incomplete_batch_retry_failed",
            "invalid_value",
            "auto_disabled_sentinel_retry_pending",
            "auto_disabled_sentinel_permanent",
            "auto_disabled_exception_code_10_permanent",
            "auto_disabled_exception_code_10",
            "auto_disabled_exception_code_3_backoff",
        }

    @property
    def native_value(self) -> float | str | None:
        """Return the sensor value."""
        if self.coordinator.data is None:
            return None

        value = self.coordinator.data.get(self._register_key)

        if (
            value is None
            and self._attr_device_class == SensorDeviceClass.ENUM
            and self._enum_map
        ):
            detail = self.coordinator.last_read_details.get(self._register_key, {})
            if (
                detail.get("status")
                in {
                    "sentinel_no_data",
                    "auto_disabled_sentinel_retry_pending",
                    "auto_disabled_sentinel_permanent",
                }
                and "device_not_available" in self._enum_map.values()
            ):
                return "device_not_available"

        if value is None:
            return None

        # Handle enum device class - return None for unmapped values
        # to avoid HA rejecting states not in the options list
        if self._attr_device_class == SensorDeviceClass.ENUM and self._enum_map:
            return self._enum_map.get(int(value))

        # Handle device type format: decode 0xZZYY into "CATEGORY-YY"
        if self._value_format == "device_type":
            raw = int(value)
            category_code = (raw >> 8) & 0xFF
            variant = raw & 0xFF
            category_name = self._device_categories.get(
                category_code, f"0x{category_code:02X}"
            )
            return f"{category_name}-{variant:02d}"

        # Round temperature values to 1 decimal
        if self._attr_device_class == SensorDeviceClass.TEMPERATURE:
            return round(value, 1)

        # Round pressure values to 2 decimals
        if self._attr_device_class == SensorDeviceClass.PRESSURE:
            return round(value, 2)

        # Round other numeric values to 2 decimals
        if isinstance(value, float):
            return round(value, 2)

        return value


class ArbeitszahlSensor(BroetjeEntity, SensorEntity):
    """Cumulative working ratio since a locally configured counter baseline."""

    _attr_icon = "mdi:chart-line"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: BroetjeModbusCoordinator) -> None:
        super().__init__(coordinator, "arbeitszahl_seit_nullpunkt")
        self._attr_translation_key = "arbeitszahl_seit_nullpunkt"
        entry = coordinator.config_entry
        self._tracker = ArbeitszahlTracker(
            entry.options.get(CONF_ARBEITSZAHL_ELECTRICAL_BASELINE),
            entry.options.get(CONF_ARBEITSZAHL_THERMAL_BASELINE),
        )
        self._store = Store(
            coordinator.hass,
            1,
            f"{entry.domain}.{entry.entry_id}.arbeitszahl",
        )
        self._restore_done = False

    @property
    def available(self) -> bool:
        return (
            super().available
            and self._tracker.baseline_valid
            and self.native_value is not None
        )

    @property
    def native_value(self) -> float | None:
        data = self.coordinator.data
        if not self._restore_done or data is None or not self._sources_available():
            return None
        # observe() is idempotent for unchanged coordinator values and keeps the
        # reset guard active even when the sensor is disabled in the registry.
        return self._tracker.observe(
            data.get("total_energy_consumed"), data.get("total_thermal_delivered")
        )

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        await async_restore_tracker(self._store, self._tracker)
        self._restore_done = True
        self._observe_and_save()

    @callback
    def _handle_coordinator_update(self) -> None:
        self._observe_and_save()
        super()._handle_coordinator_update()

    @callback
    def _observe_and_save(self) -> None:
        if (
            not self._restore_done
            or not self._tracker.baseline_valid
            or self.coordinator.data is None
            or not self._sources_available()
        ):
            return
        self._tracker.observe(
            self.coordinator.data.get("total_energy_consumed"),
            self.coordinator.data.get("total_thermal_delivered"),
        )
        self.hass.async_create_task(async_save_tracker(self._store, self._tracker))

    def _sources_available(self) -> bool:
        details = self.coordinator.last_read_details
        return source_values_available(
            details.get("total_energy_consumed"),
            details.get("total_thermal_delivered"),
        )
