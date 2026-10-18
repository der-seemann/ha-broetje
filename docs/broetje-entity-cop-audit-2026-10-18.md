# Brötje entity and working-ratio audit — 2026-10-18

## Scope and evidence

The review compares the fork with Henry’s `henrywiechert/ha-broetje` implementation by behavior, then checks the manufacturer GTW-08 parameter workbook (sheets DeviceInformation, SystemDiscovery, MainControlMonitoring, Boiler, Service, Zones X12, BufferTank, Cascade, Solar, Thermodynamic Water Heater, Hybrid, BMS) and the accompanying Modbus PDFs. The workbook carries parameter-list versions 1.02/1.03. The row-by-row manufacturer source register, code counterpart, status, rationale, and bounded live-registry evidence are in [gtw08-manufacturer-entity-audit-2026-10-18.csv](gtw08-manufacturer-entity-audit-2026-10-18.csv).

The matrix has 537 source rows. It distinguishes 301 rows represented in the static code register map, 102 dynamically generated zone rows, 97 optional-module sensor definitions and 4 raw diagnostic definitions implemented read-only, one optional Cascade register with a manufacturer width/type conflict, 11 manufacturer-reserved rows, 10 bytes covered by a multi-byte field, 7 opaque schedules, one destructive discovery command, two address ranges without metadata, and one blank workbook row. A code-map match is not proof that a device exposes that module or that a Home Assistant entity is enabled. Zone rows depend on selected zone and device role. Cascade, Hybrid, and Solar follow existing feature gates; Solar remains automatically detected by register 8114. Thermodynamic Water Heater and BMS are explicit opt-ins, default off, and are never probed automatically. The unresolved Cascade 7012 source conflict remains excluded.

## Henry comparison and implemented gaps

The fork already includes the defrost status at register 481 as an enum, buffer registers 7600–7603, and the prior polling correction. Henry’s buffer control/diagnostic set not represented in the fork was 7500–7507 and 7604–7606. This work adds eight controls (seven Number entities and one Select) and three read-only BufferTank diagnostics. Their register widths, access, encoding and scale follow the manufacturer BufferTank sheet; no plant writes were used for testing. Writable controls are declared with the ordinary validated entity path, not raw-register services.

COP 9230 (0.001 scale) and threshold 9231 are already in the integration. The live registry snapshot showed the COP sensor disabled by the integration. Hybrid COP 462/threshold 463 is conditional on the Hybrid feature; the current device record alone does not prove that feature. The workbook describes 9230 as instantaneous COP and does not document a seasonal COP entity. Register 385 is a seasonal operating-mode setting, not an efficiency measure. The integration does not derive instantaneous COP from thermal power and site-wide electrical import: no WP-only electrical power source is available, and site import includes two well pumps.

## Historical working ratio

A May 2026 Home Assistant backup contains the earlier local template and registry IDs, including `sensor.wp_cop_intern_seit_nullpunkt`, `sensor.wp_cop_extern_seit_nullpunkt`, `sensor.wp_aktueller_cop`, and the two null-point input entities. The internal formula uses (register 443 total thermal kWh minus the installation-local thermal baseline) divided by (register 439 total electrical kWh minus the installation-local electrical baseline). The external formula uses site import and is not restored because that source includes unrelated loads. The former instantaneous template also divided thermal power by site-wide power and is not restored. No defined seasonal boundary is present, so the replacement is named “Arbeitszahl seit Nullpunkt,” not SCOP or seasonal COP.

The replacement is a native sensor with optional local baselines in the integration OptionsFlow. Only the HA instance’s options carry the installation-specific baseline. The sensor is unavailable unless both baselines are configured and finite, both counters are valid and not below their baselines, and electrical delta exceeds 0.01 kWh. It stores only the last counter pair and a reset latch. A counter drop latches unavailable until the baseline pair is changed; the old template history and entity IDs are left untouched.

## Deliberate exclusions

The alternative Modbus mapping control (register 12) is R/W but is not exposed without behavior-specific safety evidence. Discovery reset (200) is a destructive command. Buffer and zone schedule OCTET_STRING blocks have no verified encoding contract. Main Controller ranges 305–339 and 343–349 lack metadata, and Boiler row 438 is completely blank in the workbook; none supports a defensible entity definition. Optional manufacturer R/W documentation is exposed only through read-only sensor entities; no hardware write was tested. No raw register write service, OTA action, or physical test write is part of this change.

## Live-registry evidence limit

Registry findings in the CSV are from the targeted current HA snapshot and are only populated for the reviewed COP and buffer entities. “No per-row registry claim” means no claim was made from that bounded lookup; it does not mean the entity is absent. Newly implemented entities require the later deployment/live gate before being reported as active.
