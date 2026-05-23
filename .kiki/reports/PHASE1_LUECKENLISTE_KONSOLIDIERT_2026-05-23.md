# Phase-1 Lückenliste konsolidiert

Stand: 2026-05-23

## Kurzfazit
- Eindeutige fehlende Register/Blöcke über alle drei Quellen: 344
- Nur R laut Doku: 228
- Enthält W laut Doku: 116
- Diese Liste dedupliziert die drei Einzelreports, ohne Schreibfunktion zu implementieren.

## Artefakte
- CSV: `.kiki/reports/PHASE1_LUECKENLISTE_KONSOLIDIERT_2026-05-23.csv`
- Quelle 1: `.kiki/reports/GTW-08_ModBus-Spec_gap_report.md`
- Quelle 2: `.kiki/reports/Modbus_GTW-08_Liste_der_Parameter_gap_report.md`
- Quelle 3: `.kiki/reports/GTW-08-Modbus-parameterlijst_gap_report.md`

## Konsolidierte Lückenliste
| Block | Typ | Zugriff | Klasse | Kontext | Quellen | Beschreibung |
|---|---|---|---|---|---|---|
| 1-10 | OCTETSTRING | R | nur R laut Doku | DeviceInformationGtw08 (2) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Manufacturer Code (= VAT code) of the device |
| 12 | UINT8 | R/W | enthält W laut Doku | DeviceInformationGtw08 (2) | GTW-08-Modbus-parameterlijst_gap_report.md | Alternative Modbus mapping |
| 197 | UINT8 | R | nur R laut Doku | SystemDiscovery (3) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Buffer Tank is active on the appliance |
| 198 | UINT8 | R | nur R laut Doku | SystemDiscovery (3) | GTW-08-Modbus-parameterlijst_gap_report.md | the appliance is part of a cascade |
| 200 | UINT8 | R/W | enthält W laut Doku | SystemDiscovery (3) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Reset discovery table. Set to 0x5A to execute the order. Reset to 0 by the GTW-08 |
| 260 | INT16 | R/W | enthält W laut Doku | MainControlMonitoring (16) | GTW-08-Modbus-parameterlijst_gap_report.md | External Remote Management: Heat demand Temperature setpoint Cooling to send to the CU device |
| 276 | UINT8 | R | nur R laut Doku | MainControlMonitoring (16) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Special Status bitfield of the appliance /cascade |
| 278 | ENUM8 | R | nur R laut Doku | MainControlMonitoring (16) | GTW-08-Modbus-parameterlijst_gap_report.md | Appliance error priority |
| 288-289 | UINT32 | R | nur R laut Doku | MainControlMonitoring (16) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Counter burner starts |
| 290-291 | UINT32 | R | nur R laut Doku | MainControlMonitoring (16) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Counter Burning Hours |
| 292 | UINT16 | R | nur R laut Doku | MainControlMonitoring (16) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Number of hours appliance was active after service |
| 293-294 | UINT32 | R | nur R laut Doku | MainControlMonitoring (16) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Number of successful Compressor Starts after service |
| 295-296 | UINT32 | R | nur R laut Doku | MainControlMonitoring (16) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | counter Backup1 starts |
| 297-298 | UINT32 | R | nur R laut Doku | MainControlMonitoring (16) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | counter Backup1 Hours |
| 299-300 | UINT32 | R | nur R laut Doku | MainControlMonitoring (16) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | counter Backup2 starts |
| 301-302 | UINT32 | R | nur R laut Doku | MainControlMonitoring (16) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | counter Backup2 Hours |
| 303-304 | UINT32 | R | nur R laut Doku | MainControlMonitoring (16) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Number of hours appliance was active |
| 340 | UINT8 | R | nur R laut Doku | MainControlMonitoring (16) | GTW-08-Modbus-parameterlijst_gap_report.md | Status bitfields number 1. Relevant for the HMI output |
| 341 | UINT8 | R | nur R laut Doku | MainControlMonitoring (16) | GTW-08-Modbus-parameterlijst_gap_report.md | Status bitfields number 2. Relevant for the HMI output |
| 342 | UINT8 | R | nur R laut Doku | MainControlMonitoring (16) | GTW-08-Modbus-parameterlijst_gap_report.md | Status bitfields number 3. Relevant for the HMI output |
| 350 | OCTETSTRING | R/W | enthält W laut Doku | MainControlMonitoring (16) | GTW-08-Modbus-parameterlijst_gap_report.md | Appliance Time |
| 351 | OCTET_STRING | R/W | enthält W laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parApTimeOfDay Byte 2 parApTimeOfDay Byte 3 Uhrzeit Ende Modusänderung ZeitStempel CIA OCTET_STRING 3023.0 Write |
| 390 | INT16 | R | nur R laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Alarm codes when there is an alarm condition |
| 416 | UINT8 | R | nur R laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Internal heat demand - Power |
| 417 | INT16 | R | nur R laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Internal heat demand - temperature Setpoint |
| 418 | UINT8 | R | nur R laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Internal heat demand - heatdemandType |
| 453 | UINT16 | R | nur R laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | current speed of the condenser pump |
| 454-455 | UINT32 | R | nur R laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | counter of the operating hours of the condenser pump (also called Hp Pump) |
| 456 | UINT16 | R | nur R laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | the actual current of the ODU as measured by the ODU, is used in the ODU unit to protect against too high current |
| 457 | UINT16 | R | nur R laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | operation mode of the outdoor unit, in the current contrôle scheme onfle the HEAT(1) and COOL(2) modes are used, The current default is HEAT(1) |
| 458 | UINT16 | R | nur R laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | system flow temperature setpoint including backups |
| 462 | UINT16 | R | nur R laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Instantaneous COP calculated by Hybrid application |
| 463 | UINT16 | R | nur R laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | COP threshold calculated by hybrid |
| 464 | ENUM8 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Hybrid mode selected |
| 465 | UINT8 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Hybrid Electricity cost in high tarif |
| 466 | UINT8 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Hybrid Electricity cost in low tarif |
| 467 | UINT8 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | cost of ofssil energy (oil or gas) - piece per litre or peu m3 |
| 468 | UINT8 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Electrical CO2 emission in heating mode |
| 469 | UINT8 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Electrical CO2 emission in DHW mode |
| 470 | UINT8 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Gas or Oil CO2 emission |
| 471 | UINT8 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Boiler in appliance efficiency |
| 472 | UINT16 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | COP threshold above which heat pump is authorized to operate when hybrid mode is primary energy |
| 473 | ENUM8 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Logic contact to take into account for Blocking input 1 |
| 474 | ENUM8 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Logic contact to take into account for Blocking input 2 |
| 475 | ENUM8 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Blocking input 2 setting |
| 476 | ENUM8 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Function blocking input |
| 477 | UINT8 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Minimum heating time before Domestic Hot Water production |
| 478 | UINT8 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Maximum time allowed to produce Domestic Hot Water |
| 479 | ENUM8 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Domestic Hot Water ECO or COMFORT setting |
| 480 | ENUM8 | R | nur R laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Low Noise Mode state |
| 481 | ENUM8 | R | nur R laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Heat Pump Defrost |
| 482 | ENUM8 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Set the type of backup used in the heat pump. |
| 483 | UINT8 | R | nur R laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Actual relative power produced for PDO output |
| 484 | UINT16 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Hybrid Electricity cost in high tarif accurate |
| 485 | UINT16 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Hybrid Electricity cost in low tarif accurate |
| 486 | UINT16 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Cost of fossil energy (oil or gas) - price per liter or per m3 accurate |
| 487 | INT16 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Outside temperature level above which the backup operation is blocked for a standard heating mode |
| 488 | UINT16 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Delay for starting the next generator (backup stage) in central heating mode |
| 489 | INT16 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Minimum oustide temperature below which Heat Pump is stopped |
| 490 | ENUM8 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Enabling Heat pump Silent mode |
| 491 | UINT8 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Start time for low noise function |
| 492 | UINT8 | R/W | enthält W laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | stop time for low noise |
| 493-494 | UINT32 | R | nur R laut Doku | Boiler(Appliance) (41) | GTW-08-Modbus-parameterlijst_gap_report.md | Total amount of pump starts |
| 530 | UINT16 | R | nur R laut Doku | Service (13) | GTW-08-Modbus-parameterlijst_gap_report.md | Current error generic code |
| 540 | UINT16 | R | nur R laut Doku | Service (13) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Code error of the device located on instance 5(CF System Discovery table Modbus Address 153) |
| 541 | ENUM8 | R | nur R laut Doku | Service (13) | GTW-08-Modbus-parameterlijst_gap_report.md | Error gravity error of the device located on instance 5 |
| 542 | UINT16 | R | nur R laut Doku | Service (13) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Code error of the device located on instance 6(CF System Discovery table Modbus Address 159) |
| 543 | ENUM8 | R | nur R laut Doku | Service (13) | GTW-08-Modbus-parameterlijst_gap_report.md | Error gravity error of the device located on instance 6 |
| 544 | UINT16 | R | nur R laut Doku | Service (13) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Code error of the device located on instance 7(CF System Discovery table Modbus Address 165) |
| 545 | ENUM8 | R | nur R laut Doku | Service (13) | GTW-08-Modbus-parameterlijst_gap_report.md | Error gravity error of the device located on instance 7 |
| 546 | UINT16 | R | nur R laut Doku | Service (13) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Code error of the device located on instance 8(CF System Discovery table Modbus Address 171) |
| 547 | ENUM8 | R | nur R laut Doku | Service (13) | GTW-08-Modbus-parameterlijst_gap_report.md | Error gravity error of the device located on instance 8 |
| 548 | UINT16 | R | nur R laut Doku | Service (13) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Code error of the device located on instance 9(CF System Discovery table Modbus Address 177) |
| 549 | ENUM8 | R | nur R laut Doku | Service (13) | GTW-08-Modbus-parameterlijst_gap_report.md | Error gravity error of the device located on instance 9 |
| 550 | UINT16 | R | nur R laut Doku | Service (13) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Code error of the device located on instance 10(CF System Discovery table Modbus Address 183) |
| 551 | ENUM8 | R | nur R laut Doku | Service (13) | GTW-08-Modbus-parameterlijst_gap_report.md | Error gravity error of the device located on instance 10 |
| 642 | 6 | R | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3202 |
| 643 | VISIBLE_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneFriendlyNameShort Byte 2 parZoneFriendlyNameShort Byte 3 Kreisbezeichnung kurz Read VISIBLE_STRING InternalVariable "DHW" |
| 646 | 1 | R | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | 3206 |
| 689 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3249 |
| 693 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramMonday1 Byte 8 parZoneTimeProgramMonday1 Byte 9 Read/Write OCTET_STRING 3431.n 363E.n |
| 699 | 20 | R | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | 3259 |
| 709 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3269 |
| 713 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramWednesday1 Byte 8 parZoneTimeProgramWednesday1 Byte 9 Read/Write OCTET_STRING 3433.n 3640.n |
| 719 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3279 |
| 723 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramThursday1 Byte 8 parZoneTimeProgramThursday1 Byte 9 Read/Write OCTET_STRING 3434.n 3641.n |
| 729 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3289 |
| 733 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramFriday1 Byte 8 parZoneTimeProgramFriday1 Byte 9 Read/Write OCTET_STRING 3435.n 3642.n |
| 739 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3299 |
| 743 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramSaturday1 Byte 8 parZoneTimeProgramSaturday1 Byte 9 Read/Write OCTET_STRING 3436.n 3643.n |
| 749 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3309 |
| 751 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramSunday1 Byte 4 parZoneTimeProgramSunday1 Byte 5 Read/Write OCTET_STRING 3437.n 3644.n |
| 759 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3319 |
| 763 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramMonday2 Byte 8 parZoneTimeProgramMonday2 Byte 9 Read/Write OCTET_STRING 3438.n 3645.n |
| 769 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3329 |
| 773 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramTuesday2 Byte 8 parZoneTimeProgramTuesday2 Byte 9 Read/Write OCTET_STRING 3439.n 3646.n |
| 779 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3339 |
| 780 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramWednesday2 Byte 2 parZoneTimeProgramWednesday2 Byte 3 Read/Write OCTET_STRING 343A.n 3647.n |
| 789 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3349 |
| 793 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramThursday2 Byte 8 parZoneTimeProgramThursday2 Byte 9 Read/Write OCTET_STRING 343B.n 3648.n |
| 799 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3359 |
| 803 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramFriday2 Byte 8 parZoneTimeProgramFriday2 Byte 9 Read/Write OCTET_STRING 343C.n 3649.n |
| 809 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3369 |
| 813 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramSaturday2 Byte 8 parZoneTimeProgramSaturday2 Byte 9 Read/Write OCTET_STRING 343D.n 364A.n |
| 819 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3379 |
| 823 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramSunday2 Byte 8 parZoneTimeProgramSunday2 Byte 9 Read/Write OCTET_STRING 343E.n 364B.n |
| 829-830 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3389 |
| 832 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramMonday3 Byte 6 parZoneTimeProgramMonday3 Byte 7 Zeitprogramm 3 Read/Write OCTET_STRING 343F.n 364C.n |
| 839 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3399 |
| 843 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramTuesday3 Byte 8 parZoneTimeProgramTuesday3 Byte 9 Read/Write OCTET_STRING 3440.n 364D.n |
| 849 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3409 |
| 853 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramWednesday3Byte 8 parZoneTimeProgramWednesday3Byte 9 Read/Write OCTET_STRING 3441.n 364E.n |
| 859 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3419 |
| 860 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramThursday3 Byte 2 parZoneTimeProgramThursday3 Byte 3 Read/Write OCTET_STRING 3442.n 364F.n |
| 869 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3429 |
| 873 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramFriday3Byte 8 parZoneTimeProgramFriday3Byte 9 Read/Write OCTET_STRING 3443.n 3650.n |
| 879 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3439 |
| 883 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramSaturday3 Byte 8 parZoneTimeProgramSaturday3 Byte 9 Read/Write OCTET_STRING 3444.n 3651.n |
| 889 | 20 | R | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | 3449 |
| 899-900 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3459 |
| 903 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramMonday4 Byte 8 parZoneTimeProgramMonday4 Byte 9 Read/Write OCTET_STRING 3446.n Not Available |
| 909 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3469 |
| 912 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramTuesday4 Byte 6 parZoneTimeProgramTuesday4 Byte 7 Read/Write OCTET_STRING 3447.n Not Available |
| 919 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3479 |
| 923 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramWednesday4Byte 8 parZoneTimeProgramWednesday4Byte 9 Read/Write OCTET_STRING 3448.n Not Available |
| 929 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3489 |
| 933 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramThursday4 Byte 8 parZoneTimeProgramThursday4 Byte 9 Read/Write OCTET_STRING 3449.n Not Available |
| 939 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3499 |
| 941 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramFriday4Byte 4 parZoneTimeProgramFriday4Byte 5 Read/Write OCTET_STRING 344A.n Not Available |
| 949 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3509 |
| 953 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramSaturday4 Byte 8 parZoneTimeProgramSaturday4 Byte 9 Read/Write OCTET_STRING 344B.n Not Available |
| 959 | 20 | - | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3519 |
| 963 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneTimeProgramSunday4Byte 8 parZoneTimeProgramSunday4Byte 9 Read/Write OCTET_STRING 344C.n Not Available |
| 971 | 6 | R | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3531 |
| 972 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneStartTimeHoliday Byte 2 parZoneStartTimeHoliday Byte 3 Startzeit Ferienbetrieb Read/Write OCTET_STRING 3421.n 365E.n ZeitStempel CIA |
| 974 | 6 | R | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3534 |
| 975 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneEndTimeHoliday Byte 2 parZoneEndTimeHoliday Byte 3 Endzeit Ferienbetrieb Read/Write OCTET_STRING 3422.n 365F.n ZeitStempel |
| 978 | 6 | R | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | 3538 |
| 979 | OCTET_STRING | R | nur R laut Doku | 3.3 Ungültige Werte | Modbus_GTW-08_Liste_der_Parameter_gap_report.md | parZoneEndTimeModeChange Byte 2 parZoneEndTimeModeChange Byte 3 Modusänderung Read/Write OCTET_STRING 3423.n 3660.n ZeitStempel CIA |
| 981 | 2 | 0,01°C | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md | CP280 to CP289 |
| 1119 | 2 | 0,01°C | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | CM040 to CM049 or DM001 |
| 1120 | 2 | 0,01°C | nur R laut Doku | Zones X12 (36) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | CM250 to CM259 or DM006 |
| 7000 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance Number on cascade: |
| 7001 | ENUM8 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | Mode on cascade |
| 7002 | ENUM8 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | Type of Cascade : Traditional or PARALLEL |
| 7003 | UINT8 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | This parameter is used to set the master boiler. |
| 7004 | UINT8 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Time delay for starting up or shutting down producers |
| 7005 | INT16 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Outside temperature triggering all stages in parallel mode |
| 7006 | INT16 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Outside temperature triggering all stages in parallel mode |
| 7007 | UINT8 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Rise Time to Acheive Setpoint |
| 7008 | ENUM8 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md | Enabled the master functionnality of this device one the S-Bus, If multople devices have this parameter all will be reset to 0 automatically, |
| 7009 | ENUM8 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | choice of cascade algorithm type, power or temperature |
| 7010 | UINT16 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md | The maximum flow temperature the système is allowed to produce |
| 7011 | ENUM8 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | the type of start order permutation, to determine which producer to start first |
| 7012-7013 | UINT16 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The time that needs to be elapsed before switching the appliance order |
| 7014 | ENUM8 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | Switching strategy for power control of the cascade. |
| 7015 | UINT8 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The preferred appliance for CH heat production |
| 7016 | UINT8 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The non-preferred appliance for CH heat production |
| 7017 | UINT8 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The power percentage for the late on strategy for activating the next appliance |
| 7018 | UINT8 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The power percentage for the late off strategy for deactivating the last appliance |
| 7019 | UINT8 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The power percentage for the early on strategy for activating the next appliance |
| 7020 | UINT8 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The power percentage for the early off strategy for deactivating the last appliance |
| 7021 | UINT8 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md | Minimum duration of post-operation of the generator pump |
| 7022 | ENUM8 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md | Force Primary Pump to Stop |
| 7023 | ENUM8 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The type of primary pump |
| 7024 | ENUM8 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The type of secondary pump |
| 7100 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Producer Active Number |
| 7102 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Number of Producers recognised in the cascade |
| 7103 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Number of stages available on the Casacde |
| 7104 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Number of stages required on the Casacde |
| 7105 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Cascade power request by the consumer manager - Power |
| 7106 | INT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Cascade power request by the consumer manager - - temperature Setpoint |
| 7107 | ENUM8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Cascade power request by the consumer manager - heatdemandType |
| 7108 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Cascade System Power Setpoint Calculated - Power |
| 7109 | INT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Cascade System Power Setpoint Calculated - temperature Setpoint |
| 7110 | ENUM8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | Cascade System Power Setpoint Calculated - heatdemandType |
| 7111 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Actual power output of Appliance 1 |
| 7112 | INT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 1 Flow Temperature |
| 7113 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 1 Status |
| 7114 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 1 Special Request |
| 7115 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Actual power output of Appliance 3 |
| 7116 | INT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 3 Flow Temperature |
| 7117 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 3 Status |
| 7118 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 3 Special Request |
| 7119 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Actual power output of Appliance 4 |
| 7120 | INT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 4 Flow Temperature |
| 7121 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 4 Status |
| 7122 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 4 Special Request |
| 7123 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Actual power output of Appliance 5 |
| 7124 | INT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 5 Flow Temperature |
| 7125 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 5 Status |
| 7126 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 5 Special Request |
| 7127 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Actual power output of Appliance 6 |
| 7128 | INT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 6 Flow Temperature |
| 7129 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 6 Status |
| 7130 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 6 Special Request |
| 7131 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Actual power output of Appliance 7 |
| 7132 | INT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 7 Flow Temperature |
| 7133 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 7 Status |
| 7134 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 7 Special Request |
| 7135 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Actual power output of Appliance 8 |
| 7136 | INT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 8 Flow Temperature |
| 7137 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 8 Status |
| 7138 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 8 Special Request |
| 7139 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Actual power output of Appliance 9 |
| 7140 | INT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 9 Flow Temperature |
| 7141 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 9 Status |
| 7142 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 9 Special Request |
| 7143 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Actual power output of Appliance 10 |
| 7144 | INT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 10 Flow Temperature |
| 7145 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 10 Status |
| 7146 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Appliance 10 Special Request |
| 7151-7152 | UINT32 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The requested power to fulfil the heat demand |
| 7153 | ENUM8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md | Outside Temperature connected |
| 7154 | INT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md | Outside Temperature Used by the Cascade |
| 7155 | INT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The requested power percentage |
| 7156 | UINT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md | Current Time To Start next Stage |
| 7157 | ENUM8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The activation of the primary pump relay |
| 7158 | ENUM8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The activation of the secondary pump relay |
| 7159 | ENUM8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The current state of the cascade system |
| 7160-7161 | UINT32 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The amount of hours spend on producing heat for CH |
| 7162-7163 | UINT32 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The amount of hours spend on producing heat for DHW |
| 7164 | INT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The measured return temperature on the LLH |
| 7165 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | Cascade, smart pump status - producer circuit of low loss header |
| 7166 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The pump speed output after transfer function for pwm or 0-10V output signal for primary pump (producer circuit) |
| 7167 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The pump speed output after transfer function for pwm or 0-10V output signal for secondary pump (consumer circuit) |
| 7168 | INT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The measured cascade flow temperature on the secondary side of the LLH |
| 7200 | UINT8 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The order in which the producers are going to be activated |
| 7201 | UINT8 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | Logical number that represents the physical location of a device within a cascade |
| 7202 | ENUM8 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The availability of the device for the cascade |
| 7203 | UINT16 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The minimum power of an appliance in the cascade system |
| 7205 | UINT16 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The maximum power of an appliance in the cascade system |
| 7207 | UINT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | List of appliances needed to fulfil the heat demand |
| 7208 | UINT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The temporary stored permutation order |
| 7209 | ENUM8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The status of all producers found on the S-Bus |
| 7210 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md | The generic error codes of all producers found on the S-Bus |
| 7211-7212 | UINT32 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md | Matrix describing the error priority and the error custom code per brand |
| 7213 | INT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md | Flow temperature of appliance. The temperature of the water leaving the appliance. |
| 7214 | INT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md | The return temperature of an appliance in the cascade system |
| 7215 | INT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md | The heat exchanger temperature of an appliance in the cascade system |
| 7216 | INT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md | The flu gas temperature of an appliance in the cascade system |
| 7217 | ENUM8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md | Current or upcoming service notification |
| 7218 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md | The water pressure of an appliance in the cascade system |
| 7219 | INT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md | The 2nd return temperature of an appliance in the cascade system |
| 7220 | UINT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md | The current pump speed |
| 7221 | UINT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md | Actual relative power of the appliance |
| 7222-7223 | UINT32 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md | Total number of burner hours. For heating and domestic hot water |
| 7224-7225 | UINT32 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md | Number of burner hours for Domestic Hot Water |
| 7226 | UINT8 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md | Producer order listed with node id's |
| 7227 | UINT16 | R | nur R laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md | The type of appliance in the cascade system |
| 7228-7229 | UINT32 | R/W | enthält W laut Doku | Cascade (110) | GTW-08-Modbus-parameterlijst_gap_report.md, GTW-08_ModBus-Spec_gap_report.md | The serial number of an appliance in the cascade system |
| 7500 | INT16 | R/W | enthält W laut Doku | BufferTank (22) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Hysteresis to start buffer loading |
| 7501 | INT16 | R/W | enthält W laut Doku | BufferTank (22) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Hysteresis to stop buffer tank loading |
| 7502 | UINT8 | R/W | enthält W laut Doku | BufferTank (22) | GTW-08-Modbus-parameterlijst_gap_report.md | Minimum duration of post-operation of the buffer tank pump |
| 7503 | ENUM8 | R/W | enthält W laut Doku | BufferTank (22) | GTW-08-Modbus-parameterlijst_gap_report.md | Heating Cooling Control strategy used with buffer tank |
| 7504 | UINT16 | R/W | enthält W laut Doku | BufferTank (22) | GTW-08-Modbus-parameterlijst_gap_report.md | Fixed setpoint requested by buffer tank in Heating Mode |
| 7505 | UINT16 | R/W | enthält W laut Doku | BufferTank (22) | GTW-08-Modbus-parameterlijst_gap_report.md | Fixed setpoint requested by buffer tank in Cooling Mode |
| 7506 | UINT8 | R/W | enthält W laut Doku | BufferTank (22) | GTW-08-Modbus-parameterlijst_gap_report.md | Buffer Tank Slope |
| 7507 | UINT16 | R/W | enthält W laut Doku | BufferTank (22) | GTW-08-Modbus-parameterlijst_gap_report.md | Offset to add to the calculate Setpoint |
| 7508-7517 | OCTET_STRING | R/W | enthält W laut Doku | BufferTank (22) | GTW-08-Modbus-parameterlijst_gap_report.md | Time program buffer tank |
| 7518-7527 | OCTET_STRING | R/W | enthält W laut Doku | BufferTank (22) | GTW-08-Modbus-parameterlijst_gap_report.md | (no description) |
| 7528-7537 | OCTET_STRING | R/W | enthält W laut Doku | BufferTank (22) | GTW-08-Modbus-parameterlijst_gap_report.md | (no description) |
| 7538-7547 | OCTET_STRING | R/W | enthält W laut Doku | BufferTank (22) | GTW-08-Modbus-parameterlijst_gap_report.md | (no description) |
| 7548-7557 | OCTET_STRING | R/W | enthält W laut Doku | BufferTank (22) | GTW-08-Modbus-parameterlijst_gap_report.md | (no description) |
| 7558-7567 | OCTET_STRING | R/W | enthält W laut Doku | BufferTank (22) | GTW-08-Modbus-parameterlijst_gap_report.md | (no description) |
| 7568-7577 | OCTET_STRING | R/W | enthält W laut Doku | BufferTank (22) | GTW-08-Modbus-parameterlijst_gap_report.md | (no description) |
| 7600 | INT16 | R | nur R laut Doku | BufferTank (22) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Measured buffer temperature bottom |
| 7601 | INT16 | R | nur R laut Doku | BufferTank (22) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Measured buffer temperature top |
| 7602 | ENUM8 | R | nur R laut Doku | BufferTank (22) | GTW-08-Modbus-parameterlijst_gap_report.md | State buffer tank pump |
| 7603 | ENUM8 | R | nur R laut Doku | BufferTank (22) | GTW-08-Modbus-parameterlijst_gap_report.md | The buffer tank Mode |
| 7604 | UINT8 | R | nur R laut Doku | BufferTank (22) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Buffer Tank winning heat demand request : the winning heat demand requested by the zones connected after the buffer tank - Power |
| 7605 | INT16 | R | nur R laut Doku | BufferTank (22) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Buffer Tank winning heat demand request : the winning heat demand requested by the zones connected after the buffer tank - temperature Setpoint |
| 7606 | UINT8 | R | nur R laut Doku | BufferTank (22) | GTW-08-Modbus-parameterlijst_gap_report.md, Modbus_GTW-08_Liste_der_Parameter_gap_report.md | Buffer Tank winning heat demand request : the winning heat demand requested by the zones connected after the buffer tank - heatdemandType |
| 8112-8113 | UINT32 | R | nur R laut Doku | Solar (21) | GTW-08-Modbus-parameterlijst_gap_report.md | Signal for storing the total solar thermal energy collected for DHW and CH. |
| 8114 | ENUM8 | R | nur R laut Doku | Solar (21) | GTW-08-Modbus-parameterlijst_gap_report.md | Signal for storing the actual status of the advanced solar range boiler |
| 8115 | UINT16 | R | nur R laut Doku | Solar (21) | GTW-08-Modbus-parameterlijst_gap_report.md | Signal for storing the instantaneous mean rotation speed of the solar pumps. |
| 8116 | INT16 | R | nur R laut Doku | Solar (21) | GTW-08-Modbus-parameterlijst_gap_report.md | Signal for storing the actual measured instantaneous value of the DHW tank low temperature sensor. |
| 8117 | INT16 | R | nur R laut Doku | Solar (21) | GTW-08-Modbus-parameterlijst_gap_report.md | Signal for storing the actual measured instantaneous value of the CH tank low temperature sensor. |
| 8118 | INT16 | R | nur R laut Doku | Solar (21) | GTW-08-Modbus-parameterlijst_gap_report.md | Signal for storing the instantaneous temperature of the heat conduct. medium at the solar collector. - collector 1 |
| 8119 | INT16 | R | nur R laut Doku | Solar (21) | GTW-08-Modbus-parameterlijst_gap_report.md | Signal for storing the instantaneous temperature of the heat conduct. medium at the solar collector - collector 2 |
| 8120 | ENUM8 | R | nur R laut Doku | Solar (21) | GTW-08-Modbus-parameterlijst_gap_report.md | Signal for storing the instantaneous status of each three way valve (ON or OFF). - valve 1 |
| 8121 | ENUM8 | R | nur R laut Doku | Solar (21) | GTW-08-Modbus-parameterlijst_gap_report.md | Signal for storing the instantaneous status of each three way valve (ON or OFF). - valve 2 |
| 8122 | INT16 | R | nur R laut Doku | Solar (21) | GTW-08-Modbus-parameterlijst_gap_report.md | Reduction of the setpoint of the DHW primary based on the heat delivery of a solar collector (solar first). |
| 8123 | INT16 | R | nur R laut Doku | Solar (21) | GTW-08-Modbus-parameterlijst_gap_report.md | Reduction of the setpoint of a buffered CH zone based on the heat delivery of a solar collector (solar first). |
| 8141 | ENUM8 | R/W | enthält W laut Doku | Solar (21) | GTW-08-Modbus-parameterlijst_gap_report.md | Configuration of the solar hydraulics installation type. |
| 8142 | ENUM8 | R/W | enthält W laut Doku | Solar (21) | GTW-08-Modbus-parameterlijst_gap_report.md | Parameter to configure the mode of the advanced solar DHW and/or CH function group. |
| 8143 | UINT16 | R/W | enthält W laut Doku | Solar (21) | GTW-08-Modbus-parameterlijst_gap_report.md | Parameter for nominal DHW tank T° setpoint. |
| 8144 | UINT16 | R/W | enthält W laut Doku | Solar (21) | GTW-08-Modbus-parameterlijst_gap_report.md | Parameter for configuring the nominal setpoint to charge the CH tank with solar energy, possible values are within the range 8°C ~ 60°C |
| 8145 | UINT16 | R/W | enthält W laut Doku | Solar (21) | GTW-08-Modbus-parameterlijst_gap_report.md | Parameter for configuring the maximum allowed temperature temperature in the solar panel.- collector 1 |
| 8146 | UINT16 | R/W | enthält W laut Doku | Solar (21) | GTW-08-Modbus-parameterlijst_gap_report.md | Parameter for configuring the maximum allowed temperature temperature in the solar panel - collector 2 |
| 8147 | UINT16 | R/W | enthält W laut Doku | Solar (21) | GTW-08-Modbus-parameterlijst_gap_report.md | Parameter for maximal DHW tank T° setpoint. |
| 8148 | UINT16 | R/W | enthält W laut Doku | Solar (21) | GTW-08-Modbus-parameterlijst_gap_report.md | Parameter for maximal CH tank T° setpoint. |
| 8149 | UINT16 | R/W | enthält W laut Doku | Solar (21) | GTW-08-Modbus-parameterlijst_gap_report.md | Parameter for setting the minimal temperature rise corresponding to one step increase in pump speed. |
| 8150 | UINT16 | R/W | enthält W laut Doku | Solar (21) | GTW-08-Modbus-parameterlijst_gap_report.md | Parameter for setting the minimal temperature rise corresponding to one step increase in pump speed. |
| 9001 | ENUM8 | R/W | enthält W laut Doku | Thermodynamic Water Heater (12) | GTW-08-Modbus-parameterlijst_gap_report.md | PV function Active |
| 9002 | ENUM8 | R/W | enthält W laut Doku | Thermodynamic Water Heater (12) | GTW-08-Modbus-parameterlijst_gap_report.md | PV function Contact Logic |
| 9003 | UINT16 | R/W | enthält W laut Doku | Thermodynamic Water Heater (12) | GTW-08-Modbus-parameterlijst_gap_report.md | Zone Dhw primary Boost PV Setpoint |
| 9004 | ENUM8 | R/W | enthält W laut Doku | Thermodynamic Water Heater (12) | GTW-08-Modbus-parameterlijst_gap_report.md | Peak/OffPeak Active |
| 9005 | ENUM8 | R/W | enthält W laut Doku | Thermodynamic Water Heater (12) | GTW-08-Modbus-parameterlijst_gap_report.md | Peak input contact logic configuration |
| 9006 | INT8 | R/W | enthält W laut Doku | Thermodynamic Water Heater (12) | GTW-08-Modbus-parameterlijst_gap_report.md | Max time BackUp off when peak mode enabled |
| 9007 | ENUM8 | R | nur R laut Doku | Thermodynamic Water Heater (12) | GTW-08-Modbus-parameterlijst_gap_report.md | S_PhotoVoltaicInputState |
| 9008 | ENUM8 | R | nur R laut Doku | Thermodynamic Water Heater (12) | GTW-08-Modbus-parameterlijst_gap_report.md | S_PeakOffPeakInputState |
| 9009 | ENUM8 | R/W | enthält W laut Doku | Thermodynamic Water Heater (12) | GTW-08-Modbus-parameterlijst_gap_report.md | Digital input 1 configuration |
| 9010 | ENUM8 | R/W | enthält W laut Doku | Thermodynamic Water Heater (12) | GTW-08-Modbus-parameterlijst_gap_report.md | Digital input 2 configuration |
| 9011 | ENUM8 | R/W | enthält W laut Doku | Thermodynamic Water Heater (12) | GTW-08-Modbus-parameterlijst_gap_report.md | digital input 1 contact logic configuration |
| 9012 | ENUM8 | R/W | enthält W laut Doku | Thermodynamic Water Heater (12) | GTW-08-Modbus-parameterlijst_gap_report.md | digital input 2 contact logic configuration |
| 9200 | INT16 | R | nur R laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | Flow temperature |
| 9201 | INT16 | R | nur R laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | Return temperature |
| 9202 | UINT16 | R | nur R laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | Internal setpoint used for hot water production |
| 9203 | UINT8 | R | nur R laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | actual Water pressure |
| 9204 | UINT8 | R | nur R laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | Status of appliance |
| 9205 | UINT8 | R | nur R laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | Sub Status of appliance |
| 9206-9207 | UINT32 | R | nur R laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | Counter burner/compressor starts |
| 9208-9209 | UINT32 | R | nur R laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | Counter Burning Hours |
| 9210-9211 | UINT32 | R | nur R laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | Number of hours appliance was active |
| 9212-9213 | UINT32 | R | nur R laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | NTotal energy consumed for production of central heat |
| 9214-9215 | UINT32 | R | nur R laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | Total energy consumed for production of domestic hot water. |
| 9216 | UINT16 | R | nur R laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | system flow temperature setpoint including backups |
| 9217 | UINT16 | R | nur R laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | current pump speed |
| 9218-9219 | UINT32 | R | nur R laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | signal used to capture actual power calculation |
| 9220 | UINT8 | R | nur R laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | Service is required |
| 9221 | ENUM8 | R/W | enthält W laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | Hybrid mode selected |
| 9222 | UINT8 | R/W | enthält W laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | Hybrid Electricity cost in high tarif |
| 9223 | UINT8 | R/W | enthält W laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | Hybrid Electricity cost in low tarif |
| 9224 | UINT8 | R/W | enthält W laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | cost of ofssil energy (oil or gas) - piece per litre or peu m3 |
| 9225 | UINT8 | R/W | enthält W laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | Electrical CO2 emission in heating mode |
| 9226 | UINT8 | R/W | enthält W laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | Electrical CO2 emission in DHW mode |
| 9227 | UINT8 | R/W | enthält W laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | Gas or Oil CO2 emission |
| 9228 | UINT8 | R/W | enthält W laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | Boiler in appliance efficiency |
| 9229 | UINT16 | R/W | enthält W laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | COP threshold above which heat pump is authorized to operate when hybrid mode is primary energy |
| 9232 | UINT16 | R/W | enthält W laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | Hybrid Electricity cost in high tarif accurate |
| 9233 | UINT16 | R/W | enthält W laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | Hybrid Electricity cost in low tarif accurate |
| 9234 | UINT16 | R/W | enthält W laut Doku | Hybrid (27) | GTW-08-Modbus-parameterlijst_gap_report.md | cost of fossil energy (oil or gas) - piece per litre or per m3 accurate |
| 21020 | ENUM8 | R/W | enthält W laut Doku | BMS (11) | GTW-08-Modbus-parameterlijst_gap_report.md | The heat demand mode which is used in case of a communication error |
| 21021 | ENUM8 | R/W | enthält W laut Doku | BMS (11) | GTW-08-Modbus-parameterlijst_gap_report.md | Fallback strategy to apply |
| 21022 | UINT8 | R/W | enthält W laut Doku | BMS (11) | GTW-08-Modbus-parameterlijst_gap_report.md | Number Of Minutes To Maintain Heat Demand in fallback mode |
| 21023 | UINT8 | R/W | enthält W laut Doku | BMS (11) | GTW-08-Modbus-parameterlijst_gap_report.md | fallback power setpoint |
| 21024 | INT16 | R/W | enthält W laut Doku | BMS (11) | GTW-08-Modbus-parameterlijst_gap_report.md | fallback temperature setpoint |
| 21025 | ENUM8 | R/W | enthält W laut Doku | BMS (11) | GTW-08-Modbus-parameterlijst_gap_report.md | fallback heat demand type |
| 21026 | ENUM8 | R/W | enthält W laut Doku | BMS (11) | GTW-08-Modbus-parameterlijst_gap_report.md | 0 - 10V input selection (temperature or power setpoint) |
| 21027 | UINT8 | R | nur R laut Doku | BMS (11) | GTW-08-Modbus-parameterlijst_gap_report.md | Measure of the Voltage on the 0-10V Input |
| 21028 | ENUM8 | R/W | enthält W laut Doku | BMS (11) | GTW-08-Modbus-parameterlijst_gap_report.md | Parameter to activate the 2nd return sensor |
| 21029 | INT16 | R | nur R laut Doku | BMS (11) | GTW-08-Modbus-parameterlijst_gap_report.md | Second return temperature |
| 21030 | UINT16 | R/W | enthält W laut Doku | BMS (11) | GTW-08-Modbus-parameterlijst_gap_report.md | Absolute max boiler power in KW. This is the power the device can produce when burner parameters are set at maximum. |
