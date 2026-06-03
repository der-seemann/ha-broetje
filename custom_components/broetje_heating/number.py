"""Number platform for the Brötje Heatpump integration."""

from __future__ import annotations

from homeassistant.components.number import NumberDeviceClass, NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import BroetjeModbusCoordinator
from .entity import BroetjeEntity

DEVICE_CLASS_MAP = {
    "temperature": NumberDeviceClass.TEMPERATURE,
}

UNIT_MAP = {
    "°C": UnitOfTemperature.CELSIUS,
}

MODE_MAP = {
    "slider": NumberMode.SLIDER,
    "box": NumberMode.BOX,
    "auto": NumberMode.AUTO,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the number platform."""
    coordinator: BroetjeModbusCoordinator = entry.runtime_data

    entities: list[BroetjeNumber] = []

    for entity_key, entity_config in coordinator.numbers.items():
        entities.append(
            BroetjeNumber(
                coordinator=coordinator,
                entity_key=entity_key,
                entity_config=entity_config,
            )
        )

    async_add_entities(entities)


class BroetjeNumber(BroetjeEntity, NumberEntity):
    """Number entity for writable Brötje Heatpump registers."""

    def __init__(
        self,
        coordinator: BroetjeModbusCoordinator,
        entity_key: str,
        entity_config: dict,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(
            coordinator,
            entity_key,
            zone_number=entity_config.get("zone_number"),
        )

        self._register_key = entity_config["register"]

        zone_number = entity_config.get("zone_number")
        if translation_key := entity_config.get("translation_key"):
            self._attr_translation_key = translation_key
            if zone_number:
                self._attr_translation_placeholders = {"zone": str(zone_number)}
        elif name := entity_config.get("name"):
            self._attr_name = (
                name.format(zone=zone_number) if zone_number is not None else name
            )
        else:
            self._attr_name = entity_key.replace("_", " ")

        self._attr_device_class = None
        device_class = entity_config.get("device_class")
        if device_class:
            self._attr_device_class = DEVICE_CLASS_MAP.get(device_class)

        unit = entity_config.get("unit")
        if unit:
            self._attr_native_unit_of_measurement = UNIT_MAP.get(unit, unit)

        mode = entity_config.get("mode", "auto")
        self._attr_mode = MODE_MAP.get(mode, NumberMode.AUTO)

        if icon := entity_config.get("icon"):
            self._attr_icon = icon

        reg_config = coordinator.register_map[self._register_key]
        if "min" in reg_config:
            self._attr_native_min_value = reg_config["min"]
        if "max" in reg_config:
            self._attr_native_max_value = reg_config["max"]
        if "step" in reg_config:
            self._attr_native_step = reg_config["step"]

    @property
    def available(self) -> bool:
        """Return entity availability."""
        if not super().available:
            return False

        detail = self.coordinator.last_read_details.get(self._register_key)
        if detail is None:
            return True

        return detail.get("status") in {
            "ok",
            "sentinel_no_data",
            "auto_disabled_sentinel_retry_pending",
            "auto_disabled_sentinel_permanent",
            "auto_disabled_exception_code_10",
            "auto_disabled_exception_code_3_backoff",
        }

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        if self.coordinator.data is None:
            return None

        value = self.coordinator.data.get(self._register_key)
        if value is None:
            return None

        if self._attr_device_class == NumberDeviceClass.TEMPERATURE:
            return round(float(value), 1)

        return round(float(value), 2)

    async def async_set_native_value(self, value: float) -> None:
        """Set the register value."""
        await self.coordinator.async_write_register(self._register_key, value)
