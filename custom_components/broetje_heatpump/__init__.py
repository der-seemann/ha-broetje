"""The Brötje Heatpump integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import BroetjeModbusCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]

type BroetjeConfigEntry = ConfigEntry[BroetjeModbusCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: BroetjeConfigEntry) -> bool:
    """Set up Brötje Heatpump from a config entry."""
    coordinator = BroetjeModbusCoordinator(hass, entry)
    
    await coordinator.async_config_entry_first_refresh()
    
    entry.runtime_data = coordinator
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: BroetjeConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        await entry.runtime_data.async_shutdown()
    
    return unload_ok
