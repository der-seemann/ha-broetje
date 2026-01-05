# Brötje Heatpump Home Assistant Integration

## Overview

HACS-ready Home Assistant custom integration for Brötje heatpumps via Modbus TCP.

## Version Roadmap

| Version | Scope |
|---------|-------|
| v0.1 | Read-only sensors and binary sensors |
| v0.2 | Climate entity with basic control |
| v0.3 | Number/Select entities for setpoints and modes |
| v1.0 | Full read/write support, stable release |

## v0.1 Implementation Plan

### Step 1: Repository Structure

```
/
├── custom_components/
│   └── broetje_heatpump/
│       ├── __init__.py          # Integration setup
│       ├── manifest.json         # Integration metadata
│       ├── config_flow.py        # UI configuration
│       ├── const.py              # Constants and register map
│       ├── coordinator.py        # DataUpdateCoordinator
│       ├── entity.py             # Base entity class
│       ├── sensor.py             # Temperature/pressure sensors
│       ├── binary_sensor.py      # Operational states
│       ├── strings.json          # Translations
│       └── translations/
│           └── en.json
├── hacs.json                     # HACS metadata
├── README.md                     # Documentation
├── LICENSE                       # License file
└── .github/
    └── workflows/
        └── validate.yml          # CI validation
```

### Step 2: Config Flow

- Host and port input (default: 502)
- Modbus TCP connection validation
- Unique ID from device serial register
- Error handling with user-friendly messages

### Step 3: Modbus Coordinator

- `DataUpdateCoordinator` with 30s polling interval
- `AsyncModbusTcpClient` from pymodbus
- `asyncio.Lock()` for thread-safe access
- Graceful reconnection on errors
- `REGISTER_MAP` for register definitions

### Step 4: Device Info

- Read manufacturer string from Modbus (fallback: "Brötje")
- Read model from Modbus (fallback: "Heatpump")
- Serial number for unique identification
- Firmware version if available

### Step 5: Entity Platforms (Read-Only)

**Sensors:**
- Outdoor temperature
- Flow temperature
- Return temperature
- DHW temperature
- System pressure
- Compressor frequency (if available)

**Binary Sensors:**
- Compressor running
- Defrost active
- DHW demand
- Error state

### Step 6: Translations

- Config flow labels and errors
- Entity names via translation keys
- English as base language

### Step 7: CI/CD

- GitHub Actions workflow
- Hassfest validation
- Ruff linting
- Basic pytest for config flow

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| host | (required) | Modbus TCP gateway IP address |
| port | 502 | Modbus TCP port |
| unit_id | 1 | Modbus unit/slave ID |

## Register Map

To be populated from Brötje Modbus documentation:

```python
REGISTER_MAP = {
    # Device info registers
    "serial_number": {"address": TBD, "type": "input", "count": TBD},
    "model": {"address": TBD, "type": "input", "count": TBD},
    
    # Sensor registers
    "outdoor_temp": {"address": TBD, "type": "input", "scale": 0.1},
    "flow_temp": {"address": TBD, "type": "input", "scale": 0.1},
    # ... more registers
}
```

## Dependencies

- `pymodbus>=3.5.0` - Async Modbus TCP client
- Home Assistant 2024.1.0+ - Minimum HA version

## Resources

- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [HACS Documentation](https://hacs.xyz/)
- [pymodbus Documentation](https://pymodbus.readthedocs.io/)
- Brötje Modbus Parameter List (PDF)
