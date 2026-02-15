"""The Brötje Heatpump integration."""

from __future__ import annotations

import logging
import shutil
from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
from .coordinator import BroetjeModbusCoordinator
from .devices import CONF_DEVICE_TYPE, DeviceType

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]

type BroetjeConfigEntry = ConfigEntry[BroetjeModbusCoordinator]


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate old config entries to new format."""
    if config_entry.version > 2:
        return False

    if config_entry.version == 1:
        _LOGGER.debug("Migrating config entry from version 1 to 2")
        new_data = {**config_entry.data, CONF_DEVICE_TYPE: DeviceType.ISR.value}
        hass.config_entries.async_update_entry(
            config_entry,
            data=new_data,
            version=2,
            minor_version=1,
        )
        _LOGGER.info("Migration to version 2 successful: added device_type=isr")

    return True


async def async_setup_entry(hass: HomeAssistant, entry: BroetjeConfigEntry) -> bool:
    """Set up Brötje Heatpump from a config entry."""
    # Copy images to www folder for dashboard use
    await hass.async_add_executor_job(_copy_images_to_www, hass)

    coordinator = BroetjeModbusCoordinator(hass, entry)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(_async_update_options))

    return True


async def _async_update_options(
    hass: HomeAssistant, entry: BroetjeConfigEntry
) -> None:
    """Handle options update."""
    coordinator: BroetjeModbusCoordinator = entry.runtime_data
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    coordinator.update_scan_interval(scan_interval)


def _copy_images_to_www(hass: HomeAssistant) -> None:
    """Copy integration images to www folder for dashboard use."""
    source_dir = Path(__file__).parent / "images"
    www_dir = Path(hass.config.path("www")) / "broetje_heatpump"

    if not source_dir.exists():
        _LOGGER.debug("No images directory found in integration")
        return

    try:
        www_dir.mkdir(parents=True, exist_ok=True)

        for image_file in source_dir.glob("*.png"):
            dest_file = www_dir / image_file.name
            if not dest_file.exists():
                shutil.copy2(image_file, dest_file)
                _LOGGER.debug("Copied %s to %s", image_file.name, dest_file)

        _LOGGER.info("Images available at /local/broetje_heatpump/ for dashboard use")
    except OSError as err:
        _LOGGER.warning("Failed to copy images to www folder: %s", err)


async def async_unload_entry(hass: HomeAssistant, entry: BroetjeConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        await entry.runtime_data.async_shutdown()

    return unload_ok
