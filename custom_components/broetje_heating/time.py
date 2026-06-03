"""Time platform for the Brötje Heatpump integration."""

from __future__ import annotations

from datetime import time

from homeassistant.components.time import TimeEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import BroetjeModbusCoordinator
from .entity import BroetjeEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the time platform."""
    coordinator: BroetjeModbusCoordinator = entry.runtime_data

    async_add_entities(
        BroetjeTime(
            coordinator=coordinator,
            entity_key=entity_key,
            entity_config=entity_config,
        )
        for entity_key, entity_config in coordinator.times.items()
    )


class BroetjeTime(BroetjeEntity, TimeEntity):
    """Time entity for writable Brötje Heatpump time-of-day registers."""

    def __init__(
        self,
        coordinator: BroetjeModbusCoordinator,
        entity_key: str,
        entity_config: dict,
    ) -> None:
        """Initialize the time entity."""
        super().__init__(
            coordinator,
            entity_key,
            zone_number=entity_config.get("zone_number"),
            sub_device=entity_config.get("sub_device"),
        )

        self._register_key = entity_config["register"]
        if translation_key := entity_config.get("translation_key"):
            self._attr_translation_key = translation_key
        elif name := entity_config.get("name"):
            self._attr_name = name
        else:
            self._attr_name = entity_key.replace("_", " ")
        self._slot_minutes = entity_config.get("slot_minutes", 10)

        if icon := entity_config.get("icon"):
            self._attr_icon = icon

    @property
    def available(self) -> bool:
        """Return entity availability."""
        if not super().available:
            return False

        detail = self.coordinator.last_read_details.get(self._register_key)
        if detail is None:
            return True

        return detail.get("status") == "ok"

    @property
    def native_value(self) -> time | None:
        """Return the current value as local time of day."""
        if self.coordinator.data is None:
            return None

        value = self.coordinator.data.get(self._register_key)
        if value is None:
            return None

        total_minutes = int(value) * self._slot_minutes
        total_minutes %= 24 * 60
        return time(hour=total_minutes // 60, minute=total_minutes % 60)

    async def async_set_value(self, value: time) -> None:
        """Set the register value from a local time of day."""
        if value.second or value.microsecond:
            raise HomeAssistantError("Only whole-minute values are supported")

        total_minutes = value.hour * 60 + value.minute
        if total_minutes % self._slot_minutes:
            raise HomeAssistantError(
                f"Time must be aligned to {self._slot_minutes}-minute steps"
            )

        await self.coordinator.async_write_register(
            self._register_key, total_minutes // self._slot_minutes
        )
