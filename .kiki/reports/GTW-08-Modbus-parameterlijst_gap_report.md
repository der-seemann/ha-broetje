# GTW-08-Modbus-parameterlijst.xlsx gap report

Stand: 2026-05-19

## Ergebnis
- XLSX parser: direkter OOXML-Parser (`openpyxl` nicht installiert); Zellwerte aus `sharedStrings.xml` und Sheets extrahiert.
- Extrahierte Modbus-Zeilen: 537 (521 Einzel-/Startzeilen, 16 Bereichszeilen).
- Bewertete Quell-Blöcke mit Bedeutung: 509; reservierte/blanke Bereiche oder Future-use-Zeilen: 18; reine Fortsetzungszeilen: 10.
- Fehlende bzw. nicht vollständig durch `register_map.csv` abgedeckte Quell-Blöcke: 314 (198 R-only/ohne W, 116 mit W-Zugriff in der Doku).
- Unerklärte Fortsetzungszeilen nach Blockbildung: 0.

Bewertung: Die XLSX enthält deutlich mehr offizielle Registerblöcke als die aktuelle `register_map.csv`. R/W-Angaben wurden nur dokumentiert; es wurde keine Schreibfunktion implementiert oder getestet.

## Artefakte
- Extrakt Cache: `.kiki/cache/extracted/GTW-08-Modbus-parameterlijst_extracted_registers.csv`
- Extrakt Report-Kopie: `.kiki/reports/GTW-08-Modbus-parameterlijst_extracted_registers.csv`
- Referenz: `custom_components/broetje_heating/register_map.csv`

