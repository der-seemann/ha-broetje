# Changelog

## v0.15.1
- Fix: Setup- und Discovery-Reads werden jetzt gemeinsam serialisiert, damit config_flow.py nicht mehr am Coordinator-Lock vorbei liest.
- Fix: async_shutdown() ist gegen einen `None`-Cleanup-Pfad abgesichert, damit Unload nicht mehr mit `TypeError: 'NoneType' object can't be awaited` crasht.
- Fix: Modbus-Timeout und Retry-Verhalten wurden erhöht, um späte RTU-Antworten und transaction-id-Mismatches zu vermeiden.

## v0.15.0
- Feat: The external room sensor flow now uses Home Assistant's native multi-entity selector for temperature sensors instead of the previous two-step room/text prefilter flow.
- Fix: Aggregation is now exposed as its own field directly below the sensor selection in config flow and options flow.
- Fix: The custom prefilter step and related selector plumbing were removed, so sensor selection, aggregation, write interval, and timeout now live on one page.
- Fix: The Modbus coordinator no longer disconnects before every update batch, which avoids transaction-ID resets and the related log flooding. This includes the discussion fix from `99ce8c6`.

## Current fork status
- Docs: `README.md` and `ENTITIES.md` synchronized to the current fork state, including the BLW 12.1 reference installation, current entity counts, HACS installation via `der-seemann/ha-broetje`, writable entity groups, and installation-dependent auto-disable notes.
- Fix/Behavior: Auto-disable logic for sentinel values and recurring Modbus exceptions is part of the active fork and documented as a first-class integration feature.
- Fix/Behavior: Poll strategy now uses three profiles (`fast`, `normal`, `slow`) instead of treating every register equally.
- Feat: Writable support currently spans `117` writable Home Assistant entities on the documented BLW 12.1 reference installation.
- Fix: Immediate write readback and state refresh after successful writes landed in commit `6e5c1cb`.
- Fix: Replaced/orphaned entities and stale sub-devices are cleaned up on reload.
- Fix: Poll-profile handling for registers `256-259` was corrected so the remote-control writes are polled on the intended cadence.

## v0.15.0-beta.3
- Feat: The external room sensor flow now uses Home Assistant's native multi-entity selector for temperature sensors instead of the previous two-step room/text prefilter flow.
- Fix: Aggregation is now exposed as its own field directly below the sensor selection in config flow and options flow.
- Fix: The custom prefilter step and related selector plumbing were removed, so sensor selection, aggregation, write interval, and timeout now live on one page.

## v0.15.0-beta.2
- Feat: External room sensor support for IWR heating zones now supports multiple Home Assistant temperature sources per zone with `average`, `min`, and `max` aggregation.
- Feat: Config and options flow now include a dedicated external-room-sensor selector with room prefilter, text prefilter, and temperature-sorted source lists for heating zones only.
- Fix: External room sensor watchdog now persists its pause/active status in Home Assistant storage and re-evaluates source validity on startup, so pause behavior survives Core restarts.
- Fix/Behavior: When all configured sources are stale or invalid, writes stop and the appliance can fall back to its own outdoor-temperature/internal control strategy; sync resumes automatically once valid sources return.
- Docs: `README.md`, `README.de.md`, and `CHANGELOG.md` updated for external room sensors, watchdog persistence, filtering, and the known read-back quantization behavior of register `2129`.

## v0.15.0-beta.1
- Feat: IWR setup flow now auto-detects zones, zone roles, and optional feature groups (`hybrid`, `cascade`, `cooling`, `buffer_tank`) with manual correction during setup and reconfiguration.
- Feat: Entity creation for IWR is now installation-dependent; disabled feature groups and unsuitable zone roles no longer create unnecessary entities.
- Feat: Options flow now exposes three separate poll intervals for `fast`, `normal`, and `slow` profiles instead of a single global scan interval.
- Fix: Sentinel matrix expanded for `0x8000` (`int16`), `0x00FF` (`uint8` / `enum8`), and register-specific sentinel overrides; invalid values now stop leaking through as bogus states.
- Fix: Registers that become `sentinel_permanent` are automatically disabled in the Home Assistant entity registry.
- Docs: `README.md`, `README.de.md`, and `CHANGELOG.md` updated for feature detection, poll profiles, configuration-dependent entity creation, and sentinel handling.

