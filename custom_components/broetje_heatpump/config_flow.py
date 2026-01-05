"""Config flow for Brötje Heatpump integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_PORT

from .const import (
    CONF_UNIT_ID,
    DEFAULT_PORT,
    DEFAULT_UNIT_ID,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
        vol.Required(CONF_UNIT_ID, default=DEFAULT_UNIT_ID): int,
    }
)


class CannotConnect(Exception):
    """Error to indicate we cannot connect."""


class BroetjeHeatpumpConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Brötje Heatpump."""

    VERSION = 1
    MINOR_VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
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
                # Generate unique ID from host (will be replaced with serial if available)
                unique_id = f"broetje_{user_input[CONF_HOST]}_{user_input[CONF_UNIT_ID]}"
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=f"Brötje Heatpump ({user_input[CONF_HOST]})",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def _test_connection(self, host: str, port: int, unit_id: int) -> None:
        """Test if we can connect to the Modbus device."""
        client = AsyncModbusTcpClient(host=host, port=port)
        
        try:
            if not await client.connect():
                raise CannotConnect(f"Failed to connect to {host}:{port}")
            
            # Try to read a register to verify communication
            # Using input register 0 as a basic connectivity test
            result = await client.read_input_registers(
                address=0,
                count=1,
                slave=unit_id,
            )
            
            if result.isError():
                _LOGGER.warning("Modbus read error during connection test: %s", result)
                # Connection works but register read failed - might be wrong unit_id
                # We still allow setup as register addresses may differ
                
        except ModbusException as err:
            _LOGGER.error("Modbus exception during connection test: %s", err)
            raise CannotConnect(str(err)) from err
        finally:
            client.close()
