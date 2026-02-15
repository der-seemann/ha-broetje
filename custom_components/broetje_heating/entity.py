"""Base entity for the Brötje Heatpump integration."""

from __future__ import annotations

from typing import Any

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import BroetjeModbusCoordinator


class BroetjeEntity(CoordinatorEntity[BroetjeModbusCoordinator]):
    """Base class for Brötje Heatpump entities."""

    _attr_has_entity_name = True
    _register_key: str | None = None

    def __init__(
        self,
        coordinator: BroetjeModbusCoordinator,
        entity_key: str,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._entity_key = entity_key

        # Generate unique ID based on device and entity key
        device_id = (
            coordinator.config_entry.unique_id or coordinator.config_entry.entry_id
        )
        self._attr_unique_id = f"{device_id}_{entity_key}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.config_entry.entry_id)},
            name=f"Brötje {self.coordinator.device_model}",
            manufacturer=self.coordinator.device_manufacturer,
            model=self.coordinator.device_model,
            serial_number=self.coordinator.device_serial,
            sw_version=self.coordinator.device_firmware,
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return register metadata as extra state attributes."""
        if self._register_key is None:
            return None

        reg_config = self.coordinator.register_map.get(self._register_key)
        if reg_config is None:
            return None

        attrs: dict[str, Any] = {
            "register_address": reg_config["address"],
            "register_type": reg_config.get("type", "holding"),
            "register_size": reg_config.get("count", 1),
            "data_type": reg_config.get("data_type", "int16"),
        }

        scale = reg_config.get("scale", 1)
        if scale != 1:
            attrs["scaling_factor"] = scale

        if bit := reg_config.get("bit"):
            attrs["bit_position"] = bit

        return attrs
