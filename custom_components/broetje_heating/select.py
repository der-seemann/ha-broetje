"""Select platform for the Brötje Heatpump integration."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import BroetjeModbusCoordinator
from .entity import BroetjeEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the select platform."""
    coordinator: BroetjeModbusCoordinator = entry.runtime_data

    entities: list[BroetjeSelect] = []

    for entity_key, entity_config in coordinator.selects.items():
        sub_device = entity_config.get("sub_device")
        if sub_device is not None and sub_device not in coordinator.active_sub_devices:
            continue
        entities.append(
            BroetjeSelect(
                coordinator=coordinator,
                entity_key=entity_key,
                entity_config=entity_config,
            )
        )

    async_add_entities(entities)


class BroetjeSelect(BroetjeEntity, SelectEntity):
    """Select entity for writable Brötje Heatpump enum registers."""

    def __init__(
        self,
        coordinator: BroetjeModbusCoordinator,
        entity_key: str,
        entity_config: dict,
    ) -> None:
        """Initialize the select entity."""
        super().__init__(
            coordinator,
            entity_key,
            zone_number=entity_config.get("zone_number"),
        )

        self._register_key = entity_config["register"]
        self._attr_translation_key = entity_config.get("translation_key", entity_key)

        if zone_number := entity_config.get("zone_number"):
            self._attr_translation_placeholders = {"zone": str(zone_number)}

        if icon := entity_config.get("icon"):
            self._attr_icon = icon

        enum_map_name = entity_config.get("enum_map", "")
        self._enum_map: dict[int, str] = coordinator.enum_maps.get(enum_map_name, {})
        self._reverse_map: dict[str, int] = {v: k for k, v in self._enum_map.items()}
        self._attr_options = list(self._enum_map.values())

    @property
    def current_option(self) -> str | None:
        """Return the current selected option."""
        if self.coordinator.data is None:
            return None

        value = self.coordinator.data.get(self._register_key)
        if value is None:
            return None

        return self._enum_map.get(int(value))

    async def async_select_option(self, option: str) -> None:
        """Set the selected option."""
        raw_value = self._reverse_map.get(option)
        if raw_value is None:
            return
        await self.coordinator.async_write_register(self._register_key, raw_value)
