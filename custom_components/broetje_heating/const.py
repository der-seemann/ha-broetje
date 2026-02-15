"""Constants for the Brötje Heatpump integration."""

from typing import Final

DOMAIN: Final = "broetje_heating"

# Default values
DEFAULT_PORT: Final = 502
DEFAULT_UNIT_ID: Final = 1
DEFAULT_SCAN_INTERVAL: Final = 120

# Configuration keys
CONF_UNIT_ID: Final = "unit_id"
CONF_SCAN_INTERVAL: Final = "scan_interval"

# Manufacturer info
MANUFACTURER: Final = "Brötje"

# Register types
REG_INPUT: Final = "input"
REG_HOLDING: Final = "holding"

# Scale factors from Brötje ISR documentation
SCALE_TEMP: Final = 1 / 64  # 0.015625 - for temperature values
SCALE_CURVE: Final = 1 / 50  # 0.02 - for heating curve slope
SCALE_POWER: Final = 1 / 10  # 0.1 - for power in kW
SCALE_PERCENT_100: Final = 1 / 100  # 0.01 - for percentages scaled by 100
SCALE_HOURS: Final = 1 / 3600  # for hours stored as seconds