## Fehlende Blöcke nach Sheet
### DeviceInformationGtw08 (2)
| Register/Block | Sheet | FriendlyName | Description | Bytes | Data Type | Format | Access | Version |
|---:|---|---|---|---:|---|---|---|---|
| 1-10 | DeviceInformationGtw08 |  | Manufacturer Code (= VAT code) of the device | 20 | OCTETSTRING |  | R | 1.00 |
| 12 | DeviceInformationGtw08 | AP059 | Alternative Modbus mapping | 1 | UINT8 | 0: the register 259 is the same as the heat demand PDO (7 : Heating and 8 : Cooling) 1: for Siemens systems, register 259 (1: Cooling and 2: Heating | r/W | 1.02 |

### SystemDiscovery (3)
| Register/Block | Sheet | FriendlyName | Description | Bytes | Data Type | Format | Access | Version |
|---:|---|---|---|---:|---|---|---|---|
| 197 | SystemDiscovery |  | Buffer Tank is active on the appliance | 1 | UINT8 | 0 : No 1: Yes | R |  |
| 198 | SystemDiscovery |  | the appliance is part of a cascade | 1 | UINT8 | 0 : No 1: Cascade Master 2: Cascade Slave | R |  |
| 200 | SystemDiscovery |  | Reset discovery table. Set to 0x5A to execute the order. Reset to 0 by the GTW-08 | 1 | UINT8 |  | R/W | 1.00 |

### MainControlMonitoring (16)
| Register/Block | Sheet | FriendlyName | Description | Bytes | Data Type | Format | Access | Version |
|---:|---|---|---|---:|---|---|---|---|
| 260 | MainControlMonitoring |  | External Remote Management: Heat demand Temperature setpoint Cooling to send to the CU device | 2 | INT16 | 0,01°C | R/W | 1.02 |
| 276 | MainControlMonitoring |  | Special Status bitfield of the appliance /cascade | 1 | UINT8 | Bit 0: Shutdown Bit 1: Heating Bit 2: Cooling Bit 3: Screed drying Bit 4: Electric Bit 5: FrostProtection Bit 6: SummerWinter Bit 7: SummerNeutralBand | R | 1.00 |
| 278 | MainControlMonitoring |  | Appliance error priority | 1 | ENUM8 | 0 : Locking 3 : Blocking 6 : Warning 255 : No error | R | 1.00 |
| 288-289 | MainControlMonitoring | PC002 | Counter burner starts | 4 | UINT32 | Unit | R | 1.00 |
| 290-291 | MainControlMonitoring | PC003 | Counter Burning Hours | 4 | UINT32 | Hours | R | 1.00 |
| 292 | MainControlMonitoring | AC002 | Number of hours appliance was active after service | 2 | UINT16 | 2Hours | R | 1.00 |
| 293-294 | MainControlMonitoring | AC004 | Number of successful Compressor Starts after service | 4 | UINT32 | Unit | R | 1.00 |
| 295-296 | MainControlMonitoring | AC030 | counter Backup1 starts | 4 | UINT32 | Unit | R | 1.00 |
| 297-298 | MainControlMonitoring | AC028 | counter Backup1 Hours | 4 | UINT32 | Unit | R | 1.00 |
| 299-300 | MainControlMonitoring | AC031 | counter Backup2 starts | 4 | UINT32 | Unit | R | 1.00 |
| 301-302 | MainControlMonitoring | AC029 | counter Backup2 Hours | 4 | UINT32 | Hours | R | 1.00 |
| 303-304 | MainControlMonitoring | AC001 | Number of hours appliance was active | 4 | UINT32 | Hours | R | 1.00 |
| 340 | MainControlMonitoring |  | Status bitfields number 1. Relevant for the HMI output | 1 | UINT8 | - | R | 1.02 |
| 341 | MainControlMonitoring |  | Status bitfields number 2. Relevant for the HMI output | 1 | UINT8 | - | R | 1.02 |
| 342 | MainControlMonitoring |  | Status bitfields number 3. Relevant for the HMI output | 1 | UINT8 | - | R | 1.02 |
| 350 | MainControlMonitoring | AP050 | Appliance Time |  | OCTETSTRING | Absolute time in milliseconds after midnight and the number of days since January 1, 1984 | R/W | 1.00 |

### Boiler(Appliance) (41)
| Register/Block | Sheet | FriendlyName | Description | Bytes | Data Type | Format | Access | Version |
|---:|---|---|---|---:|---|---|---|---|
| 390 | Boiler(Appliance) |  | Alarm codes when there is an alarm condition | 2 | INT16 | 1 | R | 1,03 |
| 416 | Boiler(Appliance) |  | Internal heat demand - Power | 1 | UINT8 | 0.01 | R | 1.00 |
| 417 | Boiler(Appliance) |  | Internal heat demand - temperature Setpoint | 2 | INT16 | 0,01°C | R |  |
| 418 | Boiler(Appliance) |  | Internal heat demand - heatdemandType | 2 | UINT8 | 0 : None 1 : DHW primary 2 : DHW high priority 3 : Process heat 4 : Screed Drying 5 : DHW medium priority 6 : DHW low priority 7 : Central Heating 8 : Cooling 9 : Electrical active 10: Electrical Reactive | R |  |
| 453 | Boiler(Appliance) | HM069 | current speed of the condenser pump | 2 | UINT16 | 1E-3 | R | 1.02 |
| 454-455 | Boiler(Appliance) | HC000 | counter of the operating hours of the condenser pump (also called Hp Pump) | 4 | UINT32 | Hours | R | 1.02 |
| 456 | Boiler(Appliance) | HM062 | the actual current of the ODU as measured by the ODU, is used in the ODU unit to protect against too high current | 2 | UINT16 | 0,1A | R | 1.02 |
| 457 | Boiler(Appliance) |  | operation mode of the outdoor unit, in the current contrôle scheme onfle the HEAT(1) and COOL(2) modes are used, The current default is HEAT(1) | 2 | UINT16 | 0 : standby 1 : heating 2 : DHW high priority 3 : cooling | R | 1.02 |
| 458 | Boiler(Appliance) | HM003 | system flow temperature setpoint including backups | 2 | UINT16 | 0,01°C | R | 1.02 |
| 462 | Boiler(Appliance) | HM031 | Instantaneous COP calculated by Hybrid application | 2 | UINT16 | 1E-3 | R | 1.03 |
| 463 | Boiler(Appliance) | HM032 | COP threshold calculated by hybrid | 2 | UINT16 | 1E-3 | R | 1.03 |
| 464 | Boiler(Appliance) | HP061 | Hybrid mode selected | 1 | ENUM8 | 0 : No Hybrid 1 : Hybrid Cost 2 : Hybrid Primary Energy 3 : Hybrid CO2 | R/W | 1.03 |
| 465 | Boiler(Appliance) | HP062 | Hybrid Electricity cost in high tarif | 1 | UINT8 | 1 | R/W | 1.03 |
| 466 | Boiler(Appliance) | HP063 | Hybrid Electricity cost in low tarif | 1 | UINT8 | 1 | R/W | 1.03 |
| 467 | Boiler(Appliance) | HP064 | cost of ofssil energy (oil or gas) - piece per litre or peu m3 | 1 | UINT8 | 1 | R/W | 1.03 |
| 468 | Boiler(Appliance) | HP065 | Electrical CO2 emission in heating mode | 1 | UINT8 | 1 | R/W | 1.03 |
| 469 | Boiler(Appliance) | HP066 | Electrical CO2 emission in DHW mode | 1 | UINT8 | 1 | R/W | 1.03 |
| 470 | Boiler(Appliance) | HP067 | Gas or Oil CO2 emission | 1 | UINT8 | 1 | R/W | 1.03 |
| 471 | Boiler(Appliance) | HP068 | Boiler in appliance efficiency | 1 | UINT8 | 0.01 | R/W | 1.03 |
| 472 | Boiler(Appliance) | HP054 | COP threshold above which heat pump is authorized to operate when hybrid mode is primary energy | 2 | UINT16 | 0.01 | R/W | 1.03 |
| 473 | Boiler(Appliance) | AP098 | Logic contact to take into account for Blocking input 1 | 1 | ENUM8 | 0 : Open 1 : Closed | R/W | 1.02 |
| 474 | Boiler(Appliance) | AP099 | Logic contact to take into account for Blocking input 2 | 1 | ENUM8 | 0 : Open 1 : Closed | R/W | 1.02 |
| 475 | Boiler(Appliance) | AP100 | Blocking input 2 setting | 1 | ENUM8 | 0 : Not Used 1 : Full Blocking 2 : Partial Blocking 3 : User Reset Locking 4 : Backup Relieved 5 : Generator Relieved 6 : Generator And Backup relieved 7 : High Tarif - Low Tarif 8 : Photovoltaic Heat Pump Only 9 : Photovoltaic Heat Pump and Backup 10: Smart Grid Ready 11: Heating Colling 12: Central Heating Blocking | R/W | 1.02 |
| 476 | Boiler(Appliance) | AP001 | Function blocking input | 1 | ENUM8 | 0 : Not Used 1 : Full Blocking 2 : Partial Blocking 3 : User Reset Locking 4 : Backup Relieved 5 : Generator Relieved 6 : Generator And Backup relieved 7 : High Tarif - Low Tarif 8 : Photovoltaic Heat Pump Only 9 : Photovoltaic Heat Pump and Backup 10: Smart Grid Ready 11: Heating Colling 12: Central Heating Blocking | R/W | 1.02 |
| 477 | Boiler(Appliance) | DP048 | Minimum heating time before Domestic Hot Water production | 1 | UINT8 | 1H | R/W | 1.02 |
| 478 | Boiler(Appliance) | DP047 | Maximum time allowed to produce Domestic Hot Water | 1 | UINT8 | 1H | R/W | 1.02 |
| 479 | Boiler(Appliance) | DP051 | Domestic Hot Water ECO or COMFORT setting | 1 | ENUM8 | 0 : Eco Only HP 1: Comfort HP Boiler | R/W | 1.02 |
| 480 | Boiler(Appliance) | AM002 | Low Noise Mode state | 1 | ENUM8 | 0: NoSilentMode 1: Silent Mode Level 1 2: Silent Mode Level 2 3: Silent Mode Level 3 4: Silent Mode Level 4 5: Silent Mode Level 5 | R | 1.02 |
| 481 | Boiler(Appliance) | HM009 | Heat Pump Defrost | 1 | ENUM8 | 0 : No 1: Yes | R | 1.02 |
| 482 | Boiler(Appliance) | HP029 | Set the type of backup used in the heat pump. | 1 | ENUM8 | 0 : NoBackUp 1 : 1 stage Electrical BackUp 2 : 2 stages Electrical Backup 3: Boiler BackUp | R/W | 1.03 |
| 483 | Boiler(Appliance) |  | Actual relative power produced for PDO output | 1 | UINT8 | 0.01 | R | 1.03 |
| 484 | Boiler(Appliance) | HP062 | Hybrid Electricity cost in high tarif accurate | 2 | UINT16 | 0.01 | R/W | 1.03 |
| 485 | Boiler(Appliance) | HP063 | Hybrid Electricity cost in low tarif accurate | 2 | UINT16 | 0.01 | R/W | 1.03 |
| 486 | Boiler(Appliance) | HP064 | Cost of fossil energy (oil or gas) - price per liter or per m3 accurate | 2 | UINT16 | 0.01 | R/W | 1.03 |
| 487 | Boiler(Appliance) | HP000 | Outside temperature level above which the backup operation is blocked for a standard heating mode | 2 | INT16 | 0.01°C | R/W | 1.03 |
| 488 | Boiler(Appliance) | HP030 | Delay for starting the next generator (backup stage) in central heating mode | 2 | UINT16 | 1 min | R/W | 1.03 |
| 489 | Boiler(Appliance) | HP051 | Minimum oustide temperature below which Heat Pump is stopped | 2 | INT16 | 0.01°C | R/W | 1.03 |
| 490 | Boiler(Appliance) | HP058 | Enabling Heat pump Silent mode | 1 | ENUM8 | 0: NoSilentMode 1: SilentModeLevel1 2: SilentModeLevel2 3: SilentModeLevel3 4: SilentModeLevel4 5: SilentModeLevel5 | R/W | 1.03 |
| 491 | Boiler(Appliance) | HP094 | Start time for low noise function | 1 | UINT8 | 1 Hour minute | R/W | 1.03 |
| 492 | Boiler(Appliance) | HP095 | stop time for low noise | 1 | UINT8 | 1 Hour Minute | R/W | 1.03 |
| 493-494 | Boiler(Appliance) | AC027 | Total amount of pump starts | 4 | UINT32 | 1 | R | 1.03 |

### Service (13)
| Register/Block | Sheet | FriendlyName | Description | Bytes | Data Type | Format | Access | Version |
|---:|---|---|---|---:|---|---|---|---|
| 530 | Service |  | Current error generic code | 2 | UINT16 | 0-255 | R |  |
| 540 | Service |  | Code error of the device located on instance 5(CF System Discovery table Modbus Address 153) | 2 | UINT16 | 0xFFFF: No error 0xFFFE: Device Not availabe otherwise error (eg 0x0207 = "02.07" Water pressure error Cf manual) | R | 1.00 |
| 541 | Service |  | Error gravity error of the device located on instance 5 | 1 | ENUM8 | 0 : Locking 3 : Blocking 6 : Warning 0xFE : Device Not availabe (since version 1.01) | R | 1.00 |
| 542 | Service |  | Code error of the device located on instance 6(CF System Discovery table Modbus Address 159) | 2 | UINT16 | 0xFFFF: No error 0xFFFE: Device Not availabe otherwise error (eg 0x0207 = "02.07" Water pressure error Cf manual) | R | 1.00 |
| 543 | Service |  | Error gravity error of the device located on instance 6 | 1 | ENUM8 | 0 : Locking 3 : Blocking 6 : Warning 0xFE : Device Not availabe (since version 1.01) | R | 1.00 |
| 544 | Service |  | Code error of the device located on instance 7(CF System Discovery table Modbus Address 165) | 2 | UINT16 | 0xFFFF: No error 0xFFFE: Device Not availabe otherwise error (eg 0x0207 = "02.07" Water pressure error Cf manual) | R | 1.00 |
| 545 | Service |  | Error gravity error of the device located on instance 7 | 1 | ENUM8 | 0 : Locking 3 : Blocking 6 : Warning 0xFE : Device Not availabe (since version 1.01) | R | 1.00 |
| 546 | Service |  | Code error of the device located on instance 8(CF System Discovery table Modbus Address 171) | 2 | UINT16 | 0xFFFF: No error 0xFFFE: Device Not availabe otherwise error (eg 0x0207 = "02.07" Water pressure error Cf manual) | R | 1.00 |
| 547 | Service |  | Error gravity error of the device located on instance 8 | 1 | ENUM8 | 0 : Locking 3 : Blocking 6 : Warning 0xFE : Device Not availabe (since version 1.01) | R | 1.00 |
| 548 | Service |  | Code error of the device located on instance 9(CF System Discovery table Modbus Address 177) | 2 | UINT16 | 0xFFFF: No error 0xFFFE: Device Not availabe otherwise error (eg 0x0207 = "02.07" Water pressure error Cf manual) | R | 1.00 |
| 549 | Service |  | Error gravity error of the device located on instance 9 | 1 | ENUM8 | 0 : Locking 3 : Blocking 6 : Warning 0xFE : Device Not availabe (since version 1.01) | R | 1.00 |
| 550 | Service |  | Code error of the device located on instance 10(CF System Discovery table Modbus Address 183) | 2 | UINT16 | 0xFFFF: No error 0xFFFE: Device Not availabe otherwise error (eg 0x0207 = "02.07" Water pressure error Cf manual) | R | 1.00 |
| 551 | Service |  | Error gravity error of the device located on instance 10 | 1 | ENUM8 | 0 : Locking 3 : Blocking 6 : Warning 0xFE : Device Not availabe (since version 1.01) | R | 1.00 |

### Zones X12 (36)
| Register/Block | Sheet | FriendlyName | Description | Bytes | Data Type | Format | Access | Version |
|---:|---|---|---|---:|---|---|---|---|
| 642 | Zones X12 | 3202 | 3202 | Zone Short Name | 6 | VISIBLE_STRING | eg "CIRCA1" | R |
| 646 | Zones X12 | 3206 | 3206 | device instance owning the zone (CF system discovery Table) | 1 | UINT8 |  | R |
| 689 | Zones X12 | 3249 | 3249 | Time program 1 | 20 | OCTET_STRING |  | R/W |
| 699 | Zones X12 | 3259 | 3259 |  | 20 | OCTET_STRING |  | R/W |
| 709 | Zones X12 | 3269 | 3269 |  | 20 | OCTET_STRING |  | R/W |
| 719 | Zones X12 | 3279 | 3279 |  | 20 | OCTET_STRING |  | R/W |
| 729 | Zones X12 | 3289 | 3289 |  | 20 | OCTET_STRING |  | R/W |
| 739 | Zones X12 | 3299 | 3299 |  | 20 | OCTET_STRING |  | R/W |
| 749 | Zones X12 | 3309 | 3309 |  | 20 | OCTET_STRING |  | R/W |
| 759 | Zones X12 | 3319 | 3319 | Time program 2 | 20 | OCTET_STRING |  | R/W |
| 769 | Zones X12 | 3329 | 3329 |  | 20 | OCTET_STRING |  | R/W |
| 779 | Zones X12 | 3339 | 3339 |  | 20 | OCTET_STRING |  | R/W |
| 789 | Zones X12 | 3349 | 3349 |  | 20 | OCTET_STRING |  | R/W |
| 799 | Zones X12 | 3359 | 3359 |  | 20 | OCTET_STRING |  | R/W |
| 809 | Zones X12 | 3369 | 3369 |  | 20 | OCTET_STRING |  | R/W |
| 819 | Zones X12 | 3379 | 3379 |  | 20 | OCTET_STRING |  | R/W |
| 829-830 | Zones X12 | 3389 | 3389 | Time program 3 | 20 | OCTET_STRING |  | R/W |
| 839 | Zones X12 | 3399 | 3399 |  | 20 | OCTET_STRING |  | R/W |
| 849 | Zones X12 | 3409 | 3409 |  | 20 | OCTET_STRING |  | R/W |
| 859 | Zones X12 | 3419 | 3419 |  | 20 | OCTET_STRING |  | R/W |
| 869 | Zones X12 | 3429 | 3429 |  | 20 | OCTET_STRING |  | R/W |
| 879 | Zones X12 | 3439 | 3439 |  | 20 | OCTET_STRING |  | R/W |
| 889 | Zones X12 | 3449 | 3449 |  | 20 | OCTET_STRING |  | R/W |
| 899-900 | Zones X12 | 3459 | 3459 | Time program 4 Cooling | 20 | OCTET_STRING |  | R/W |
| 909 | Zones X12 | 3469 | 3469 |  | 20 | OCTET_STRING |  | R/W |
| 919 | Zones X12 | 3479 | 3479 |  | 20 | OCTET_STRING |  | R/W |
| 929 | Zones X12 | 3489 | 3489 |  | 20 | OCTET_STRING |  | R/W |
| 939 | Zones X12 | 3499 | 3499 |  | 20 | OCTET_STRING |  | R/W |
| 949 | Zones X12 | 3509 | 3509 |  | 20 | OCTET_STRING |  | R/W |
| 959 | Zones X12 | 3519 | 3519 |  | 20 | OCTET_STRING |  | R/W |
| 971 | Zones X12 | 3531 | 3531 | Start Time holiday Mode | 6 | OCTET_STRING | Absolute time in milliseconds after midnight and the number of days since January 1, 1984. Timestamp format : Time_Of_Day | R/W |
| 974 | Zones X12 | 3534 | 3534 | End Time holiday Mode | 6 | OCTET_STRING | Absolute time in milliseconds after midnight and the number of days since January 1, 1984. Timestamp format : Time_Of_Day | R/W |
| 978 | Zones X12 | 3538 | 3538 | End change mode Time | 6 | OCTET_STRING | Absolute time in milliseconds after midnight and the number of days since January 1, 1984. Timestamp format : Time_Of_Day | R/W |
| 981 | Zones X12 | 3541 | CP280 to CP289 | Flow temperature set point requested during cooling | 2 | UINT16 | 0,01°C | R/W |
| 1119 | Zones X12 | 3679 | CM040 to CM049 or DM001 | Tank temperature DHW tank (bottom sensor) | 2 | INT16 | 0,01°C | R |
| 1120 | Zones X12 | 3680 | CM250 to CM259 or DM006 | Tank temperature DHW tank (Top sensor) | 2 | INT16 | 0,01°C | R |

### BufferTank (22)
| Register/Block | Sheet | FriendlyName | Description | Bytes | Data Type | Format | Access | Version |
|---:|---|---|---|---:|---|---|---|---|
| 7500 | BufferTank | BP014 | Hysteresis to start buffer loading | 2 | INT16 | 0,01°C | R/W | 1.00 |
| 7501 | BufferTank | BP019 | Hysteresis to stop buffer tank loading | 2 | INT16 | 0,01°C | R/W | 1.00 |
| 7502 | BufferTank | BP015 | Minimum duration of post-operation of the buffer tank pump | 1 | UINT8 | 1 Min | R/W | 1.00 |
| 7503 | BufferTank | BP002 | Heating Cooling Control strategy used with buffer tank | 1 | ENUM8 | 0: Fixed Setpoint 1: Calculated Setpoint 2: Dedicated Slope | R/W | 1.00 |
| 7504 | BufferTank | BP003 | Fixed setpoint requested by buffer tank in Heating Mode | 2 | UINT16 | 0,01°C | R/W | 1.00 |
| 7505 | BufferTank | BP004 | Fixed setpoint requested by buffer tank in Cooling Mode | 2 | UINT16 | 0,01°C | R/W | 1.00 |
| 7506 | BufferTank | BP005 | Buffer Tank Slope | 1 | UINT8 | 0.1 | R/W | 1.00 |
| 7507 | BufferTank | BP013 | Offset to add to the calculate Setpoint | 2 | UINT16 | 0,01°C | R/W | 1.00 |
| 7508-7517 | BufferTank |  | Time program buffer tank | 20 | OCTET_STRING |  | R/W | 1.00 |
| 7518-7527 | BufferTank |  | (no description) | 20 | OCTET_STRING |  | R/W | 1.00 |
| 7528-7537 | BufferTank |  | (no description) | 20 | OCTET_STRING |  | R/W | 1.00 |
| 7538-7547 | BufferTank |  | (no description) | 20 | OCTET_STRING |  | R/W | 1.00 |
| 7548-7557 | BufferTank |  | (no description) | 20 | OCTET_STRING |  | R/W | 1.00 |
| 7558-7567 | BufferTank |  | (no description) | 20 | OCTET_STRING |  | R/W | 1.00 |
| 7568-7577 | BufferTank |  | (no description) | 20 | OCTET_STRING |  | R/W | 1.00 |
| 7600 | BufferTank | BM001 | Measured buffer temperature bottom | 2 | INT16 | 0,01°C | R | 1.00 |
| 7601 | BufferTank | BM002 | Measured buffer temperature top | 2 | INT16 | 0,01°C | R | 1.00 |
| 7602 | BufferTank | BM021 | State buffer tank pump | 1 | ENUM8 | 0: OFF 1: ON | R | 1.00 |
| 7603 | BufferTank | BM020 | The buffer tank Mode | 1 | ENUM8 | 0 : Decoupling Tank 1 : Storage Tank | R | 1.00 |
| 7604 | BufferTank |  | Buffer Tank winning heat demand request : the winning heat demand requested by the zones connected after the buffer tank - Power | 1 | UINT8 | 0.01 | R | 1.00 |
| 7605 | BufferTank |  | Buffer Tank winning heat demand request : the winning heat demand requested by the zones connected after the buffer tank - temperature Setpoint | 2 | INT16 | 0,01°C | R |  |
| 7606 | BufferTank |  | Buffer Tank winning heat demand request : the winning heat demand requested by the zones connected after the buffer tank - heatdemandType | 1 | UINT8 | 0 : None 1 : DHW primary 2 : DHW high priority 3 : Process heat 4 : Screed Drying 5 : DHW medium priority 6 : DHW low priority 7 : Central Heating 8 : Cooling 9 : Electrical active 10: Electrical Reactive | R |  |

### Cascade (110)
| Register/Block | Sheet | FriendlyName | Description | Bytes | Data Type | Format | Access | Version |
|---:|---|---|---|---:|---|---|---|---|
| 7000 | Cascade |  | Appliance Number on cascade: | 1 | UINT8 | 1 :Master 3 - 127 : Slave 255: not part of cascade | R | 1.00 |
| 7001 | Cascade | NP014 | Mode on cascade | 1 | ENUM8 | 0 :Automatic 1 : Heating Only 2 : Cooling Only | R/W | 1.00 |
| 7002 | Cascade | NP006 | Type of Cascade : Traditional or PARALLEL | 1 | ENUM8 | 0 :TRADITIONAL 1 : PARALLEL | R/W | 1.00 |
| 7003 | Cascade | NP005 | This parameter is used to set the master boiler. | 1 | UINT8 | 0: The master boiler switches automatically every 7 days 1 -127: The master boiler is always the one defined by this value | R/W | 1.00 |
| 7004 | Cascade | NP009 | Time delay for starting up or shutting down producers | 1 | UINT8 | Min | R/W | 1.00 |
| 7005 | Cascade | NP007 | Outside temperature triggering all stages in parallel mode | 2 | INT16 | 0,01°C | R/W | 1.00 |
| 7006 | Cascade | NP010 | Outside temperature triggering all stages in parallel mode | 2 | INT16 | 0,01°C | R/W | 1.00 |
| 7007 | Cascade | NP012 | Rise Time to Acheive Setpoint | 1 | UINT8 | 0-10 | R/W | 1.00 |
| 7008 | Cascade | AP083 | Enabled the master functionnality of this device one the S-Bus, If multople devices have this parameter all will be reset to 0 automatically, | 1 | ENUM8 | 0 : No 1: Yes | R/W | 1.02 |
| 7009 | Cascade | NP011 | choice of cascade algorithm type, power or temperature | 1 | ENUM8 | 0 : Temperature 1 : Power | R/W | 1.02 |
| 7010 | Cascade | NP289 | The maximum flow temperature the système is allowed to produce | 2 | UINT16 | 0,01°C | R/W | 1.02 |
| 7011 | Cascade | NP223 | the type of start order permutation, to determine which producer to start first | 1 | ENUM8 | 0 : Fixed Time 1: Operating hours | R/W | 1.02 |
| 7012-7013 | Cascade | NP281 | The time that needs to be elapsed before switching the appliance order | 4 | UINT16 | Hours | R/W | 1.02 |
| 7013 | Cascade | NP224 | Time delay for starting and shutting down producers, to prevent repeatedly turning on/off producers. | 2 | UINT16 | 1s | R/W | 1.02 |
| 7014 | Cascade | NP225 | Switching strategy for power control of the cascade. | 1 | ENUM8 | 0 : Late On Early Off 1: Early On Late Off 2: Late On Late Off | R/W | 1.02 |
| 7015 | Cascade | NP227 | The preferred appliance for CH heat production | 1 | UINT8 | 0-255 | R/W | 1.02 |
| 7016 | Cascade | NP228 | The non-preferred appliance for CH heat production | 1 | UINT8 | 0-255 | R/W | 1.02 |
| 7017 | Cascade | NP282 | The power percentage for the late on strategy for activating the next appliance | 1 | UINT8 | 0.01 | R/W | 1.02 |
| 7018 | Cascade | NP283 | The power percentage for the late off strategy for deactivating the last appliance | 1 | UINT8 | 0.01 | R/W | 1.02 |
| 7019 | Cascade | NP284 | The power percentage for the early on strategy for activating the next appliance | 1 | UINT8 | 0.01 | R/W | 1.02 |
| 7020 | Cascade | NP285 | The power percentage for the early off strategy for deactivating the last appliance | 1 | UINT8 | 0.01 | R/W | 1.02 |
| 7021 | Cascade | NP008 | Minimum duration of post-operation of the generator pump | 1 | UINT8 | Min | R/W | 1.02 |
| 7022 | Cascade | NP013 | Force Primary Pump to Stop | 1 | ENUM8 | 0 : No 1: Yes | R/W | 1.02 |
| 7023 | Cascade | NP287 | The type of primary pump | 1 | ENUM8 | 0 : None (no pump connected) 1: On / Off (the pump relays switches on and off) 2 : PWM (relay is always active, pump is controlled over PWM) 3 : 0-10V (relay is always active, pump is controlled over 0-10V) | R/W | 1.02 |
| 7024 | Cascade | NP288 | The type of secondary pump | 1 | ENUM8 | 0 : None (no pump connected) 1: On / Off (the pump relays switches on and off) 2 : PWM (relay is always active, pump is controlled over PWM) 3 : 0-10V (relay is always active, pump is controlled over 0-10V) | R/W | 1.02 |
| 7100 | Cascade | NM000 | Producer Active Number | 1 | UINT8 | 1 -127 | R | 1.00 |
| 7102 | Cascade | NM028 | Number of Producers recognised in the cascade | 1 | UINT8 | 0-255 | R | 1.00 |
| 7103 | Cascade | NM022 | Number of stages available on the Casacde | 1 | UINT8 | 0-255 | R | 1.00 |
| 7104 | Cascade | NM023 | Number of stages required on the Casacde | 1 | UINT8 | 0-255 | R | 1.00 |
| 7105 | Cascade |  | Cascade power request by the consumer manager - Power | 1 | UINT8 | 0.01 | R | 1.00 |
| 7106 | Cascade |  | Cascade power request by the consumer manager - - temperature Setpoint | 2 | INT16 | 0,01°C | R | 1.00 |
| 7107 | Cascade |  | Cascade power request by the consumer manager - heatdemandType | 1 | ENUM8 | 0 : None 1 : DHW primary 2 : DHW high priority 3 : Process heat 4 : Screed Drying 5 : DHW medium priority 6 : DHW low priority 7 : Central Heating 8 : Cooling 9 : Electrical active 10: Electrical Reactive | R | 1.00 |
| 7108 | Cascade |  | Cascade System Power Setpoint Calculated - Power | 1 | UINT8 | 0.01 | R | 1.00 |
| 7109 | Cascade |  | Cascade System Power Setpoint Calculated - temperature Setpoint | 2 | INT16 | 0,01°C | R | 1.00 |
| 7110 | Cascade |  | Cascade System Power Setpoint Calculated - heatdemandType | 1 | ENUM8 | 0 : None 1 : DHW primary 2 : DHW high priority 3 : Process heat 4 : Screed Drying 5 : DHW medium priority 6 : DHW low priority 7 : Central Heating 8 : Cooling 9 : Electrical active 10: Electrical Reactive | R | 1.00 |
| 7111 | Cascade |  | Actual power output of Appliance 1 | 1 | UINT8 | 0.01 | R | 1.00 |
| 7112 | Cascade |  | Appliance 1 Flow Temperature | 2 | INT16 | 0,01°C | R | 1.00 |
| 7113 | Cascade |  | Appliance 1 Status | 1 | UINT8 | Bit 0: Pump Active Bit 1: Power Engine Active (burner, compressor or backup) Bit 2: DHW in progress Bit 3: CH possible Bit 4: DHW possible Bit 5: Cooling possible Bit 6: Electrical possible Bit 7: Locking present | R | 1.00 |
| 7114 | Cascade |  | Appliance 1 Special Request | 1 | UINT8 | Bit 0: Frost Protect Bit 1: Frost Protect Pump Only Bit 2: Chimney / commissioning mode Bit 3: Service Request | R | 1.00 |
| 7115 | Cascade |  | Actual power output of Appliance 3 | 1 | UINT8 | 0.01 | R | 1.00 |
| 7116 | Cascade |  | Appliance 3 Flow Temperature | 2 | INT16 | 0,01°C | R | 1.00 |
| 7117 | Cascade |  | Appliance 3 Status | 1 | UINT8 | Bit 0: Pump Active Bit 1: Power Engine Active (burner, compressor or backup) Bit 2: DHW in progress Bit 3: CH possible Bit 4: DHW possible Bit 5: Cooling possible Bit 6: Electrical possible Bit 7: Locking present | R | 1.00 |
| 7118 | Cascade |  | Appliance 3 Special Request | 1 | UINT8 | Bit 0: Frost Protect Bit 1: Frost Protect Pump Only Bit 2: Chimney / commissioning mode Bit 3: Service Request | R | 1.00 |
| 7119 | Cascade |  | Actual power output of Appliance 4 | 1 | UINT8 | 0.01 | R | 1.00 |
| 7120 | Cascade |  | Appliance 4 Flow Temperature | 2 | INT16 | 0,01°C | R | 1.00 |
| 7121 | Cascade |  | Appliance 4 Status | 1 | UINT8 | Bit 0: Pump Active Bit 1: Power Engine Active (burner, compressor or backup) Bit 2: DHW in progress Bit 3: CH possible Bit 4: DHW possible Bit 5: Cooling possible Bit 6: Electrical possible Bit 7: Locking present | R | 1.00 |
| 7122 | Cascade |  | Appliance 4 Special Request | 1 | UINT8 | Bit 0: Frost Protect Bit 1: Frost Protect Pump Only Bit 2: Chimney / commissioning mode Bit 3: Service Request | R | 1.00 |
| 7123 | Cascade |  | Actual power output of Appliance 5 | 1 | UINT8 | 0.01 | R | 1.00 |
| 7124 | Cascade |  | Appliance 5 Flow Temperature | 2 | INT16 | 0,01°C | R | 1.00 |
| 7125 | Cascade |  | Appliance 5 Status | 1 | UINT8 | Bit 0: Pump Active Bit 1: Power Engine Active (burner, compressor or backup) Bit 2: DHW in progress Bit 3: CH possible Bit 4: DHW possible Bit 5: Cooling possible Bit 6: Electrical possible Bit 7: Locking present | R | 1.00 |
| 7126 | Cascade |  | Appliance 5 Special Request | 1 | UINT8 | Bit 0: Frost Protect Bit 1: Frost Protect Pump Only Bit 2: Chimney / commissioning mode Bit 3: Service Request | R | 1.00 |
| 7127 | Cascade |  | Actual power output of Appliance 6 | 1 | UINT8 | 0.01 | R | 1.00 |
| 7128 | Cascade |  | Appliance 6 Flow Temperature | 2 | INT16 | 0,01°C | R | 1.00 |
| 7129 | Cascade |  | Appliance 6 Status | 1 | UINT8 | Bit 0: Pump Active Bit 1: Power Engine Active (burner, compressor or backup) Bit 2: DHW in progress Bit 3: CH possible Bit 4: DHW possible Bit 5: Cooling possible Bit 6: Electrical possible Bit 7: Locking present | R | 1.00 |
| 7130 | Cascade |  | Appliance 6 Special Request | 1 | UINT8 | Bit 0: Frost Protect Bit 1: Frost Protect Pump Only Bit 2: Chimney / commissioning mode Bit 3: Service Request | R | 1.00 |
| 7131 | Cascade |  | Actual power output of Appliance 7 | 1 | UINT8 | 0.01 | R | 1.00 |
| 7132 | Cascade |  | Appliance 7 Flow Temperature | 2 | INT16 | 0,01°C | R | 1.00 |
| 7133 | Cascade |  | Appliance 7 Status | 1 | UINT8 | Bit 0: Pump Active Bit 1: Power Engine Active (burner, compressor or backup) Bit 2: DHW in progress Bit 3: CH possible Bit 4: DHW possible Bit 5: Cooling possible Bit 6: Electrical possible Bit 7: Locking present | R | 1.00 |
| 7134 | Cascade |  | Appliance 7 Special Request | 1 | UINT8 | Bit 0: Frost Protect Bit 1: Frost Protect Pump Only Bit 2: Chimney / commissioning mode Bit 3: Service Request | R | 1.00 |
| 7135 | Cascade |  | Actual power output of Appliance 8 | 1 | UINT8 | 0.01 | R | 1.00 |
| 7136 | Cascade |  | Appliance 8 Flow Temperature | 2 | INT16 | 0,01°C | R | 1.00 |
| 7137 | Cascade |  | Appliance 8 Status | 1 | UINT8 | Bit 0: Pump Active Bit 1: Power Engine Active (burner, compressor or backup) Bit 2: DHW in progress Bit 3: CH possible Bit 4: DHW possible Bit 5: Cooling possible Bit 6: Electrical possible Bit 7: Locking present | R | 1.00 |
| 7138 | Cascade |  | Appliance 8 Special Request | 1 | UINT8 | Bit 0: Frost Protect Bit 1: Frost Protect Pump Only Bit 2: Chimney / commissioning mode Bit 3: Service Request | R | 1.00 |
| 7139 | Cascade |  | Actual power output of Appliance 9 | 1 | UINT8 | 0.01 | R | 1.00 |
| 7140 | Cascade |  | Appliance 9 Flow Temperature | 2 | INT16 | 0,01°C | R | 1.00 |
| 7141 | Cascade |  | Appliance 9 Status | 1 | UINT8 | Bit 0: Pump Active Bit 1: Power Engine Active (burner, compressor or backup) Bit 2: DHW in progress Bit 3: CH possible Bit 4: DHW possible Bit 5: Cooling possible Bit 6: Electrical possible Bit 7: Locking present | R | 1.00 |
| 7142 | Cascade |  | Appliance 9 Special Request | 1 | UINT8 | Bit 0: Frost Protect Bit 1: Frost Protect Pump Only Bit 2: Chimney / commissioning mode Bit 3: Service Request | R | 1.00 |
| 7143 | Cascade |  | Actual power output of Appliance 10 | 1 | UINT8 | 0.01 | R | 1.00 |
| 7144 | Cascade |  | Appliance 10 Flow Temperature | 2 | INT16 | 0,01°C | R | 1.00 |
| 7145 | Cascade |  | Appliance 10 Status | 1 | UINT8 | Bit 0: Pump Active Bit 1: Power Engine Active (burner, compressor or backup) Bit 2: DHW in progress Bit 3: CH possible Bit 4: DHW possible Bit 5: Cooling possible Bit 6: Electrical possible Bit 7: Locking present | R | 1.00 |
| 7146 | Cascade |  | Appliance 10 Special Request | 1 | UINT8 | Bit 0: Frost Protect Bit 1: Frost Protect Pump Only Bit 2: Chimney / commissioning mode Bit 3: Service Request | R | 1.00 |
| 7151-7152 | Cascade | NM112 | The requested power to fulfil the heat demand | 4 | UINT32 | 0,1kW | R | 1.02 |
| 7153 | Cascade | NM026 | Outside Temperature connected | 1 | ENUM8 | 0 : NO 1 : Yes | R | 1.02 |
| 7154 | Cascade | NM027 | Outside Temperature Used by the Cascade | 2 | INT16 | 0,01°C | R | 1.02 |
| 7155 | Cascade | NM170 | The requested power percentage | 2 | INT16 | 1E-3 | R | 1.02 |
| 7156 | Cascade | NM002 | Current Time To Start next Stage | 2 | UINT16 | 0-60 Min | R | 1.02 |
| 7157 | Cascade | NM166 | The activation of the primary pump relay | 1 | ENUM8 | 0 : Inactive 1: active | R | 1.02 |
| 7158 | Cascade | NM167 | The activation of the secondary pump relay | 1 | ENUM8 | 0 : Inactive 1: active | R | 1.02 |
| 7159 | Cascade | NM163 | The current state of the cascade system | 1 | ENUM8 | 0 : Standby 1 : Heat Demand 2 : Burner Start 3 : Burning CH 4 : Burning DHW 5 : Burner Stop 6: Pump Post Run 7: Cooling Active 8 : Controlled Stop 9 : Blocking Mode 10 : Locking Mode 11: CS Mode L CH 12 : CS Mode H CH 13 : CS Mode H DHW 14 : CS Mode Custom 15 : Manual Hd CH On 16 : Boiler Frost Prot 17 : DE Air 18 : CU Cooling 19 : Reset In Progress 200 : Auto Filling 21 : Halted 22 : Forced Calibration 23 : Factory Test 24 : Hydraulic Balancing Mode 200 : Device Mode 254 : Unknown | R | 1.02 |
| 7160-7161 | Cascade | NC000 | The amount of hours spend on producing heat for CH | 4 | UINT32 | Hours | R | 1.02 |
| 7162-7163 | Cascade | NC001 | The amount of hours spend on producing heat for DHW | 4 | UINT32 | Hours | R | 1.02 |
| 7164 | Cascade | NM165 | The measured return temperature on the LLH | 2 | INT16 | 0,01°C | R | 1.02 |
| 7165 | Cascade |  | Cascade, smart pump status - producer circuit of low loss header | 2 | UINT8 | 0-14 | R | 1.02 |
| 7166 | Cascade |  | The pump speed output after transfer function for pwm or 0-10V output signal for primary pump (producer circuit) | 1 | UINT8 | 1E-3 | R | 1.02 |
| 7167 | Cascade |  | The pump speed output after transfer function for pwm or 0-10V output signal for secondary pump (consumer circuit) | 2 | UINT8 | 1E-3 | R | 1.02 |
| 7168 | Cascade | EM012 | The measured cascade flow temperature on the secondary side of the LLH | 2 | INT16 | 0,01°C | R | 1.02 |
| 7200 | Cascade | NP231 | The order in which the producers are going to be activated | 1 | UINT8 | 0-255 | R/W | 1.02 |
| 7201 | Cascade |  | Logical number that represents the physical location of a device within a cascade | 1 | UINT8 | [ Type = 0 Serial Number = 0 Logical Number = 0 Element Number = 0 Lorder = 0 Logical Name State = Not Connected ] | R/W | 1.02 |
| 7202 | Cascade |  | The availability of the device for the cascade | 1 | ENUM8 | [ Type = 0 Serial Number = 0 Logical Number = 0 Element Number = 0 Lorder = 0 Logical Name State = Not Connected ] | R/W | 1.02 |
| 7203 | Cascade | EP001 | The minimum power of an appliance in the cascade system | 2 | UINT16 | [ Power Rating = 20,0 State = None ] | R/W | 1.02 |
| 7205 | Cascade | EP086 | The maximum power of an appliance in the cascade system | 2 | UINT16 | [ Power Rating = 100,0 State = None ] | R/W | 1.02 |
| 7207 | Cascade | NM113 | List of appliances needed to fulfil the heat demand | 1 | UINT16 | 0-255 | R | 1.02 |
| 7208 | Cascade | NM171 | The temporary stored permutation order | 1 | UINT16 | 0-255 | R | 1.02 |
| 7209 | Cascade | EM058 | The status of all producers found on the S-Bus | 1 | ENUM8 | 0 : Standby 1 : Heat Demand 2 : Burner Start 3 : Burning CH 4 : Burning DHW 5 : Burner Stop 6: Pump Post Run 7: Cooling Active 8 : Controlled Stop 9 : Blocking Mode 10 : Locking Mode 11: CS Mode L CH 12 : CS Mode H CH 13 : CS Mode H DHW 14 : CS Mode Custom 15 : Manual Hd CH On 16 : Boiler Frost Prot 17 : DE Air 18 : CU Cooling 19 : Reset In Progress 200 : Auto Filling 21 : Halted 22 : Forced Calibration 23 : Factory Test 24 : Hydraulic Balancing Mode 200 : Device Mode 254 : Unknown | R | 1.02 |
| 7210 | Cascade | EM208 | The generic error codes of all producers found on the S-Bus | 1 | UINT8 | [Error Code = 0,0 Error Category = 1,0] | R | 1.02 |
| 7211-7212 | Cascade | EM068 | Matrix describing the error priority and the error custom code per brand | 4 | UINT32 |  | R | 1.02 |
| 7213 | Cascade | EM078 | Flow temperature of appliance. The temperature of the water leaving the appliance. | 2 | INT16 | 0,01°C | R | 1.02 |
| 7214 | Cascade | EM088 | The return temperature of an appliance in the cascade system | 2 | INT16 | 0,01°C | R | 1.02 |
| 7215 | Cascade | EM098 | The heat exchanger temperature of an appliance in the cascade system | 2 | INT16 | 0,01°C | R | 1.02 |
| 7216 | Cascade | EM108 | The flu gas temperature of an appliance in the cascade system | 2 | INT16 | 0,1°C | R | 1.02 |
| 7217 | Cascade | EM118 | Current or upcoming service notification | 1 | ENUM8 | 0 : None 1 : A 1 : B 2 : C 4 : Custom 5 : D | R | 1.02 |
| 7218 | Cascade | EM128 | The water pressure of an appliance in the cascade system | 2 | UINT8 | 0,1 bar | R | 1.02 |
| 7219 | Cascade | EM148 | The 2nd return temperature of an appliance in the cascade system | 2 | INT16 | 0,01°C | R | 1.02 |
| 7220 | Cascade | EM158 | The current pump speed | 2 | UINT16 | 1E-3 | R | 1.02 |
| 7221 | Cascade | EM168 | Actual relative power of the appliance | 2 | UINT16 | 1E-4 | R | 1.02 |
| 7222-7223 | Cascade | EM178 | Total number of burner hours. For heating and domestic hot water | 4 | UINT32 | Hours | R | 1.02 |
| 7224-7225 | Cascade | EM188 | Number of burner hours for Domestic Hot Water | 4 | UINT32 | Hours | R | 1.02 |
| 7226 | Cascade | EM198 | Producer order listed with node id's | 2 | UINT8 | 0-255 | R | 1.02 |
| 7227 | Cascade | EM218 | The type of appliance in the cascade system | 2 | UINT16 | 0-65535 | R | 1.02 |
| 7228-7229 | Cascade | EM228 | The serial number of an appliance in the cascade system | 4 | UINT32 | 0-4294967295 | R/W | 1.02 |

### Solar (21)
| Register/Block | Sheet | FriendlyName | Description | Bytes | Data Type | Format | Access | Version |
|---:|---|---|---|---:|---|---|---|---|
| 8112-8113 | Solar | SC129 | Signal for storing the total solar thermal energy collected for DHW and CH. | 4 | UINT32 | 0,001 kWh | R | 1.02 |
| 8114 | Solar | SM020 | Signal for storing the actual status of the advanced solar range boiler | 1 | ENUM8 | 0 : OFF 1 : Standby 2: FrostProtection 3: PumpProtection 4: PanelProtection 5: DhwLoading 6: LoadingCH 7: Recooling 8: SolarTube | R | 1.02 |
| 8115 | Solar | SM036 | Signal for storing the instantaneous mean rotation speed of the solar pumps. | 2 | UINT16 | 1E-3 | R | 1.02 |
| 8116 | Solar | SM033 | Signal for storing the actual measured instantaneous value of the DHW tank low temperature sensor. | 2 | INT16 | 0,01°C | R | 1.02 |
| 8117 | Solar | SM034 | Signal for storing the actual measured instantaneous value of the CH tank low temperature sensor. | 2 | INT16 | 0,01°C | R | 1.02 |
| 8118 | Solar | SM023 | Signal for storing the instantaneous temperature of the heat conduct. medium at the solar collector. - collector 1 | 2 | INT16 | 0,01°C | R | 1.02 |
| 8119 | Solar | SM024 | Signal for storing the instantaneous temperature of the heat conduct. medium at the solar collector - collector 2 | 2 | INT16 | 0,01°C | R | 1.02 |
| 8120 | Solar | SM000 | Signal for storing the instantaneous status of each three way valve (ON or OFF). - valve 1 | 1 | ENUM8 | 0: OFF 1: ON | R | 1.02 |
| 8121 | Solar | SM001 | Signal for storing the instantaneous status of each three way valve (ON or OFF). - valve 2 | 1 | ENUM8 | 0: OFF 1: ON | R | 1.02 |
| 8122 | Solar |  | Reduction of the setpoint of the DHW primary based on the heat delivery of a solar collector (solar first). | 2 | INT16 | 0,01°C | R | 1.02 |
| 8123 | Solar |  | Reduction of the setpoint of a buffered CH zone based on the heat delivery of a solar collector (solar first). | 2 | INT16 | 0,01°C | R | 1.02 |
| 8141 | Solar | SP287 | Configuration of the solar hydraulics installation type. | 1 | ENUM8 | 0 : NoSolar 1: LayeredTank 2: Standard 3: TwoTanks3WV 4 : EastWestPanels 5: TwoTanksPump 6: TwoTanksHeatExchange | R/W | 1.02 |
| 8142 | Solar | SP010 | Parameter to configure the mode of the advanced solar DHW and/or CH function group. | 1 | ENUM8 | 0: OFF 1: DHW 2: CH 3 : DhwCh | R/W | 1.02 |
| 8143 | Solar | SP044 | Parameter for nominal DHW tank T° setpoint. | 2 | UINT16 | 0,01°C | R/W | 1.02 |
| 8144 | Solar | SP047 | Parameter for configuring the nominal setpoint to charge the CH tank with solar energy, possible values are within the range 8°C ~ 60°C | 2 | UINT16 | 0,01°C | R/W | 1.02 |
| 8145 | Solar | Sp034 | Parameter for configuring the maximum allowed temperature temperature in the solar panel.- collector 1 | 2 | UINT16 | 0,01°C | R/W | 1.02 |
| 8146 | Solar | Sp035 | Parameter for configuring the maximum allowed temperature temperature in the solar panel - collector 2 | 2 | UINT16 | 0,01°C | R/W | 1.02 |
| 8147 | Solar | SP045 | Parameter for maximal DHW tank T° setpoint. | 2 | UINT16 | 0,01°C | R/W | 1.02 |
| 8148 | Solar | SP048 | Parameter for maximal CH tank T° setpoint. | 2 | UINT16 | 0,01°C | R/W | 1.02 |
| 8149 | Solar | SP182 | Parameter for setting the minimal temperature rise corresponding to one step increase in pump speed. | 2 | UINT16 | 0,01°C | R/W | 1.02 |
| 8150 | Solar | SP183 | Parameter for setting the minimal temperature rise corresponding to one step increase in pump speed. | 2 | UINT16 | 0,01°C | R/W | 1.02 |

### Thermodynamic Water Heater (12)
| Register/Block | Sheet | FriendlyName | Description | Bytes | Data Type | Format | Access | Version |
|---:|---|---|---|---:|---|---|---|---|
| 9001 | Thermodynamic Water Heater | AP055 | PV function Active | 1 | ENUM8 | How PV input must be used. 0 : no pv - pv input not used 1 : with HP only - pv input can enable boost PV mode, working with HP only 2 : with HP & backup - pv input can enable boost PV mode, working with HP and backup 3 : with backup only - pv input can enable boost PV mode, working with backup only | R/W | 1.02 |
| 9002 | Thermodynamic Water Heater | AP057 | PV function Contact Logic | 1 | ENUM8 | Logic contact to take into account for PV input: 0 : normalyOpen - PV input is considered active when PV input contact is open 1 : normalyClose - PV input is considered active when PV input contact is closed | R/W | 1.02 |
| 9003 | Thermodynamic Water Heater | DP512 | Zone Dhw primary Boost PV Setpoint | 2 | UINT16 | 0.01 °C | R/W | 1.02 |
| 9004 | Thermodynamic Water Heater | AP024 | Peak/OffPeak Active | 1 | ENUM8 | How peak off / peak on input must be used. 0 : no - peak input not used 1 : yes - comfort / reduced mode is computed on peak input state instead of timeprogram | R/W | 1.02 |
| 9005 | Thermodynamic Water Heater | AP047 | Peak input contact logic configuration | 1 | ENUM8 | Logic contact to take into account for peak input: 0 : normalyOpen - peak input is considered active when peak input contact is open 1 : normalyClose - peak input is considered active when peak input contact is closed | R/W | 1.02 |
| 9006 | Thermodynamic Water Heater | HP149 | Max time BackUp off when peak mode enabled | 1 | INT8 | 0.1 Hour | R/W | 1.02 |
| 9007 | Thermodynamic Water Heater | AM034 | S_PhotoVoltaicInputState | 1 | ENUM8 | 0 : Open 1 : Closed 2: Off | R | 1.02 |
| 9008 | Thermodynamic Water Heater | AM032 | S_PeakOffPeakInputState | 1 | ENUM8 | 0 : Open 1 : Closed 2: Off | R | 1.02 |
| 9009 | Thermodynamic Water Heater | HP059 | Digital input 1 configuration | 1 | ENUM8 | Digital input configuration 0 - off 1 - smartGrid 2 - release compressor 3 - release backup | R/W | 1.02 |
| 9010 | Thermodynamic Water Heater | HP076 | Digital input 2 configuration | 1 | ENUM8 | Digital input configuration 0 - off 1 - smartGrid 2 - release compressor 3 - release backup | R/W | 1.02 |
| 9011 | Thermodynamic Water Heater | HP077 | digital input 1 contact logic configuration | 1 | ENUM8 | Logic contact to take into account for digital input: 0 : normalyOpen - digital input is considered active when digital input contact is open 1 : normalyClose - digital input is considered active when digital input contact is closed | R/W | 1.02 |
| 9012 | Thermodynamic Water Heater | HP078 | digital input 2 contact logic configuration | 1 | ENUM8 | Logic contact to take into account for digital input: 0 : normalyOpen - digital input is considered active when digital input contact is open 1 : normalyClose - digital input is considered active when digital input contact is closed | R/W | 1.02 |

### Hybrid (27)
| Register/Block | Sheet | FriendlyName | Description | Bytes | Data Type | Format | Access | Version |
|---:|---|---|---|---:|---|---|---|---|
| 9200 | Hybrid | AM016 | Flow temperature | 2 | INT16 | 0,01°C | R | 1.02 |
| 9201 | Hybrid | AM018 | Return temperature | 2 | INT16 | 0,01°C | R | 1.02 |
| 9202 | Hybrid | AM101 | Internal setpoint used for hot water production | 2 | UINT16 | 0,01°C | R | 1.02 |
| 9203 | Hybrid | AM019 | actual Water pressure | 1 | UINT8 | 0,1 bar | R | 1.02 |
| 9204 | Hybrid | AM012 | Status of appliance | 1 | UINT8 | 0-255 cf appliance manual | R | 1.02 |
| 9205 | Hybrid | AM014 | Sub Status of appliance | 1 | UINT8 | 0-255 cf appliance manual | R | 1.02 |
| 9206-9207 | Hybrid | PC002 | Counter burner/compressor starts | 4 | UINT32 | Unit | R | 1.02 |
| 9208-9209 | Hybrid | PC003 | Counter Burning Hours | 4 | UINT32 | Hours | R | 1.02 |
| 9210-9211 | Hybrid | AC001 | Number of hours appliance was active | 4 | UINT32 | Hours | R | 1.02 |
| 9212-9213 | Hybrid | AC005 | NTotal energy consumed for production of central heat | 4 | UINT32 | 1 kWh | R | 1.02 |
| 9214-9215 | Hybrid | AC006 | Total energy consumed for production of domestic hot water. | 4 | UINT32 | 1 kWh | R | 1.02 |
| 9216 | Hybrid | HM003 | system flow temperature setpoint including backups | 2 | UINT16 | 0,01°C | R | 1.02 |
| 9217 | Hybrid | AM010 | current pump speed | 2 | UINT16 | 1E-3 | R | 1.02 |
| 9218-9219 | Hybrid | AM047 | signal used to capture actual power calculation | 4 | UINT32 | 0,01kW | R | 1.02 |
| 9220 | Hybrid | AM011 | Service is required | 1 | UINT8 | 0: No 1: Yes | R | 1.02 |
| 9221 | Hybrid | HP061 | Hybrid mode selected | 1 | ENUM8 | 0 : No Hybrid 1 : Hybrid Cost 2 : Hybrid Primary Energy 3 : Hybrid CO2 | R/W | 1.02 |
| 9222 | Hybrid | HP062 | Hybrid Electricity cost in high tarif | 1 | UINT8 | 1 | R/W | 1.02 |
| 9223 | Hybrid | HP063 | Hybrid Electricity cost in low tarif | 1 | UINT8 | 1 | R/W | 1.02 |
| 9224 | Hybrid | HP064 | cost of ofssil energy (oil or gas) - piece per litre or peu m3 | 1 | UINT8 | 1 | R/W | 1.02 |
| 9225 | Hybrid | HP065 | Electrical CO2 emission in heating mode | 1 | UINT8 | 1 | R/W | 1.02 |
| 9226 | Hybrid | HP066 | Electrical CO2 emission in DHW mode | 1 | UINT8 | 1 | R/W | 1.02 |
| 9227 | Hybrid | HP067 | Gas or Oil CO2 emission | 1 | UINT8 | 1 | R/W | 1.02 |
| 9228 | Hybrid | HP068 | Boiler in appliance efficiency | 1 | UINT8 | 0.01 | R/W | 1.02 |
| 9229 | Hybrid | HP054 | COP threshold above which heat pump is authorized to operate when hybrid mode is primary energy | 2 | UINT16 | 0.01 | R/W | 1.02 |
| 9232 | Hybrid | HP062 | Hybrid Electricity cost in high tarif accurate | 2 | UINT16 | 0.01 | R/W | 1.03 |
| 9233 | Hybrid | HP063 | Hybrid Electricity cost in low tarif accurate | 2 | UINT16 | 0.01 | R/W | 1.03 |
| 9234 | Hybrid | HP064 | cost of fossil energy (oil or gas) - piece per litre or per m3 accurate | 2 | UINT16 | 0.01 | R/W | 1.03 |

### BMS (11)
| Register/Block | Sheet | FriendlyName | Description | Bytes | Data Type | Format | Access | Version |
|---:|---|---|---|---:|---|---|---|---|
| 21020 | BMS |  | The heat demand mode which is used in case of a communication error | 1 | ENUM8 | 0 : MaintainLastHeatDemand 1 : UseFallbackHeatDemand | R/W | 1.02 |
| 21021 | BMS |  | Fallback strategy to apply | 1 | ENUM8 | 0 : No heating or cooling 1 : Fallback Heat Demand 2 : Temporary Fallback Heat Demand | R/W | 1.02 |
| 21022 | BMS |  | Number Of Minutes To Maintain Heat Demand in fallback mode | 1 | UINT8 | 0 - 255 min | R/W | 1.02 |
| 21023 | BMS |  | fallback power setpoint | 1 | UINT8 | % | R/W | 1.02 |
| 21024 | BMS |  | fallback temperature setpoint | 2 | INT16 | °C | R/W | 1.02 |
| 21025 | BMS |  | fallback heat demand type | 1 | ENUM8 | 0 : Off 1 : Temperature Control 2 : Power Control | R/W | 1.02 |
| 21026 | BMS | EP014 | 0 - 10V input selection (temperature or power setpoint) | 1 | ENUM8 | 0 : Off 1 : Temperature Control 2 : Power Control | R/W | 1.02 |
| 21027 | BMS | EM010 | Measure of the Voltage on the 0-10V Input | 1 | UINT8 | 0,1V | R | 1.02 |
| 21028 | BMS | AP110 | Parameter to activate the 2nd return sensor | 1 | ENUM8 | 0 : Inactive 1 : Active | R/W | 1.02 |
| 21029 | BMS |  | Second return temperature | 2 | INT16 | 0,01°C | R | 1.02 |
| 21030 | BMS | GP017 | Absolute max boiler power in KW. This is the power the device can produce when burner parameters are set at maximum. | 2 | UINT16 | 0,1kW | R/W | 1.02 |

## Reservierte/blanke Quellzeilen (nicht als Lücke gezählt)
| Register/Block | Sheet | Text | Parser-Hinweis |
|---:|---|---|---|
| 199 | SystemDiscovery | Reserved for future use | reserved/future-use row in source; not counted as implementation gap |
| 261-271 | MainControlMonitoring | reserved for futur use | reserved/blank range in source; not counted as implementation gap |
| 281-287 | MainControlMonitoring | reserved for futur use | reserved/blank range in source; not counted as implementation gap |
| 305-339 | MainControlMonitoring | (blank) | reserved/blank range in source; not counted as implementation gap |
| 343-349 | MainControlMonitoring | (blank) | reserved/blank range in source; not counted as implementation gap |
| 390-399 | Boiler(Appliance) | Reserved for futur use | reserved/blank range in source; not counted as implementation gap |
| 495-499 | Boiler(Appliance) | Reserved for futur use | reserved/blank range in source; not counted as implementation gap |
| 518-530 | Service | Reserved for futur use | reserved/blank range in source; not counted as implementation gap |
| 643-644 | Zones X12 | Reserved for futur use | reserved/blank range in source; not counted as implementation gap |
| 647 | Zones X12 | Reserved for futur use | reserved/future-use row in source; not counted as implementation gap |
| 960-970 | Zones X12 | Reserved for futur use | reserved/blank range in source; not counted as implementation gap |
| 979-990 | Zones X12 | Reserved for futur use | reserved/blank range in source; not counted as implementation gap |
| 982-1099 | Zones X12 | Reserved for futur use | reserved/blank range in source; not counted as implementation gap |
| 7578-7599 | BufferTank | Reserved for futur use | reserved/blank range in source; not counted as implementation gap |
| 7024-7099 | Cascade | Reserved for future | reserved/blank range in source; not counted as implementation gap |
| 7170-7199 | Cascade | Reserved for future | reserved/blank range in source; not counted as implementation gap |
| 8123-8140 | Solar | reserved for futur | reserved/blank range in source; not counted as implementation gap |
| 21003-21019 | BMS | reserved for futur | reserved/blank range in source; not counted as implementation gap |

## Parser-Hinweise
- Mehrregister-Felder wurden aus `No. Of Bytes` in Modbus-Registerblöcke umgerechnet (`ceil(bytes/2)`).
- Einzelne XLSX-Zeilen ohne Beschreibung/Datentyp/Zugriff wurden als Fortsetzungszeilen behandelt, nicht als eigene Sensor-Kandidaten.
- Reservierte/Future-use/blanke Zeilen wurden dokumentiert, aber nicht als Implementierungslücke gezählt.
- Semantische Bedeutungen wurden nicht geraten; alle Beschreibungen stammen aus der XLSX.
- R/W-Register sind nur Kandidaten für spätere Implementierung nach separater Entscheidung.
