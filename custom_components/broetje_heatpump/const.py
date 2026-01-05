"""Constants for the Brötje Heatpump integration."""

from typing import Final

DOMAIN: Final = "broetje_heatpump"

# Default values
DEFAULT_PORT: Final = 502
DEFAULT_UNIT_ID: Final = 1
DEFAULT_SCAN_INTERVAL: Final = 30

# Configuration keys
CONF_UNIT_ID: Final = "unit_id"

# Manufacturer info
MANUFACTURER: Final = "Brötje"
DEFAULT_MODEL: Final = "Heatpump"

# Register types
REG_INPUT: Final = "input"
REG_HOLDING: Final = "holding"

# Modbus register map
# TODO: Populate from Brötje Modbus documentation
# Format: "key": {"address": int, "type": str, "count": int, "scale": float, "data_type": str}
REGISTER_MAP: Final = {
    # Device identification registers (placeholder addresses)
    # "serial_number": {"address": 0, "type": REG_INPUT, "count": 4, "data_type": "string"},
    # "model": {"address": 4, "type": REG_INPUT, "count": 8, "data_type": "string"},
    # "firmware_version": {"address": 12, "type": REG_INPUT, "count": 2, "data_type": "string"},
    
    # Sensor registers (placeholder addresses - to be updated from PDF)
    # "outdoor_temp": {"address": 100, "type": REG_INPUT, "count": 1, "scale": 0.1, "data_type": "int16"},
    # "flow_temp": {"address": 101, "type": REG_INPUT, "count": 1, "scale": 0.1, "data_type": "int16"},
    # "return_temp": {"address": 102, "type": REG_INPUT, "count": 1, "scale": 0.1, "data_type": "int16"},
    # "dhw_temp": {"address": 103, "type": REG_INPUT, "count": 1, "scale": 0.1, "data_type": "int16"},
    # "system_pressure": {"address": 104, "type": REG_INPUT, "count": 1, "scale": 0.01, "data_type": "uint16"},
    
    # Binary sensor registers (placeholder addresses - to be updated from PDF)
    # "compressor_running": {"address": 200, "type": REG_INPUT, "count": 1, "bit": 0, "data_type": "bool"},
    # "defrost_active": {"address": 200, "type": REG_INPUT, "count": 1, "bit": 1, "data_type": "bool"},
    # "dhw_demand": {"address": 200, "type": REG_INPUT, "count": 1, "bit": 2, "data_type": "bool"},
    # "error_state": {"address": 201, "type": REG_INPUT, "count": 1, "bit": 0, "data_type": "bool"},
}

# Sensor definitions
# Format: "key": {"register": str, "device_class": str, "unit": str, "icon": str}
SENSORS: Final = {
    # "outdoor_temp": {
    #     "register": "outdoor_temp",
    #     "translation_key": "outdoor_temperature",
    #     "device_class": "temperature",
    #     "unit": "°C",
    #     "state_class": "measurement",
    # },
    # "flow_temp": {
    #     "register": "flow_temp",
    #     "translation_key": "flow_temperature",
    #     "device_class": "temperature",
    #     "unit": "°C",
    #     "state_class": "measurement",
    # },
    # "return_temp": {
    #     "register": "return_temp",
    #     "translation_key": "return_temperature",
    #     "device_class": "temperature",
    #     "unit": "°C",
    #     "state_class": "measurement",
    # },
    # "dhw_temp": {
    #     "register": "dhw_temp",
    #     "translation_key": "dhw_temperature",
    #     "device_class": "temperature",
    #     "unit": "°C",
    #     "state_class": "measurement",
    # },
    # "system_pressure": {
    #     "register": "system_pressure",
    #     "translation_key": "system_pressure",
    #     "device_class": "pressure",
    #     "unit": "bar",
    #     "state_class": "measurement",
    # },
}

# Binary sensor definitions
BINARY_SENSORS: Final = {
    # "compressor_running": {
    #     "register": "compressor_running",
    #     "translation_key": "compressor_running",
    #     "device_class": "running",
    # },
    # "defrost_active": {
    #     "register": "defrost_active",
    #     "translation_key": "defrost_active",
    #     "device_class": None,
    #     "icon": "mdi:snowflake-melt",
    # },
    # "dhw_demand": {
    #     "register": "dhw_demand",
    #     "translation_key": "dhw_demand",
    #     "device_class": None,
    #     "icon": "mdi:water-boiler",
    # },
    # "error_state": {
    #     "register": "error_state",
    #     "translation_key": "error_state",
    #     "device_class": "problem",
    # },
}