## v0.14.0-beta.0
- Feat: Kaskaden-Register `7105-7146` und `7151-7227` als neue IWR/GTW-08-Entities ergänzt, inklusive Erzeuger-8/9/10-Statusblöcke und Kaskadenleistungs-Sollwerten.
- Fix: Neue Kaskaden-Entities standardmäßig aktiviert statt `disabled_by=integration`.
- Fix: Modbus-Coordinator robuster gegen Batch-Fehler, Incomplete-Reads und Sentinel-Werte; Diagnoseattribute (`last_read_status`, Rohregister, Fehlerdetails) werden exponiert.
- Fix: `unknown`-Restfälle auf sinnvolle Zustände reduziert (`unavailable` bzw. `device_not_available`) für Sensoren, Binary-Sensoren und betroffene Enum-Zonen.
- Docs: `WORKLOG.md`, `ENTITY_STATUS.md` und `UNDOCUMENTED.md` auf den verifizierten Endstand der Broetje-/HA-Validierung synchronisiert.

## v0.13.0-beta.0
- Feat: Neuer Buffer-Tank-Block mit `buffer_tank_temperature_bottom`, `buffer_tank_temperature_top`, `buffer_tank_pump_state`, `buffer_tank_mode`.

## v0.12.0-beta.0
- Feat: Neuer Service-Block mit `board9_error_code`/`severity` und `board10_error_code`/`severity`.

## v0.11.0-beta.0
- Feat: Neuer Service-Block mit `board7_error_code`/`severity` und `board8_error_code`/`severity`.

## v0.10.0-beta.0
- Feat: Neuer Service-Block mit `current_generic_error_code`, `board5_error_code`/`severity` und `board6_error_code`/`severity`.

## v0.9.0-beta.0
- Docs: Phase-1 Gap-Reports zu einer deduplizierten Lückenliste unter `.kiki/reports/PHASE1_LUECKENLISTE_KONSOLIDIERT_2026-05-23.{md,csv}` zusammengeführt.
- Feat: Neue IWR/GTW-08 Sensoren `buffer_tank_active`, `cascade_role` und `appliance_error_priority` ergänzt.

## v0.8.0-beta.0
- Feat: `AP050` Gerätezeit wird als lesbarer Zeitstempel aus dem 6-Byte-OCTETSTRING dekodiert.

## v0.7.0-beta.4
- Fix: `appliance_time_sensor` und `low_noise_mode_state_sensor` aus dem Binary-Sensor-Block in den Sensor-Block verschoben.

## v0.7.0-beta.3
- Fix: Config-Entry-Migration 3.2 entfernt die alten fehlerhaften `binary_sensor`-Registry-Einträge für `appliance_time` und `low_noise_mode_state`.

## v0.7.0-beta.2
- Fix: neue Sensor-Entity-Keys für `appliance_time` und `low_noise_mode_state`, damit alte fehlerhafte Binary-Sensor-Registry-Einträge die Sensoranlage nicht mehr blockieren.

## v0.7.0-beta.1
- Fix: fehlenden Register-Map-Eintrag für `low_noise_mode_state` ergänzt, damit der Sensor live gelesen wird.

## v0.7.0-beta.0
- Feat: System-Discovery-Register für Board 1-10 als Sensoren ergänzt.
- Fix: `gateway_device_type` und `board*_device_type` werden lesbar formatiert.
- Fix: `low_noise_mode_state` und `appliance_time` korrekt als Sensoren übersetzt.

## v0.6.0-beta.5
- Fix: `AP050` Appliance Time als Rohsensor ergänzt.

## v0.6.0-beta.4
- Fix: HMI-Statusbitfelder 340-342 als rohe Diagnosticsensors ergänzt.

## v0.6.0-beta.3
- Fix: Main-Control-Register 260 für externe Kühl-Fernverwaltung ergänzt.

## v0.6.0-beta.2
- Fix: `outdoor_unit_operation_mode` im Register-Map ergänzt, damit der letzte Batch-Read-Hinweis verschwindet.

## v0.6.0-beta.1
- Fix: Missing boiler register map entries ergänzt, damit `number`/`select`/`sensor`-Setup nicht mehr an KeyErrors scheitert.
- Fix: `BroetjeNumber` gegen fehlendes `_attr_device_class` abgesichert.

## v0.6.0-beta.0
- Feat: Boiler/Appliance Monitoring Block 390-493 als Entities ergänzt.
- Feat: Neue Boiler-/Hybrid-Selects und -Numbers in `iwr.py`, `register_map.csv` und Übersetzungen ergänzt.

## v0.5.0-beta.0
- Feat: Main Control Monitoring counters 288-304 als Entities ergänzt.
- Feat: Neue Register in `register_map.csv`, `iwr.py` und Übersetzungen ergänzt.
