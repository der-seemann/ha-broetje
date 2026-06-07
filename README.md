# Brötje Heating System Integration for Home Assistant

🇩🇪 [Deutsche Version](README.de.md)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![Version](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fder-seemann%2Fha-broetje%2Fmain%2Fcustom_components%2Fbroetje_heating%2Fmanifest.json&query=%24.version&label=version)](https://github.com/der-seemann/ha-broetje/blob/main/custom_components/broetje_heating/manifest.json)

<img src="custom_components/broetje_heating/images/logo.png" alt="Brötje Logo" width="200">

Home Assistant integration for Brötje heating systems via Modbus TCP. This is an extended fork based on [`henrywiechert/ha-broetje`](https://github.com/henrywiechert/ha-broetje) and tracks the current implementation status of the **IWR/GTW-08** gateway and the **ISR Plus** module without intentionally mirroring outdated upstream README sections.

Current BLW 12.1 reference setup:

- `244 sensor`
- `32 number`
- `10 select`
- `2 climate`
- `47 binary_sensor`
- `117` writable Home Assistant entities

The current codebase also includes:

- automatic register backoff/disable handling for sentinel values and recurring Modbus exceptions
- three poll profiles (`fast` / `normal` / `slow`)
- IWR setup auto-detection for zones and optional feature groups with manual correction
- write support with immediate readback and in-memory state refresh
- orphan entity and orphan sub-device cleanup on reload

## Supported Modules

This integration supports two Brötje Modbus modules. During installation, you select which module your system uses. Both can be installed in parallel if you have multiple heating appliances.

| Module | Type | Typical Use | Status |
|--------|------|-------------|--------|
| **IWR / GTW-08** | Gateway module | Heat pumps, newer systems | Supported |
| **ISR Plus** | Modbus module | Gas boilers, older systems | Supported |

### IWR / GTW-08 (Gateway Module)

The IWR/GTW-08 is the current-generation Modbus gateway used by Brötje heat pumps and newer heating systems. It provides comprehensive monitoring including:

- Appliance temperatures, pressures, and power
- Heat pump status (main status + sub status with 100+ codes)
- Energy counters (consumed and delivered, per CH/DHW/cooling)
- COP monitoring
- Up to 12 configurable zones with per-zone temperatures, setpoints, and pump status
- Bitfield-based status indicators (flame, heat pump, backup heaters, valves)
- Service and error diagnostics per board

Register specifications:
- GTW-08 Modbus (7854678 - v.01) — English
- Modbus GTW-08 Parameter List (7740782-01) — German

### ISR Plus (Legacy Module)

The ISR Plus module is the older Modbus interface found on Brötje gas boilers and some heat pump installations. It provides:

- Heating circuit 1 temperatures and setpoints
- DHW (domestic hot water) settings and tank status
- Buffer storage monitoring
- Boiler/burner status and energy counters
- General functions (outdoor temperature, alarm relay)

Register specification: [de-de_ma_modbm.pdf](https://polo.broetje.de/pdf/7715040=6=pdf_(bdr_a4_manual)=de-de_ma_modbm.pdf)

## Supported Models
All Brötje heatpumps and gasboilers with one of the listed Modbus interfaces.

<img src="custom_components/broetje_heating/images/Broetje-BLW-Eco-10.1.png" alt="Brötje BLW Eco" width="300">

### Tested Models
- **Brötje BLW Eco 10.1** (tested with ISR and IWR/GTW-08)
- **Brötje BLW Eco 12.1** (explicitly tested on the current fork)
- **Brötje BLW Mono 8** (Hybrid Setup, Remeha GTW-08)

*Other Brötje heating systems with Modbus interface should also work. I appreciate any feedback for other models*

## Features

- **Two module types**: IWR/GTW-08 and ISR Plus, selectable during setup
- **Parallel operation**: Both modules can run side by side for different appliances
- **Writable IWR controls**: Write-enabled IWR entities are exposed as `number`, `select`, `time`, and `climate` entities, with immediate readback and state refresh after writes
- **Auto-disable logic**: Registers that repeatedly return sentinel values or recurring Modbus exceptions are automatically throttled or disabled instead of spamming invalid states
- **Automatic feature detection (IWR)**: Setup probes zones, zone roles, hybrid, cascade, cooling, and buffer tank capabilities and uses the result as the default entity layout
- **Manual correction**: The detected IWR zones and feature groups can be corrected during setup or later in the options flow
- **Poll strategy**: `fast`, `normal`, and `slow` poll profiles reduce bus load while still keeping relevant runtime values responsive
- **Orphan cleanup**: Replaced entities, removed sub-devices, and stale zone devices are cleaned up on reload
- **IWR**: entity count depends on configured zones and detected sub-devices; the current BLW 12.1 reference setup exposes the counts listed above
- **ISR**: 117 entities (100 sensors + 17 binary sensors) across 6 categories
- **Climate subsystem** (IWR): Zone thermostat entities are exposed via Home Assistant `climate` entities (Thermostat card compatible) with current temperature, target setpoint, and HVAC mode/action mapping.
- **Writable zone controls** (IWR): Includes control mode, room setpoint, external room temperature injection, DHW setpoints/hysteresis, low-noise schedule, remote control registers `256-259`, and the current per-zone writable parameter families documented in [ENTITIES.md](ENTITIES.md)
- **Sub-devices**: Entities are grouped under functional sub-devices (for example boiler/service/solar/buffer/hybrid). Only detected sub-devices are kept; stale/orphaned sub-devices are removed automatically on reload.
- **Configurable zones** (IWR): 1–12 zones selectable during setup or reconfigurable via integration options
- **Configuration-dependent entity creation**: Entities are only created for enabled feature groups and meaningful zone roles. For example, DHW zones do not get room-control entities and disabled feature groups do not create unused entities.
- **Configurable poll profiles**: Separate `fast`, `normal`, and `slow` intervals adjustable via integration options
- **External room sensor sync** (IWR): Heating zones can mirror one or more Home Assistant temperature sensors into the writable room-temperature measured registers with `average`, `min`, or `max` aggregation
- **External room sensor watchdog**: A per-zone timeout watchdog stops writes when all sources are stale/invalid, persists the pause/active state across Core restarts, and resumes automatically when valid sources return
- **External room sensor source filter**: Setup/options flow supports room prefilter, text prefilter, and temperature-sorted source lists for large sensor inventories
- **German and English translations**
- **Sentinel value filtering**: Invalid Modbus readings (for example `0x8000` for `int16`, `0x00FF` for `uint8/enum8`, `0xFFFF`, `0xFFFFFFFF`, and register-specific sentinel overrides) are shown as unavailable instead of bogus numbers
- **Automatic registry disable**: Registers that become `sentinel_permanent` are automatically disabled in the Home Assistant entity registry so they stay recoverable without being recreated by default

### ISR Coverage

- 🌡️ **Heating Circuit 1** — temperatures, setpoints, pump, mixer
- 🚿 **DHW** — operating mode, legionella protection, circulation
- 🪣 **DHW Storage Tank** — tank temperatures, pumps
- 🔋 **Buffer Storage** — buffer temperatures, valves
- 🔥 **Boiler** — burner, fan, energy counters
- ⚙️ **General Functions** — outdoor temperature, alarm relay, manual mode

> **Note:** Currently only **Heating Circuit 1 (HK1)** is supported. Support for HC2/HC3 may be added in a future version.

### IWR Coverage

- 🌡️ **Appliance** — temperatures, pressures, flow/return, COP, power, CH/DHW/cooling enable
- 🎛️ **Main Controller** — status bits, heat demand, output states, energy counters
- 🏠 **Zones** (per zone, up to 12) — setpoints, heating curves, control strategy, time programs, room/flow temperatures, valve and pump states
- 🔧 **System Discovery** — connected boards, device types, software/firmware versions, article numbers
- ⚠️ **Service & Diagnostics** — error codes and severity per board, service notifications
- 🔗 **Cascade** — cascade status

> Entity counts scale with the number of configured zones: ~213 entities for 1 zone, up to ~884 for 12 zones.

## Requirements

- Brötje heating system with Modbus interface
- Modbus TCP gateway connected to the heating system
- Home Assistant 2024.1.0 or newer

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add `https://github.com/der-seemann/ha-broetje` and select "Integration" as the category
6. Click "Add"
7. Search for "Brötje" and install it
8. Restart Home Assistant

This README documents the fork state at `der-seemann/ha-broetje`. If you install from HACS, make sure you use the fork URL above rather than the original upstream repository.

### Manual Installation

1. Download or clone `https://github.com/der-seemann/ha-broetje`
2. Copy it to your Home Assistant `config/custom_components/` directory
3. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Brötje"
4. **Select your module type**: ISR or IWR
5. Enter the connection details:
   - **Host**: IP address of your Modbus TCP gateway
   - **Port**: Modbus TCP port (default: 502)
   - **Unit ID**: Modbus slave ID (default: 1)
6. **IWR only**: Choose how to configure zones and feature groups:
   - **Autodetect**: Reads zone type and zone function registers, classifies each zone as heating / DHW / inactive, and probes optional feature groups (`Hybrid function`, `Cascade operation`, `Cooling`, `Buffer tank`) from live registers. Review the preselection and correct it if needed.
   - **Manual**: Select any combination of zones 1–12 and explicitly decide which optional feature groups should create entities.

To add a second module (e.g., both ISR and IWR), simply add the integration again and select the other module type.

### Options

After setup, click the **Configure** (gear icon) button on the integration entry to adjust:

- **Fast poll profile**: Interval for fast-changing runtime values (default: 30 seconds, range: 10–3600)
- **Normal poll profile**: Interval for the standard register set (default: 120 seconds, range: 10–3600)
- **Slow poll profile**: Interval for slowly changing diagnostics and counters (default: 600 seconds, range: 10–3600)
- **Zones and feature groups** (IWR only): Re-run autodetection or manually change active zones, zone roles, and optional feature groups. Changes trigger an integration reload and prune stale entities from the registry.
- **External room sensors** (IWR heating zones only): Select one or more Home Assistant temperature sensors per heating zone, choose `average` / `min` / `max`, and configure write interval plus source timeout. The flow includes room and text prefilters and keeps the actual selector list sorted by current temperature when opened.

### External room sensors (IWR)

The writable `room temperature measured` registers can be driven from Home Assistant sensors for heating zones. Typical use cases are wall thermostats, BLE room sensors, or aggregated room values.

- Multiple source entities per zone are supported
- Aggregation modes: `average`, `min`, `max`
- Default source timeout: 90 minutes
- Default write interval: 60 seconds
- If all sources are stale/invalid, writes stop and the appliance can fall back to its own internal/outdoor-temperature strategy
- The watchdog pause/active state is persisted and re-evaluated on Home Assistant Core restart
- The selector flow supports room prefilter + text prefilter before showing the final entity list

## Entities

See [ENTITIES.md](ENTITIES.md) for:

- the full ISR entity inventory with register addresses and descriptions
- the currently documented writable IWR entity groups
- plant-dependent auto-disabled registers and current limitations

For IWR entities, see [`custom_components/broetje_heating/register_map.csv`](custom_components/broetje_heating/register_map.csv) for a comprehensive register map including addresses, data types, descriptions (EN/DE), units, scaling factors, and read/write status (`rw_spec` and `rw_implemented`).

### Highlights

- **Temperatures**: Flow, return, room, outdoor, exhaust gas, heat pump
- **Energy counters**: Consumed and delivered energy for CH, DHW, and cooling (kWh)
- **Operating hours**: Total hours, backup heater hours, pump hours per zone
- **Status information**: Main/sub status, pump states, valve positions, flame/heat pump on
- **COP**: Coefficient of performance monitoring (IWR)
- **Diagnostics**: Per-board error codes and severity, service notifications

Not every sensor is available on every heating system! E.g., gas consumption on heat pumps, or COP on gas boilers.

## Dashboard Example

```yaml
type: picture-glance
image: /local/broetje_heatpump/Broetje-BLW-Eco-10.1.png
title: Brötje Wärmepumpe
entities:
  - entity: sensor.brotje_heatpump_hc1_flow_temperature
    name: Vorlauf
  - entity: sensor.brotje_heatpump_kesseltemperatur
    name: Kessel
  - entity: sensor.brotje_heatpump_aussentemperatur
    name: Außen
  - entity: binary_sensor.brotje_heatpump_hc1_pump
    name: Pumpe
```

## Troubleshooting

### Cannot connect to device

- Verify the Modbus TCP gateway is accessible from Home Assistant
- Check the IP address and port are correct
- Ensure the Modbus unit ID matches your device configuration
- Test connectivity using a Modbus tool like `mbpoll`

### No sensor values

- The register addresses may need adjustment for your specific model
- Check Home Assistant logs for Modbus communication errors
- Some sensors show unavailable when the appliance reports sentinel values or when the coordinator temporarily/permanently auto-disables a plant-dependent register after repeated failures
- Permanently unavailable plant-dependent registers can be auto-disabled in the Home Assistant entity registry; re-enable them manually if your hydraulic layout changes later

### External room sensor writeback differs from the written value

- Register `2129` (`room temperature measured` on the tested IWR zone-3 setup) can quantize the injected value internally
- During live verification, a raw write of `1960` (19.6 °C) was read back as raw `2000` (20.0 °C)
- This is treated as appliance behavior, not as an integration write bug

## Development

This integration uses:

- [pymodbus](https://pymodbus.readthedocs.io/) ≥3.11.0 for Modbus TCP communication
- Home Assistant's `DataUpdateCoordinator` for efficient polling

### Pre-commit hook

A pre-commit hook runs `ruff check` and `ruff format` on `custom_components/broetje_heating` before each commit. To set it up:

```bash
pip install pre-commit
pre-commit install
```

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Run `ruff check` and `ruff format --check custom_components/broetje_heating` (or use the pre-commit hook)
4. Submit a pull request

## Roadmap

- [~] Write support for selected R/W registers (ongoing expansion)
- [ ] Anti-short-cycling / generator protection logic: [Issue #3](https://github.com/der-seemann/ha-broetje/issues/3)
- [ ] Additional heating circuits for ISR (HC2, HC3)
- [X] Brötje logo in official HA brand repo

## Acknowledgements

- [Henry Wiechert](https://github.com/henrywiechert) for the original `ha-broetje` groundwork this fork directly builds on. Without that work, this extended version would not exist.
- The Home Assistant community and all contributors who made Home Assistant what it is.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This integration is not affiliated with or endorsed by Brötje. Use at your own risk.
