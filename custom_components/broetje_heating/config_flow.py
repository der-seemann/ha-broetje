"""Config flow for Brötje Heatpump integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.helpers import area_registry as ar
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_EXTERNAL_ROOM_SENSORS,
    CONF_EXTERNAL_ROOM_SENSOR_AGGREGATION,
    CONF_EXTERNAL_ROOM_SENSOR_ENTITY_IDS,
    CONF_EXTERNAL_ROOM_SENSOR_TIMEOUT,
    CONF_EXTERNAL_ROOM_SENSOR_WRITE_INTERVAL,
    CONF_IWR_FEATURES,
    CONF_IWR_FEATURES_SOURCE,
    CONF_IWR_ZONE_DETAILS,
    CONF_SCAN_INTERVAL,
    CONF_SCAN_INTERVAL_FAST,
    CONF_SCAN_INTERVAL_NORMAL,
    CONF_SCAN_INTERVAL_SLOW,
    CONF_UNIT_ID,
    CONF_ZONES,
    DEFAULT_EXTERNAL_ROOM_SENSOR_TIMEOUT,
    DEFAULT_EXTERNAL_ROOM_SENSOR_WRITE_INTERVAL,
    DEFAULT_PORT,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL_FAST,
    DEFAULT_SCAN_INTERVAL_SLOW,
    DEFAULT_UNIT_ID,
    DOMAIN,
    EXTERNAL_ROOM_SENSOR_AGGREGATION_AVERAGE,
    EXTERNAL_ROOM_SENSOR_AGGREGATION_MAX,
    EXTERNAL_ROOM_SENSOR_AGGREGATION_MIN,
    FEATURE_BUFFER_TANK,
    FEATURE_CASCADE,
    FEATURE_COOLING,
    FEATURE_HYBRID,
    IWR_FEATURES_SOURCE_MANUAL,
)
from .devices import CONF_DEVICE_TYPE, DEVICE_MODELS, DeviceType
from .iwr_setup import ZONE_ROLE_HEATING
from .iwr_setup import detect_iwr_setup

_LOGGER = logging.getLogger(__name__)
_ALL_AREAS_FILTER = "__all_areas__"

STEP_CONNECTION_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
        vol.Required(CONF_UNIT_ID, default=DEFAULT_UNIT_ID): int,
    }
)

class CannotConnect(Exception):
    """Error to indicate we cannot connect."""


def _normalize_feature_selection(
    selected: dict[str, Any] | None,
) -> dict[str, bool]:
    """Return feature flags with explicit bool defaults."""
    selected = selected or {}
    return {
        FEATURE_HYBRID: bool(selected.get(FEATURE_HYBRID, False)),
        FEATURE_CASCADE: bool(selected.get(FEATURE_CASCADE, False)),
        FEATURE_COOLING: bool(selected.get(FEATURE_COOLING, False)),
        FEATURE_BUFFER_TANK: bool(selected.get(FEATURE_BUFFER_TANK, False)),
    }


def _build_iwr_setup_schema(
    zone_options: list[SelectOptionDict],
    preselected: list[str],
    features: dict[str, bool],
) -> vol.Schema:
    """Build a voluptuous schema for zone + feature selection."""
    return vol.Schema(
        {
            vol.Required("zones", default=preselected): SelectSelector(
                SelectSelectorConfig(
                    options=zone_options,
                    multiple=True,
                    mode=SelectSelectorMode.LIST,
                )
            ),
            vol.Required(
                FEATURE_HYBRID, default=features.get(FEATURE_HYBRID, False)
            ): bool,
            vol.Required(
                FEATURE_CASCADE, default=features.get(FEATURE_CASCADE, False)
            ): bool,
            vol.Required(
                FEATURE_COOLING, default=features.get(FEATURE_COOLING, False)
            ): bool,
            vol.Required(
                FEATURE_BUFFER_TANK,
                default=features.get(FEATURE_BUFFER_TANK, False),
            ): bool,
        }
    )


def _parse_zone_selection(user_input: dict[str, Any]) -> list[int]:
    """Parse zone selection from form input, returning sorted 1-based zone numbers."""
    return sorted(int(z) for z in user_input["zones"])


def _external_room_sensor_field(zone: int) -> str:
    """Return the config-flow field name for an external room sensor source."""
    return f"zone_{zone}_external_room_sensor"


def _external_room_sensor_aggregation_field(zone: int) -> str:
    """Return the config-flow field name for an external room sensor aggregation."""
    return f"zone_{zone}_external_room_sensor_aggregation"


def _external_room_sensor_write_interval_field(zone: int) -> str:
    """Return the config-flow field name for the external room sensor write interval."""
    return f"zone_{zone}_external_room_sensor_write_interval"


def _external_room_sensor_timeout_field(zone: int) -> str:
    """Return the config-flow field name for the external room sensor timeout."""
    return f"zone_{zone}_external_room_sensor_timeout"


def _external_room_sensor_area_filter_field() -> str:
    """Return the config-flow field name for the room prefilter."""
    return "external_room_sensor_area_filter"


def _external_room_sensor_text_filter_field() -> str:
    """Return the config-flow field name for the text prefilter."""
    return "external_room_sensor_text_filter"


def _heating_zones_from_details(
    zones: list[int], zone_details: dict[str, Any] | None
) -> list[int]:
    """Return only heating zones from the configured zone set."""
    zone_details = zone_details or {}
    return [
        zone
        for zone in zones
        if zone_details.get(str(zone), {}).get("role", ZONE_ROLE_HEATING)
        == ZONE_ROLE_HEATING
    ]


def _entity_area_name(hass, entity_id: str) -> str | None:
    """Resolve an entity to its Home Assistant area name when available."""
    entity_registry = er.async_get(hass)
    entity_entry = entity_registry.async_get(entity_id)
    if entity_entry is None:
        return None

    area_registry = ar.async_get(hass)
    if entity_entry.area_id:
        area_entry = area_registry.async_get_area(entity_entry.area_id)
        if area_entry is not None:
            return area_entry.name

    if entity_entry.device_id:
        device_registry = dr.async_get(hass)
        device_entry = device_registry.async_get(entity_entry.device_id)
        if device_entry is not None and device_entry.area_id:
            area_entry = area_registry.async_get_area(device_entry.area_id)
            if area_entry is not None:
                return area_entry.name

    return None


def _temperature_sensor_records(hass) -> list[dict[str, Any]]:
    """Return sorted temperature sensor records for selector building."""
    records: list[dict[str, Any]] = []
    for state in hass.states.async_all("sensor"):
        if state.attributes.get("device_class") != "temperature":
            continue
        try:
            value = float(state.state)
        except (TypeError, ValueError):
            continue
        friendly_name = state.attributes.get("friendly_name", state.entity_id)
        area_name = _entity_area_name(hass, state.entity_id)
        area_label = f"{area_name} - " if area_name else ""
        label = (
            f"{area_label}{friendly_name} ({state.entity_id}, {value:.2f} °C)"
        )
        records.append(
            {
                "value": value,
                "entity_id": state.entity_id,
                "friendly_name": friendly_name,
                "area_name": area_name,
                "option": SelectOptionDict(value=state.entity_id, label=label),
            }
        )
    records.sort(key=lambda item: (item["value"], item["entity_id"]))
    return records


def _area_filter_options(hass) -> list[SelectOptionDict]:
    """Build area prefilter options for temperature sensors."""
    area_names = sorted(
        {
            record["area_name"]
            for record in _temperature_sensor_records(hass)
            if record["area_name"]
        }
    )
    options = [SelectOptionDict(value=_ALL_AREAS_FILTER, label="Alle Räume")]
    options.extend(
        SelectOptionDict(value=area_name, label=area_name) for area_name in area_names
    )
    return options


def _filter_temperature_sensor_records(
    hass,
    area_filter: str,
    text_filter: str,
) -> list[dict[str, Any]]:
    """Return temperature sensor records filtered by area and free-text search."""
    text_filter = text_filter.strip().casefold()
    filtered: list[dict[str, Any]] = []

    for record in _temperature_sensor_records(hass):
        area_name = record["area_name"] or ""
        if area_filter != _ALL_AREAS_FILTER and area_name != area_filter:
            continue

        if text_filter:
            haystack = " ".join(
                (
                    record["entity_id"],
                    record["friendly_name"],
                    area_name,
                )
            ).casefold()
            if text_filter not in haystack:
                continue

        filtered.append(record)

    return filtered


def _build_external_room_sensor_filter_schema(
    hass,
    *,
    area_filter: str,
    text_filter: str,
) -> vol.Schema:
    """Build the prefilter form shown before the sensor selector."""
    return vol.Schema(
        {
            vol.Required(
                _external_room_sensor_area_filter_field(),
                default=area_filter,
            ): SelectSelector(
                SelectSelectorConfig(
                    options=_area_filter_options(hass),
                    multiple=False,
                    mode=SelectSelectorMode.LIST,
                )
            ),
            vol.Optional(
                _external_room_sensor_text_filter_field(),
                default=text_filter,
            ): str,
        }
    )


def _aggregation_options() -> list[SelectOptionDict]:
    """Return the selectable aggregation strategies."""
    return [
        SelectOptionDict(
            value=EXTERNAL_ROOM_SENSOR_AGGREGATION_AVERAGE,
            label="Durchschnitt",
        ),
        SelectOptionDict(value=EXTERNAL_ROOM_SENSOR_AGGREGATION_MIN, label="Minimum"),
        SelectOptionDict(value=EXTERNAL_ROOM_SENSOR_AGGREGATION_MAX, label="Maximum"),
    ]


def _build_external_room_sensor_schema(
    hass,
    zones: list[int],
    configured: dict[str, Any] | None,
    *,
    area_filter: str,
    text_filter: str,
) -> vol.Schema:
    """Build a schema for optional external room-temperature source entities."""
    configured = configured or {}
    filtered_records = _filter_temperature_sensor_records(
        hass,
        area_filter=area_filter,
        text_filter=text_filter,
    )
    temperature_options = [record["option"] for record in filtered_records]
    aggregation_options = _aggregation_options()
    schema: dict[Any, Any] = {}

    for zone in zones:
        zone_config = configured.get(str(zone), {})
        if isinstance(zone_config, str):
            zone_config = {
                CONF_EXTERNAL_ROOM_SENSOR_ENTITY_IDS: [zone_config],
                CONF_EXTERNAL_ROOM_SENSOR_AGGREGATION: EXTERNAL_ROOM_SENSOR_AGGREGATION_AVERAGE,
                CONF_EXTERNAL_ROOM_SENSOR_WRITE_INTERVAL: DEFAULT_EXTERNAL_ROOM_SENSOR_WRITE_INTERVAL,
                CONF_EXTERNAL_ROOM_SENSOR_TIMEOUT: DEFAULT_EXTERNAL_ROOM_SENSOR_TIMEOUT,
            }
        elif not isinstance(zone_config, dict):
            zone_config = {}

        schema[
            vol.Optional(
                _external_room_sensor_field(zone),
                default=zone_config.get(CONF_EXTERNAL_ROOM_SENSOR_ENTITY_IDS, []),
            )
        ] = SelectSelector(
            SelectSelectorConfig(
                options=temperature_options,
                multiple=True,
                mode=SelectSelectorMode.LIST,
            )
        )
        schema[
            vol.Optional(
                _external_room_sensor_aggregation_field(zone),
                default=zone_config.get(
                    CONF_EXTERNAL_ROOM_SENSOR_AGGREGATION,
                    EXTERNAL_ROOM_SENSOR_AGGREGATION_AVERAGE,
                ),
            )
        ] = SelectSelector(
            SelectSelectorConfig(
                options=aggregation_options,
                multiple=False,
                mode=SelectSelectorMode.LIST,
            )
        )
        schema[
            vol.Optional(
                _external_room_sensor_write_interval_field(zone),
                default=zone_config.get(
                    CONF_EXTERNAL_ROOM_SENSOR_WRITE_INTERVAL,
                    DEFAULT_EXTERNAL_ROOM_SENSOR_WRITE_INTERVAL,
                ),
            )
        ] = vol.All(int, vol.Range(min=15, max=3600))
        schema[
            vol.Optional(
                _external_room_sensor_timeout_field(zone),
                default=zone_config.get(
                    CONF_EXTERNAL_ROOM_SENSOR_TIMEOUT,
                    DEFAULT_EXTERNAL_ROOM_SENSOR_TIMEOUT,
                ),
            )
        ] = vol.All(int, vol.Range(min=300, max=86400))

    return vol.Schema(schema)


def _parse_external_room_sensor_selection(
    zones: list[int], user_input: dict[str, Any]
) -> dict[str, dict[str, Any]]:
    """Normalize external room sensor selections from a flow form."""
    selected: dict[str, dict[str, Any]] = {}
    for zone in zones:
        raw_entities = user_input.get(_external_room_sensor_field(zone), [])
        if isinstance(raw_entities, str):
            raw_entities = [raw_entities]
        if not isinstance(raw_entities, list):
            continue

        entity_ids = [
            entity_id.strip()
            for entity_id in raw_entities
            if isinstance(entity_id, str) and entity_id.strip()
        ]
        if not entity_ids:
            continue

        aggregation = user_input.get(
            _external_room_sensor_aggregation_field(zone),
            EXTERNAL_ROOM_SENSOR_AGGREGATION_AVERAGE,
        )
        if aggregation not in {
            EXTERNAL_ROOM_SENSOR_AGGREGATION_AVERAGE,
            EXTERNAL_ROOM_SENSOR_AGGREGATION_MIN,
            EXTERNAL_ROOM_SENSOR_AGGREGATION_MAX,
        }:
            aggregation = EXTERNAL_ROOM_SENSOR_AGGREGATION_AVERAGE

        selected[str(zone)] = {
            CONF_EXTERNAL_ROOM_SENSOR_ENTITY_IDS: entity_ids,
            CONF_EXTERNAL_ROOM_SENSOR_AGGREGATION: aggregation,
            CONF_EXTERNAL_ROOM_SENSOR_WRITE_INTERVAL: int(
                user_input.get(
                    _external_room_sensor_write_interval_field(zone),
                    DEFAULT_EXTERNAL_ROOM_SENSOR_WRITE_INTERVAL,
                )
            ),
            CONF_EXTERNAL_ROOM_SENSOR_TIMEOUT: int(
                user_input.get(
                    _external_room_sensor_timeout_field(zone),
                    DEFAULT_EXTERNAL_ROOM_SENSOR_TIMEOUT,
                )
            ),
        }
    return selected


# ---------------------------------------------------------------------------
# Options flow
# ---------------------------------------------------------------------------


class BroetjeOptionsFlow(OptionsFlow):
    """Handle options for Brötje Heatpump."""

    def __init__(self) -> None:
        """Initialize options flow."""
        self._zone_options: list[SelectOptionDict] = []
        self._preselected: list[str] = []
        self._detected_setup: dict[str, Any] | None = None
        self._selected_zones: list[int] = []
        self._external_room_sensor_area_filter: str = _ALL_AREAS_FILTER
        self._external_room_sensor_text_filter: str = ""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Entry point: show menu for IWR, or go straight to general for ISR."""
        device_type = self.config_entry.data.get(CONF_DEVICE_TYPE)
        if device_type == DeviceType.IWR.value:
            return self.async_show_menu(
                step_id="init",
                menu_options=["general", "zone_config", "external_room_sensors"],
            )
        return await self.async_step_general(user_input)

    async def async_step_general(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage polling profile interval options."""
        if user_input is not None:
            return self.async_create_entry(
                data={**self.config_entry.options, **user_input}
            )

        fast_interval = self.config_entry.options.get(
            CONF_SCAN_INTERVAL_FAST, DEFAULT_SCAN_INTERVAL_FAST
        )
        normal_interval = self.config_entry.options.get(
            CONF_SCAN_INTERVAL_NORMAL,
            self.config_entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )
        slow_interval = self.config_entry.options.get(
            CONF_SCAN_INTERVAL_SLOW, DEFAULT_SCAN_INTERVAL_SLOW
        )

        return self.async_show_form(
            step_id="general",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SCAN_INTERVAL_FAST, default=fast_interval
                    ): vol.All(
                        int, vol.Range(min=10, max=3600)
                    ),
                    vol.Required(
                        CONF_SCAN_INTERVAL_NORMAL, default=normal_interval
                    ): vol.All(
                        int, vol.Range(min=10, max=3600)
                    ),
                    vol.Required(
                        CONF_SCAN_INTERVAL_SLOW, default=slow_interval
                    ): vol.All(
                        int, vol.Range(min=10, max=3600)
                    ),
                }
            ),
        )

    async def async_step_zone_config(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Zone configuration sub-menu: autodetect or manual."""
        return self.async_show_menu(
            step_id="zone_config",
            menu_options=["zones_auto", "zones_manual"],
        )

    async def async_step_zones_auto(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Autodetect zones via the running coordinator."""
        if user_input is not None:
            return await self._async_save_iwr_setup(user_input)

        coordinator = self.config_entry.runtime_data
        await coordinator._connect()
        self._detected_setup = await detect_iwr_setup(
            coordinator._client, coordinator._unit_id
        )
        zone_info = self._detected_setup["zone_info"]

        self._zone_options = [
            SelectOptionDict(value=str(z["zone"]), label=z["label"]) for z in zone_info
        ]
        self._preselected = [str(z) for z in self._detected_setup[CONF_ZONES]]

        return self.async_show_form(
            step_id="zones_auto",
            data_schema=_build_iwr_setup_schema(
                self._zone_options,
                self._preselected,
                _normalize_feature_selection(self._detected_setup["features"]),
            ),
        )

    async def async_step_zones_manual(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manually select zones with current zones pre-checked."""
        if user_input is not None:
            return await self._async_save_iwr_setup(user_input)

        coordinator = self.config_entry.runtime_data
        try:
            await coordinator._connect()
            self._detected_setup = await detect_iwr_setup(
                coordinator._client, coordinator._unit_id
            )
        except Exception:
            _LOGGER.exception("Manual IWR setup detection failed")
            self._detected_setup = {
                "zone_info": [],
                CONF_ZONES: self.config_entry.data.get(CONF_ZONES, [1]),
                "features": self.config_entry.data.get(CONF_IWR_FEATURES, {}),
                "zone_details": self.config_entry.data.get(CONF_IWR_ZONE_DETAILS, {}),
            }

        current_zones = self.config_entry.data.get(CONF_ZONES, self._detected_setup[CONF_ZONES])
        self._zone_options = [
            SelectOptionDict(value=str(z), label=f"Zone {z}") for z in range(1, 13)
        ]
        self._preselected = [str(z) for z in current_zones]

        return self.async_show_form(
            step_id="zones_manual",
            data_schema=_build_iwr_setup_schema(
                self._zone_options,
                self._preselected,
                _normalize_feature_selection(
                    self._detected_setup["features"]
                    or self.config_entry.data.get(CONF_IWR_FEATURES, {})
                ),
            ),
        )

    async def _async_save_iwr_setup(
        self, user_input: dict[str, Any]
    ) -> ConfigFlowResult:
        """Save selected zones and feature groups to entry.data and reload."""
        zones = _parse_zone_selection(user_input)
        features = _normalize_feature_selection(user_input)
        zone_details = (self._detected_setup or {}).get(
            "zone_details", self.config_entry.data.get(CONF_IWR_ZONE_DETAILS, {})
        )
        new_data = {
            **self.config_entry.data,
            CONF_ZONES: zones,
            CONF_IWR_FEATURES: features,
            CONF_IWR_FEATURES_SOURCE: IWR_FEATURES_SOURCE_MANUAL,
            CONF_IWR_ZONE_DETAILS: zone_details,
        }
        self.hass.config_entries.async_update_entry(self.config_entry, data=new_data)
        self.hass.async_create_task(
            self.hass.config_entries.async_reload(self.config_entry.entry_id)
        )
        return self.async_create_entry(data=self.config_entry.options)

    async def async_step_external_room_sensors(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Collect prefilters before showing the room-sensor selector."""
        zone_details = self.config_entry.data.get(CONF_IWR_ZONE_DETAILS, {})
        zones = _heating_zones_from_details(
            sorted(self.config_entry.data.get(CONF_ZONES, [])),
            zone_details,
        )
        configured = self.config_entry.options.get(
            CONF_EXTERNAL_ROOM_SENSORS,
            self.config_entry.data.get(CONF_EXTERNAL_ROOM_SENSORS, {}),
        )

        if not zones:
            new_options = {
                **self.config_entry.options,
                CONF_EXTERNAL_ROOM_SENSORS: {},
            }
            self.hass.config_entries.async_update_entry(
                self.config_entry, options=new_options
            )
            return self.async_create_entry(data=new_options)

        if user_input is not None:
            self._external_room_sensor_area_filter = user_input.get(
                _external_room_sensor_area_filter_field(),
                _ALL_AREAS_FILTER,
            )
            self._external_room_sensor_text_filter = user_input.get(
                _external_room_sensor_text_filter_field(),
                "",
            ).strip()
            return await self.async_step_external_room_sensors_select()

        return self.async_show_form(
            step_id="external_room_sensors",
            data_schema=_build_external_room_sensor_filter_schema(
                self.hass,
                area_filter=self._external_room_sensor_area_filter,
                text_filter=self._external_room_sensor_text_filter,
            ),
        )

    async def async_step_external_room_sensors_select(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Configure optional Home Assistant source entities for room-temperature sync."""
        zone_details = self.config_entry.data.get(CONF_IWR_ZONE_DETAILS, {})
        zones = _heating_zones_from_details(
            sorted(self.config_entry.data.get(CONF_ZONES, [])),
            zone_details,
        )
        configured = self.config_entry.options.get(
            CONF_EXTERNAL_ROOM_SENSORS,
            self.config_entry.data.get(CONF_EXTERNAL_ROOM_SENSORS, {}),
        )

        if user_input is not None:
            new_options = {
                **self.config_entry.options,
                CONF_EXTERNAL_ROOM_SENSORS: _parse_external_room_sensor_selection(
                    zones, user_input
                ),
            }
            self.hass.config_entries.async_update_entry(
                self.config_entry, options=new_options
            )
            self.hass.async_create_task(
                self.hass.config_entries.async_reload(self.config_entry.entry_id)
            )
            return self.async_create_entry(data=new_options)

        if not _filter_temperature_sensor_records(
            self.hass,
            area_filter=self._external_room_sensor_area_filter,
            text_filter=self._external_room_sensor_text_filter,
        ):
            return self.async_show_form(
                step_id="external_room_sensors",
                data_schema=_build_external_room_sensor_filter_schema(
                    self.hass,
                    area_filter=self._external_room_sensor_area_filter,
                    text_filter=self._external_room_sensor_text_filter,
                ),
                errors={"base": "no_matching_temperature_sensors"},
            )

        return self.async_show_form(
            step_id="external_room_sensors_select",
            data_schema=_build_external_room_sensor_schema(
                self.hass,
                zones,
                configured,
                area_filter=self._external_room_sensor_area_filter,
                text_filter=self._external_room_sensor_text_filter,
            ),
        )


# ---------------------------------------------------------------------------
# Config flow
# ---------------------------------------------------------------------------


class BroetjeHeatpumpConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Brötje Heatpump."""

    VERSION = 3
    MINOR_VERSION = 6

    @staticmethod
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> BroetjeOptionsFlow:
        """Get the options flow handler."""
        return BroetjeOptionsFlow()

    def __init__(self) -> None:
        """Initialize the flow."""
        self._device_type: DeviceType | None = None
        self._connection_data: dict[str, Any] = {}
        self._zone_options: list[SelectOptionDict] = []
        self._preselected: list[str] = []
        self._detected_setup: dict[str, Any] | None = None
        self._selected_zones: list[int] = []
        self._external_room_sensor_area_filter: str = _ALL_AREAS_FILTER
        self._external_room_sensor_text_filter: str = ""

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle device type selection via menu."""
        return self.async_show_menu(
            step_id="user",
            menu_options=["isr", "iwr"],
        )

    async def async_step_isr(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle ISR connection setup."""
        self._device_type = DeviceType.ISR
        return await self._async_step_connection(user_input)

    async def async_step_iwr(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle IWR connection setup."""
        self._device_type = DeviceType.IWR
        return await self._async_step_connection(user_input)

    async def _async_step_connection(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle connection details (shared by ISR and IWR steps)."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                await self._test_connection(
                    user_input[CONF_HOST],
                    user_input[CONF_PORT],
                    user_input[CONF_UNIT_ID],
                )
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                if self._device_type == DeviceType.IWR:
                    self._connection_data = user_input
                    return await self.async_step_iwr_zone_method()

                return await self._async_create_entry(user_input)

        return self.async_show_form(
            step_id=self._device_type.value,
            data_schema=STEP_CONNECTION_DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_iwr_zone_method(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Zone configuration method menu: autodetect or manual."""
        return self.async_show_menu(
            step_id="iwr_zone_method",
            menu_options=["iwr_zones_auto", "iwr_zones_manual"],
        )

    async def async_step_iwr_zones_auto(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Autodetect zones and present multi-select with pre-checked active zones."""
        if user_input is not None:
            self._selected_zones = _parse_zone_selection(user_input)
            self._connection_data[CONF_ZONES] = self._selected_zones
            self._connection_data[CONF_IWR_FEATURES] = _normalize_feature_selection(
                user_input
            )
            self._connection_data[CONF_IWR_FEATURES_SOURCE] = (
                IWR_FEATURES_SOURCE_MANUAL
            )
            if self._detected_setup is not None:
                self._connection_data[CONF_IWR_ZONE_DETAILS] = self._detected_setup[
                    "zone_details"
                ]
            return await self.async_step_iwr_external_room_sensors()

        from pymodbus.client import AsyncModbusTcpClient

        client = AsyncModbusTcpClient(
            host=self._connection_data[CONF_HOST],
            port=self._connection_data[CONF_PORT],
        )
        try:
            connected = await client.connect()
            if not connected:
                _LOGGER.error("Zone detection: failed to connect to Modbus device")
            self._detected_setup = await detect_iwr_setup(
                client, self._connection_data[CONF_UNIT_ID]
            )
        finally:
            client.close()

        zone_info = self._detected_setup["zone_info"]
        self._zone_options = [
            SelectOptionDict(value=str(z["zone"]), label=z["label"]) for z in zone_info
        ]
        self._preselected = [str(z) for z in self._detected_setup[CONF_ZONES]]

        return self.async_show_form(
            step_id="iwr_zones_auto",
            data_schema=_build_iwr_setup_schema(
                self._zone_options,
                self._preselected,
                _normalize_feature_selection(self._detected_setup["features"]),
            ),
        )

    async def async_step_iwr_zones_manual(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manually select zones from all 12 options."""
        if user_input is not None:
            self._selected_zones = _parse_zone_selection(user_input)
            self._connection_data[CONF_ZONES] = self._selected_zones
            self._connection_data[CONF_IWR_FEATURES] = _normalize_feature_selection(
                user_input
            )
            self._connection_data[CONF_IWR_FEATURES_SOURCE] = (
                IWR_FEATURES_SOURCE_MANUAL
            )
            if self._detected_setup is not None:
                self._connection_data[CONF_IWR_ZONE_DETAILS] = self._detected_setup[
                    "zone_details"
                ]
            return await self.async_step_iwr_external_room_sensors()

        from pymodbus.client import AsyncModbusTcpClient

        client = AsyncModbusTcpClient(
            host=self._connection_data[CONF_HOST],
            port=self._connection_data[CONF_PORT],
        )
        try:
            connected = await client.connect()
            if connected:
                self._detected_setup = await detect_iwr_setup(
                    client, self._connection_data[CONF_UNIT_ID]
                )
        finally:
            client.close()

        self._zone_options = [
            SelectOptionDict(value=str(z), label=f"Zone {z}") for z in range(1, 13)
        ]

        return self.async_show_form(
            step_id="iwr_zones_manual",
            data_schema=_build_iwr_setup_schema(
                self._zone_options,
                [str(z) for z in (self._detected_setup or {}).get(CONF_ZONES, [])],
                _normalize_feature_selection(
                    (self._detected_setup or {}).get("features", {})
                ),
            ),
        )

    async def async_step_iwr_external_room_sensors(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Collect prefilters before showing the room-sensor selector."""
        zones = self._selected_zones or self._connection_data.get(CONF_ZONES, [])
        zone_details = self._connection_data.get(CONF_IWR_ZONE_DETAILS, {})
        heating_zones = _heating_zones_from_details(zones, zone_details)
        configured = self._connection_data.get(CONF_EXTERNAL_ROOM_SENSORS, {})

        if not heating_zones:
            self._connection_data[CONF_EXTERNAL_ROOM_SENSORS] = {}
            return await self._async_create_entry(self._connection_data)

        if user_input is not None:
            self._external_room_sensor_area_filter = user_input.get(
                _external_room_sensor_area_filter_field(),
                _ALL_AREAS_FILTER,
            )
            self._external_room_sensor_text_filter = user_input.get(
                _external_room_sensor_text_filter_field(),
                "",
            ).strip()
            return await self.async_step_iwr_external_room_sensors_select()

        return self.async_show_form(
            step_id="iwr_external_room_sensors",
            data_schema=_build_external_room_sensor_filter_schema(
                self.hass,
                area_filter=self._external_room_sensor_area_filter,
                text_filter=self._external_room_sensor_text_filter,
            ),
        )

    async def async_step_iwr_external_room_sensors_select(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Configure optional Home Assistant sensor sources during initial setup."""
        zones = self._selected_zones or self._connection_data.get(CONF_ZONES, [])
        zone_details = self._connection_data.get(CONF_IWR_ZONE_DETAILS, {})
        heating_zones = _heating_zones_from_details(zones, zone_details)
        configured = self._connection_data.get(CONF_EXTERNAL_ROOM_SENSORS, {})

        if user_input is not None:
            self._connection_data[CONF_EXTERNAL_ROOM_SENSORS] = (
                _parse_external_room_sensor_selection(heating_zones, user_input)
            )
            return await self._async_create_entry(self._connection_data)

        if not _filter_temperature_sensor_records(
            self.hass,
            area_filter=self._external_room_sensor_area_filter,
            text_filter=self._external_room_sensor_text_filter,
        ):
            return self.async_show_form(
                step_id="iwr_external_room_sensors",
                data_schema=_build_external_room_sensor_filter_schema(
                    self.hass,
                    area_filter=self._external_room_sensor_area_filter,
                    text_filter=self._external_room_sensor_text_filter,
                ),
                errors={"base": "no_matching_temperature_sensors"},
            )

        return self.async_show_form(
            step_id="iwr_external_room_sensors_select",
            data_schema=_build_external_room_sensor_schema(
                self.hass,
                heating_zones,
                configured,
                area_filter=self._external_room_sensor_area_filter,
                text_filter=self._external_room_sensor_text_filter,
            ),
        )

    async def _async_create_entry(
        self, connection_data: dict[str, Any]
    ) -> ConfigFlowResult:
        """Create a config entry from validated connection data."""
        device_type = self._device_type.value
        unique_id = f"broetje_{device_type}_{connection_data[CONF_HOST]}_{connection_data[CONF_UNIT_ID]}"
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()

        model_name = DEVICE_MODELS[self._device_type]
        data = {**connection_data, CONF_DEVICE_TYPE: device_type}

        return self.async_create_entry(
            title=f"Brötje {model_name} ({connection_data[CONF_HOST]})",
            data=data,
        )

    async def _test_connection(self, host: str, port: int, unit_id: int) -> None:
        """Test if we can connect to the Modbus device."""
        from pymodbus.client import AsyncModbusTcpClient

        client = AsyncModbusTcpClient(host=host, port=port)

        try:
            _LOGGER.debug("Attempting to connect to %s:%s", host, port)

            connected = await client.connect()
            if not connected:
                _LOGGER.error("Failed to connect to %s:%s", host, port)
                raise CannotConnect(f"Failed to connect to {host}:{port}")

            _LOGGER.info("Connection test successful for %s:%s", host, port)

        except OSError as err:
            _LOGGER.error("OS error during connection test: %s", err)
            raise CannotConnect(str(err)) from err
        finally:
            client.close()
