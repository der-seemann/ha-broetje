"""The Brötje Heatpump integration."""

from __future__ import annotations

import logging
import re
import shutil
from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er

from .const import CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN, SUB_DEVICE_LABELS
from .coordinator import BroetjeModbusCoordinator
from .devices import CONF_DEVICE_TYPE, DeviceType

_LOGGER = logging.getLogger(__name__)

_RW_ENTITY_ID_MIGRATIONS: dict[tuple[str, str], str] = {
    (
        Platform.NUMBER,
        "control_power",
    ): "number.brotje_iwr_gtw_08_boiler_steuerung_leistungssollwert",
    (
        Platform.NUMBER,
        "control_temperature",
    ): "number.brotje_iwr_gtw_08_boiler_steuerung_temperatursollwert",
    (
        Platform.SELECT,
        "control_algorithm_type",
    ): "select.brotje_iwr_gtw_08_boiler_steuerung_algorithmustyp",
    (
        Platform.SELECT,
        "control_heat_demand_type",
    ): "select.brotje_iwr_gtw_08_boiler_steuerung_warmeanforderungstyp",
}

_RW_STALE_ENTITY_KEYS: dict[str, set[str]] = {
    Platform.SENSOR: {
        "control_power",
        "control_temperature",
        "control_algorithm_type",
        "control_heat_demand_type",
    },
    Platform.NUMBER: {
        "low_noise_start_time",
        "low_noise_stop_time",
    },
}

PLATFORMS: list[Platform] = [
    Platform.CLIMATE,
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.TIME,
]

