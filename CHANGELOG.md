# Changelog

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
