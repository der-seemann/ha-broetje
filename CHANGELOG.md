# Changelog

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
