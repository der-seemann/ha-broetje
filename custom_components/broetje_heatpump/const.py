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

# Scale factors from Brötje documentation
SCALE_TEMP: Final = 1 / 64  # 0.015625 - for temperature values
SCALE_CURVE: Final = 1 / 50  # 0.02 - for heating curve slope

# Operating mode enumeration (Betriebsart)
OPERATING_MODES: Final = {
    0: "protection",  # Schutzbetrieb
    1: "auto",        # Automatik
    2: "reduced",     # Reduziert
    3: "comfort",     # Komfort
}

# Modbus register map from Brötje documentation
# Heizkreis 1 (Heating Circuit 1)
REGISTER_MAP: Final = {
    # Operating mode - Register 1024
    "hc1_operating_mode": {
        "address": 1024,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    # Comfort setpoint - Register 1025
    "hc1_comfort_setpoint": {
        "address": 1025,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": SCALE_TEMP,
    },
    # Reduced setpoint - Register 1026
    "hc1_reduced_setpoint": {
        "address": 1026,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": SCALE_TEMP,
    },
    # Frost protection setpoint - Register 1027
    "hc1_frost_protection_setpoint": {
        "address": 1027,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": SCALE_TEMP,
    },
    # Heating curve slope - Register 1028
    "hc1_heating_curve_slope": {
        "address": 1028,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": SCALE_CURVE,
    },
    # Heating curve offset - Register 1029
    "hc1_heating_curve_offset": {
        "address": 1029,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": SCALE_TEMP,
    },
    # Summer/Winter threshold - Register 1030
    "hc1_summer_winter_threshold": {
        "address": 1030,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": SCALE_TEMP,
    },
    # Day heating threshold - Register 1032
    "hc1_day_heating_threshold": {
        "address": 1032,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": SCALE_TEMP,
    },
    # Flow setpoint minimum - Register 1034
    "hc1_flow_setpoint_min": {
        "address": 1034,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": SCALE_TEMP,
    },
    # Flow setpoint maximum - Register 1035
    "hc1_flow_setpoint_max": {
        "address": 1035,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": SCALE_TEMP,
    },
    # Flow setpoint room thermostat - Register 1036
    "hc1_flow_setpoint_room_thermostat": {
        "address": 1036,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": SCALE_TEMP,
    },
    # Room influence - Register 1038
    "hc1_room_influence": {
        "address": 1038,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    # Room temperature 1 - Register 1042 (read-only)
    "hc1_room_temperature": {
        "address": 1042,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": SCALE_TEMP,
    },
    # Room setpoint 1 - Register 1044 (read-only)
    "hc1_room_setpoint": {
        "address": 1044,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": SCALE_TEMP,
    },
    # Flow temperature 1 - Register 1046 (read-only)
    "hc1_flow_temperature": {
        "address": 1046,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": SCALE_TEMP,
    },
    # Flow setpoint 1 - Register 1048 (read-only)
    "hc1_flow_setpoint": {
        "address": 1048,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": SCALE_TEMP,
    },
    # Room thermostat demand - Register 1050 (read-only)
    "hc1_room_thermostat_demand": {
        "address": 1050,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    # Heating circuit status - Register 1054 (read-only)
    "hc1_status": {
        "address": 1054,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    # Heating circuit on/off - Register 1055
    "hc1_enabled": {
        "address": 1055,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    # Mixer boost - Register 1077
    "hc1_mixer_boost": {
        "address": 1077,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": SCALE_TEMP,
    },
    # Heating circuit pump 1 - Register 1095 (read-only)
    "hc1_pump": {
        "address": 1095,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    # Mixer open - Register 1097 (read-only)
    "hc1_mixer_open": {
        "address": 1097,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    # Mixer close - Register 1099 (read-only)
    "hc1_mixer_close": {
        "address": 1099,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    # Pump speed - Register 1101 (read-only)
    "hc1_pump_speed": {
        "address": 1101,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    # Pump speed minimum - Register 1128
    "hc1_pump_speed_min": {
        "address": 1128,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    # Pump speed maximum - Register 1129
    "hc1_pump_speed_max": {
        "address": 1129,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
}

# Sensor definitions
SENSORS: Final = {
    "hc1_comfort_setpoint": {
        "register": "hc1_comfort_setpoint",
        "translation_key": "hc1_comfort_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
    },
    "hc1_reduced_setpoint": {
        "register": "hc1_reduced_setpoint",
        "translation_key": "hc1_reduced_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
    },
    "hc1_frost_protection_setpoint": {
        "register": "hc1_frost_protection_setpoint",
        "translation_key": "hc1_frost_protection_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
    },
    "hc1_heating_curve_slope": {
        "register": "hc1_heating_curve_slope",
        "translation_key": "hc1_heating_curve_slope",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:chart-line",
    },
    "hc1_heating_curve_offset": {
        "register": "hc1_heating_curve_offset",
        "translation_key": "hc1_heating_curve_offset",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
    },
    "hc1_summer_winter_threshold": {
        "register": "hc1_summer_winter_threshold",
        "translation_key": "hc1_summer_winter_threshold",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
    },
    "hc1_day_heating_threshold": {
        "register": "hc1_day_heating_threshold",
        "translation_key": "hc1_day_heating_threshold",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
    },
    "hc1_flow_setpoint_min": {
        "register": "hc1_flow_setpoint_min",
        "translation_key": "hc1_flow_setpoint_min",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
    },
    "hc1_operating_mode": {
        "register": "hc1_operating_mode",
        "translation_key": "hc1_operating_mode",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:thermostat",
    },
    "hc1_flow_setpoint_max": {
        "register": "hc1_flow_setpoint_max",
        "translation_key": "hc1_flow_setpoint_max",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
    },
    "hc1_flow_setpoint_room_thermostat": {
        "register": "hc1_flow_setpoint_room_thermostat",
        "translation_key": "hc1_flow_setpoint_room_thermostat",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
    },
    "hc1_room_influence": {
        "register": "hc1_room_influence",
        "translation_key": "hc1_room_influence",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:home-thermometer",
    },
    "hc1_room_temperature": {
        "register": "hc1_room_temperature",
        "translation_key": "hc1_room_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
    },
    "hc1_room_setpoint": {
        "register": "hc1_room_setpoint",
        "translation_key": "hc1_room_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
    },
    "hc1_flow_temperature": {
        "register": "hc1_flow_temperature",
        "translation_key": "hc1_flow_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
    },
    "hc1_flow_setpoint": {
        "register": "hc1_flow_setpoint",
        "translation_key": "hc1_flow_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
    },
    "hc1_status": {
        "register": "hc1_status",
        "translation_key": "hc1_status",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:information-outline",
    },
    "hc1_mixer_boost": {
        "register": "hc1_mixer_boost",
        "translation_key": "hc1_mixer_boost",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
    },
    "hc1_pump_speed": {
        "register": "hc1_pump_speed",
        "translation_key": "hc1_pump_speed",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:pump",
    },
    "hc1_pump_speed_min": {
        "register": "hc1_pump_speed_min",
        "translation_key": "hc1_pump_speed_min",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:pump",
    },
    "hc1_pump_speed_max": {
        "register": "hc1_pump_speed_max",
        "translation_key": "hc1_pump_speed_max",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:pump",
    },
}

# Binary sensor definitions
BINARY_SENSORS: Final = {
    "hc1_room_thermostat_demand": {
        "register": "hc1_room_thermostat_demand",
        "translation_key": "hc1_room_thermostat_demand",
        "device_class": "heat",
    },
    "hc1_enabled": {
        "register": "hc1_enabled",
        "translation_key": "hc1_enabled",
        "device_class": "running",
    },
    "hc1_pump": {
        "register": "hc1_pump",
        "translation_key": "hc1_pump",
        "device_class": "running",
    },
    "hc1_mixer_open": {
        "register": "hc1_mixer_open",
        "translation_key": "hc1_mixer_open",
        "device_class": None,
        "icon": "mdi:valve-open",
    },
    "hc1_mixer_close": {
        "register": "hc1_mixer_close",
        "translation_key": "hc1_mixer_close",
        "device_class": None,
        "icon": "mdi:valve-closed",
    },
}
