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
from homeassistant.helpers.selector import (
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_IWR_FEATURES,
    CONF_IWR_FEATURES_SOURCE,
    CONF_IWR_ZONE_DETAILS,
    CONF_SCAN_INTERVAL,
    CONF_SCAN_INTERVAL_FAST,
    CONF_SCAN_INTERVAL_NORMAL,
    CONF_SCAN_INTERVAL_SLOW,
    CONF_UNIT_ID,
    CONF_ZONES,
    DEFAULT_PORT,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL_FAST,
    DEFAULT_SCAN_INTERVAL_SLOW,
    DEFAULT_UNIT_ID,
    DOMAIN,
    FEATURE_BUFFER_TANK,
    FEATURE_CASCADE,
    FEATURE_COOLING,
    FEATURE_HYBRID,
    IWR_FEATURES_SOURCE_MANUAL,
)
from .devices import CONF_DEVICE_TYPE, DEVICE_MODELS, DeviceType
from .iwr_setup import detect_iwr_setup

_LOGGER = logging.getLogger(__name__)

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

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Entry point: show menu for IWR, or go straight to general for ISR."""
        device_type = self.config_entry.data.get(CONF_DEVICE_TYPE)
        if device_type == DeviceType.IWR.value:
            return self.async_show_menu(
                step_id="init",
                menu_options=["general", "zone_config"],
            )
        return await self.async_step_general(user_input)

    async def async_step_general(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage polling profile interval options."""
        if user_input is not None:
            return self.async_create_entry(data=user_input)

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


# ---------------------------------------------------------------------------
# Config flow
# ---------------------------------------------------------------------------


class BroetjeHeatpumpConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Brötje Heatpump."""

    VERSION = 3
    MINOR_VERSION = 4

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
            self._connection_data[CONF_ZONES] = _parse_zone_selection(user_input)
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
            return await self._async_create_entry(self._connection_data)

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
            self._connection_data[CONF_ZONES] = _parse_zone_selection(user_input)
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
            return await self._async_create_entry(self._connection_data)

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
