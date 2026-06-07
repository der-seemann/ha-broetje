"""Constants for the Brötje Heatpump integration."""

from typing import Final

DOMAIN: Final = "broetje_heating"

# Default values
DEFAULT_PORT: Final = 502
DEFAULT_UNIT_ID: Final = 1
DEFAULT_SCAN_INTERVAL: Final = 120
DEFAULT_SCAN_INTERVAL_FAST: Final = 30
DEFAULT_SCAN_INTERVAL_NORMAL: Final = 120
DEFAULT_SCAN_INTERVAL_SLOW: Final = 600
SENTINEL_AUTO_DISABLE_THRESHOLD: Final = 3
SENTINEL_RETRY_INTERVAL_SECONDS: Final = 3600
EXCEPTION_CODE10_AUTO_DISABLE_THRESHOLD: Final = 3
EXCEPTION_CODE3_BACKOFF_THRESHOLD: Final = 3
EXCEPTION_CODE3_BACKOFF_SECONDS: Final = 900

# Configuration keys
CONF_UNIT_ID: Final = "unit_id"
CONF_SCAN_INTERVAL: Final = "scan_interval"
CONF_SCAN_INTERVAL_FAST: Final = "scan_interval_fast"
CONF_SCAN_INTERVAL_NORMAL: Final = "scan_interval_normal"
CONF_SCAN_INTERVAL_SLOW: Final = "scan_interval_slow"
CONF_ZONES: Final = "zones"
CONF_IWR_FEATURES: Final = "iwr_features"
CONF_IWR_ZONE_DETAILS: Final = "iwr_zone_details"
CONF_IWR_FEATURES_SOURCE: Final = "iwr_features_source"
CONF_EXTERNAL_ROOM_SENSORS: Final = "external_room_sensors"
CONF_EXTERNAL_ROOM_SENSOR_ENTITY_IDS: Final = "entity_ids"
CONF_EXTERNAL_ROOM_SENSOR_AGGREGATION: Final = "aggregation"
CONF_EXTERNAL_ROOM_SENSOR_WRITE_INTERVAL: Final = "write_interval_seconds"
CONF_EXTERNAL_ROOM_SENSOR_TIMEOUT: Final = "timeout_seconds"

EXTERNAL_ROOM_SENSOR_AGGREGATION_AVERAGE: Final = "average"
EXTERNAL_ROOM_SENSOR_AGGREGATION_MIN: Final = "min"
EXTERNAL_ROOM_SENSOR_AGGREGATION_MAX: Final = "max"
DEFAULT_EXTERNAL_ROOM_SENSOR_WRITE_INTERVAL: Final = 60
DEFAULT_EXTERNAL_ROOM_SENSOR_TIMEOUT: Final = 90 * 60

# Manufacturer info
MANUFACTURER: Final = "Brötje"

# Register types
REG_INPUT: Final = "input"
REG_HOLDING: Final = "holding"

# Sub-device identifiers
SUBDEV_BOILER: Final = "boiler"
SUBDEV_SERVICE: Final = "service"
SUBDEV_SOLAR: Final = "solar"
SUBDEV_BUFFER_TANK: Final = "buffer_tank"
SUBDEV_HYBRID: Final = "hybrid"

FEATURE_HYBRID: Final = "hybrid"
FEATURE_CASCADE: Final = "cascade"
FEATURE_COOLING: Final = "cooling"
FEATURE_BUFFER_TANK: Final = "buffer_tank"
IWR_OPTIONAL_FEATURES: Final[tuple[str, ...]] = (
    FEATURE_HYBRID,
    FEATURE_CASCADE,
    FEATURE_COOLING,
    FEATURE_BUFFER_TANK,
)
IWR_FEATURES_SOURCE_AUTO: Final = "auto"
IWR_FEATURES_SOURCE_MANUAL: Final = "manual"

SUB_DEVICE_LABELS: Final[dict[str, str]] = {
    SUBDEV_BOILER: "Boiler",
    SUBDEV_SERVICE: "Service",
    SUBDEV_SOLAR: "Solar",
    SUBDEV_BUFFER_TANK: "Buffer Tank",
    SUBDEV_HYBRID: "Hybrid",
}

# Always-present sub-devices for IWR (created unconditionally)
ALWAYS_PRESENT_SUBDEVICES: Final = {SUBDEV_BOILER, SUBDEV_SERVICE}

# Scale factors from Brötje ISR documentation
SCALE_TEMP: Final = 1 / 64  # 0.015625 - for temperature values
SCALE_CURVE: Final = 1 / 50  # 0.02 - for heating curve slope
SCALE_POWER: Final = 1 / 10  # 0.1 - for power in kW
SCALE_PERCENT_100: Final = 1 / 100  # 0.01 - for percentages scaled by 100
SCALE_HOURS: Final = 1 / 3600  # for hours stored as seconds
