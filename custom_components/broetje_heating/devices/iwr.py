"""IWR/GTW-08 device register and sensor definitions."""

from __future__ import annotations

from typing import Final

from ..const import (  # noqa: F401
    REG_HOLDING,
    REG_INPUT,
    SCALE_CURVE,
    SCALE_HOURS,
    SCALE_PERCENT_100,
    SCALE_POWER,
    SCALE_TEMP,
)

# Modbus register map for IWR/GTW-08
# Populate with IWR-specific register definitions
IWR_REGISTER_MAP: Final = {}

# Sensor definitions for IWR/GTW-08
# Populate with IWR-specific sensor definitions
IWR_SENSORS: Final = {}

# Binary sensor definitions for IWR/GTW-08
# Populate with IWR-specific binary sensor definitions
IWR_BINARY_SENSORS: Final = {}