type BroetjeConfigEntry = ConfigEntry[BroetjeModbusCoordinator]


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate old config entries to new format."""
    if config_entry.version > 3:
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

    if config_entry.version == 2:
        _LOGGER.debug("Migrating config entry from version 2 to 3")
        zone_count = config_entry.data.get("zone_count", 1)
        new_data = {**config_entry.data}
        new_data.pop("zone_count", None)
        new_data["zones"] = list(range(1, zone_count + 1))
        hass.config_entries.async_update_entry(
            config_entry,
            data=new_data,
            version=3,
            minor_version=1,
        )
        _LOGGER.info(
            "Migration to version 3 successful: zone_count=%d -> zones=%s",
            zone_count,
            new_data["zones"],
        )

    if config_entry.version == 3 and config_entry.minor_version < 2:
        _LOGGER.debug("Migrating config entry from version 3.1 to 3.2")
        entity_registry = er.async_get(hass)
        stale_unique_ids = {
            f"{config_entry.unique_id}_appliance_time",
            f"{config_entry.unique_id}_low_noise_mode_state",
        }
        removed = 0

        for entry in er.async_entries_for_config_entry(entity_registry, config_entry.entry_id):
            if (
                entry.platform == DOMAIN
                and entry.domain == Platform.BINARY_SENSOR
                and entry.unique_id in stale_unique_ids
            ):
                entity_registry.async_remove(entry.entity_id)
                removed += 1

        hass.config_entries.async_update_entry(
            config_entry,
            version=3,
            minor_version=2,
        )
        _LOGGER.info(
            "Migration to version 3.2 successful: removed %d stale binary sensor entries",
            removed,
        )

    if config_entry.version == 3 and config_entry.minor_version < 3:
        _LOGGER.debug("Migrating config entry from version 3.2 to 3.3")
        entity_registry = er.async_get(hass)
        unique_root = config_entry.unique_id or config_entry.entry_id

        removed = _remove_stale_rw_registry_entries(
            entity_registry, config_entry, unique_root
        )
        renamed = _migrate_rw_entity_ids(entity_registry, config_entry, unique_root)

        hass.config_entries.async_update_entry(
            config_entry,
            version=3,
            minor_version=3,
        )
        _LOGGER.info(
            "Migration to version 3.3 successful: removed %d stale RW entities, renamed %d active entities",
            removed,
            renamed,
        )

    return True


def _remove_stale_rw_registry_entries(
    entity_registry: er.EntityRegistry,
    config_entry: ConfigEntry,
    unique_root: str,
) -> int:
    """Remove disabled/hidden legacy entries replaced by RW/time entities."""
    stale_unique_ids = {
        (domain, f"{unique_root}_{entity_key}")
        for domain, entity_keys in _RW_STALE_ENTITY_KEYS.items()
        for entity_key in entity_keys
    }
    removed = 0

    for entry in er.async_entries_for_config_entry(entity_registry, config_entry.entry_id):
        if entry.platform != DOMAIN:
            continue

        key = (entry.domain, entry.unique_id)
        if key not in stale_unique_ids:
            continue

        if entry.disabled_by is None and entry.hidden_by is None:
            _LOGGER.warning(
                "Skipping removal of active legacy entity %s during 3.3 migration",
                entry.entity_id,
            )
            continue

        entity_registry.async_remove(entry.entity_id)
        removed += 1

    return removed


def _migrate_rw_entity_ids(
    entity_registry: er.EntityRegistry,
    config_entry: ConfigEntry,
    unique_root: str,
) -> int:
    """Rename new RW entities from generic IDs to stable descriptive IDs."""
    renamed = 0

    for (domain, entity_key), target_entity_id in _RW_ENTITY_ID_MIGRATIONS.items():
        unique_id = f"{unique_root}_{entity_key}"
        entry = entity_registry.async_get_entity_id(domain, DOMAIN, unique_id)
        if entry is None:
            continue

        if entry == target_entity_id:
            continue

        blocking_entry = entity_registry.async_get(target_entity_id)
        if blocking_entry is not None and blocking_entry.entity_id != entry:
            if (
                blocking_entry.platform == DOMAIN
                and blocking_entry.config_entry_id == config_entry.entry_id
                and (blocking_entry.disabled_by is not None or blocking_entry.hidden_by is not None)
            ):
                entity_registry.async_remove(blocking_entry.entity_id)
            else:
                _LOGGER.warning(
                    "Skipping entity-id migration for %s because %s is already in use",
                    entry,
                    target_entity_id,
                )
                continue

        entity_registry.async_update_entity(entry, new_entity_id=target_entity_id)
        renamed += 1

    return renamed


async def async_setup_entry(hass: HomeAssistant, entry: BroetjeConfigEntry) -> bool:
    """Set up Brötje Heatpump from a config entry."""
    # Copy images to www folder for dashboard use
    await hass.async_add_executor_job(_copy_images_to_www, hass)

    coordinator = BroetjeModbusCoordinator(hass, entry)

    await coordinator.async_config_entry_first_refresh()
    disabled = coordinator.sync_permanently_disabled_registry_entities()
    if disabled:
        _LOGGER.info(
            "Disabled %d registry entries for permanently auto-disabled registers",
            disabled,
        )

    entry.runtime_data = coordinator

    _cleanup_replaced_registry_entities(hass, entry, coordinator)
    _cleanup_inactive_subdevice_registry_entities(hass, entry, coordinator)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Clean up orphaned zone sub-devices when zone_count has been reduced
    _cleanup_orphan_zone_devices(hass, entry)
    # Clean up sub-devices that are no longer detected on this installation
    _cleanup_orphan_sub_devices(hass, entry, coordinator)

    entry.async_on_unload(entry.add_update_listener(_async_update_options))

    return True


def _cleanup_replaced_registry_entities(
    hass: HomeAssistant,
    entry: BroetjeConfigEntry,
    coordinator: BroetjeModbusCoordinator,
) -> None:
    """Remove stale registry entries replaced by other entity platforms."""
    entity_registry = er.async_get(hass)
    unique_root = entry.unique_id or entry.entry_id

    current_domain_by_key: dict[str, set[str]] = {}
    known_entity_keys: set[str] = set()
    for domain, entity_map in (
        (Platform.SENSOR, coordinator.sensors),
        (Platform.BINARY_SENSOR, coordinator.binary_sensors),
        (Platform.NUMBER, coordinator.numbers),
        (Platform.SELECT, coordinator.selects),
        (Platform.TIME, coordinator.times),
        (Platform.CLIMATE, coordinator.climates),
    ):
        for entity_key, config in entity_map.items():
            known_entity_keys.add(entity_key)
            sub_device = config.get("sub_device")
            if (
                sub_device is not None
                and sub_device not in coordinator.active_sub_devices
            ):
                continue
            current_domain_by_key.setdefault(entity_key, set()).add(domain)

    removed = 0
    enabled = 0
    prefix = f"{unique_root}_"
    writable_keys = {
        key for key, config in coordinator.register_map.items() if config.get("writable")
    }

    for registry_entry in er.async_entries_for_config_entry(entity_registry, entry.entry_id):
        if registry_entry.platform != DOMAIN:
            continue
        if not registry_entry.unique_id.startswith(prefix):
            continue

        entity_key = registry_entry.unique_id[len(prefix) :]
        expected_domains = current_domain_by_key.get(entity_key)
        if entity_key in known_entity_keys and expected_domains is None:
            entity_registry.async_remove(registry_entry.entity_id)
            removed += 1
            continue
        if expected_domains is None:
            continue
        if registry_entry.domain in expected_domains:
            if (
                entity_key in writable_keys
                and not coordinator.is_entity_permanently_disabled(entity_key)
                and str(registry_entry.disabled_by).lower().endswith("integration")
            ):
                entity_registry.async_update_entity(
                    registry_entry.entity_id,
                    disabled_by=None,
                )
                enabled += 1
            continue

        entity_registry.async_remove(registry_entry.entity_id)
        removed += 1

    if removed:
        _LOGGER.info("Removed %d stale registry entries replaced by RW entities", removed)
    if enabled:
        _LOGGER.info("Enabled %d writable RW registry entries", enabled)


def _cleanup_inactive_subdevice_registry_entities(
    hass: HomeAssistant,
    entry: BroetjeConfigEntry,
    coordinator: BroetjeModbusCoordinator,
) -> None:
    """Remove registry entries for entities gated behind inactive sub-devices."""
    entity_registry = er.async_get(hass)
    unique_root = entry.unique_id or entry.entry_id

    inactive_entity_keys: set[str] = set()
    for entity_map in (
        coordinator.sensors,
        coordinator.binary_sensors,
        coordinator.numbers,
        coordinator.selects,
        coordinator.times,
    ):
        for entity_key, config in entity_map.items():
            sub_device = config.get("sub_device")
            if (
                sub_device is not None
                and sub_device not in coordinator.active_sub_devices
            ):
                inactive_entity_keys.add(entity_key)

    removed = 0
    prefix = f"{unique_root}_"
    for registry_entry in er.async_entries_for_config_entry(entity_registry, entry.entry_id):
        if registry_entry.platform != DOMAIN:
            continue
        if not registry_entry.unique_id.startswith(prefix):
            continue

        entity_key = registry_entry.unique_id[len(prefix) :]
        if entity_key not in inactive_entity_keys:
            continue

        entity_registry.async_remove(registry_entry.entity_id)
        removed += 1

    if removed:
        _LOGGER.info(
            "Removed %d registry entries for inactive sub-device entities",
            removed,
        )


def _cleanup_orphan_zone_devices(
    hass: HomeAssistant, entry: BroetjeConfigEntry
) -> None:
    """Remove zone sub-devices that are no longer in the configured zones list."""
    configured_zones = set(entry.data.get("zones", []))
    device_registry = dr.async_get(hass)
    entry_id = entry.entry_id

    zone_id_pattern = re.compile(rf"^{re.escape(entry_id)}_zone_(\d+)$")

    for device in dr.async_entries_for_config_entry(device_registry, entry_id):
        for _, identifier in device.identifiers:
            match = zone_id_pattern.match(identifier)
            if match:
                zone_num = int(match.group(1))
                if zone_num not in configured_zones:
                    _LOGGER.info(
                        "Removing orphaned zone device: Zone %d (configured=%s)",
                        zone_num,
                        sorted(configured_zones),
                    )
                    device_registry.async_remove_device(device.id)
                break


def _cleanup_orphan_sub_devices(
    hass: HomeAssistant,
    entry: BroetjeConfigEntry,
    coordinator: BroetjeModbusCoordinator,
) -> None:
    """Remove functional sub-devices that are no longer detected on this installation."""
    device_registry = dr.async_get(hass)
    entry_id = entry.entry_id
    known_subdev_ids = {f"{entry_id}_{key}" for key in SUB_DEVICE_LABELS}
    active_subdev_ids = {f"{entry_id}_{key}" for key in coordinator.active_sub_devices}

    for device in dr.async_entries_for_config_entry(device_registry, entry_id):
        for _, identifier in device.identifiers:
            if identifier in known_subdev_ids and identifier not in active_subdev_ids:
                _LOGGER.info(
                    "Removing orphaned sub-device: %s",
                    identifier,
                )
                device_registry.async_remove_device(device.id)
            break


async def _async_update_options(hass: HomeAssistant, entry: BroetjeConfigEntry) -> None:
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
