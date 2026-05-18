# Modbus GTW-08 - Liste der Parameter Gap Report

Quelle: `Modbus GTW-08 - Liste der Parameter 7740782-01 26072019.pdf`.
Ziel: Abgleich gegen `custom_components/broetje_heating/register_map.csv`.

Heuristik: `pdftotext -layout`; Registerzeilen benötigen Adresse, Zugriff (`Read`/`Write`) und Datentyp (`UNSIGNED16` etc.). Mehrwort-Register gelten als abgedeckt, wenn die Adresse innerhalb eines bestehenden `register`+`size`-Bereichs liegt.

- Extrahierte eindeutige Register-Kandidaten: 288
- Durch bestehende Register/Size-Bereiche abgedeckt: 164
- Fehlend in register_map.csv: 124

## Fehlende Register-Kandidaten

| Register | Datentyp | Zugriff | Display-Code | Abschnitt | Beschreibungsauszug |
|---:|---|---|---|---|---|
| 5 | VISIBLE_STRING | Read | 2001.1 | 3.3          Ungültige Werte | parApDeviceInfoManufacturerCode Byte 8   parApDeviceInfoManufacturerCode Byte 9                                             Read Herstellercode (= USt-Code) des Gerätes            VISIBLE_STRING      2001.1 |
| 197 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | BufferTankActive            Puffertank ist am Gerät aktiv                                              Read    UNSIGNED8 das Gerät ist Teil einer Kaskade 0: nein |
| 200 | UNSIGNED8 | Write |  | 3.3          Ungültige Werte | Reset discovery table                                                                                          UNSIGNED8 auszuführen. Zurücksetzen auf 0 durch das GTW-08                           Write                Variables |
| 276 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | -              ProducerManagerRequestReceived                                                                           Read     UNSIGNED8       PDO mapping |
| 288 | UNSIGNED32 | Read |  | 3.3          Ungültige Werte | varChCtrBurnerStarts 24-17        Zähler Brennerstarts                                         Read   UNSIGNED32 |
| 289 | UNSIGNED32 | Read |  | 3.3          Ungültige Werte | varChCtrBurnerStarts 16-9    varChCtrBurnerStarts 8-1          Zähler Brennerstarts                                         Read   UNSIGNED32 |
| 290 | UNSIGNED32 | Read |  | 3.3          Ungültige Werte | varChCtrBurnHours 32-25      varChCtrBurnHours 24-17           Zähler Brennerstunden                                        Read   UNSIGNED32 530C.0 |
| 291 | UNSIGNED32 | Read |  | 3.3          Ungültige Werte | varChCtrBurnHours 16-9       varChCtrBurnHours 8-1             Zähler Brennerstunden                                        Read   UNSIGNED32 varApCtrServiceBurningHo                                     Anzahl der Stunden, in denen das Gerät nach der Wartung i |
| 292 | UNSIGNED16 | Read | 5040.0 | 3.3          Ungültige Werte | varApCtrServiceBurningHours 8-1                                                                Read   UNSIGNED16       5040.0 urs 16-9                                                     Betrieb war |
| 293 | UNSIGNED32 | Read | 5042.0 | 3.3          Ungültige Werte | varApCtrServiceBurnerStarts 24-17   Anzahl erfolgreicher Verdichterstarts nach der Wartung   Read    UNSIGNED32 ts 32-25 5042.0 varApCtrServiceBurnerStar |
| 294 | UNSIGNED32 | Read |  | 3.3          Ungültige Werte | varApCtrServiceBurnerStarts 8-1     Anzahl erfolgreicher Verdichterstarts nach der Wartung   Read    UNSIGNED32 ts 16-9 varApCtrBackup1Starts 32- |
| 295 | UNSIGNED32 | Read |  | 3.3          Ungültige Werte | varApCtrBackup1Starts 24-17         Zähler Starts Zusatzerzeuger 1                           Read    UNSIGNED32 25 50B1.0 varApCtrBackup1Starts 16- |
| 296 | UNSIGNED32 | Read |  | 3.3          Ungültige Werte | varApCtrBackup1Starts 8-1           Zähler Starts Zusatzerzeuger 1                           Read    UNSIGNED32 9 varApCtrBackup1Hours 32- |
| 297 | UNSIGNED32 | Read |  | 3.3          Ungültige Werte | varApCtrBackup1Hours 24-17          Zähler Stunden Zusatzerzeuger 1                          Read    UNSIGNED32 25 50AF.0 varApCtrBackup1Hours 16- |
| 298 | UNSIGNED32 | Read |  | 3.3          Ungültige Werte | varApCtrBackup1Hours 8-1            Zähler Stunden Zusatzerzeuger 1                          Read    UNSIGNED32 9 varApCtrBackup2Starts 32- |
| 299 | UNSIGNED32 | Read |  | 3.3          Ungültige Werte | varApCtrBackup2Starts 24-17         Zähler Starts Zusatzerzeuger 2                           Read    UNSIGNED32 25 50B2.0 varApCtrBackup2Starts 16- |
| 300 | UNSIGNED32 | Read |  | 3.3          Ungültige Werte | varApCtrBackup2Starts 8-1           Zähler Starts Zusatzerzeuger 2                           Read    UNSIGNED32 9 varApCtrBackup2Hours 32- |
| 301 | UNSIGNED32 | Read |  | 3.3          Ungültige Werte | varApCtrBackup2Hours 24-17          Zähler Stunden Zusatzerzeuger 2                          Read    UNSIGNED32 25 50B0.0 varApCtrBackup2Hours 16- |
| 302 | UNSIGNED32 | Read |  | 3.3          Ungültige Werte | varApCtrBackup2Hours 8-1            Zähler Stunden Zusatzerzeuger 2                          Read    UNSIGNED32 9 |
| 303 | UNSIGNED32 | Read | 5000.0 | 3.3          Ungültige Werte | varApCtrHoursTotal16-9        varApCtrHoursTotal 8-1              Betriebsstundenzahl                                      Read    UNSIGNED32 5000.0 |
| 304 | UNSIGNED32 | Read |  | 3.3          Ungültige Werte | varApCtrHoursTotal16-9        varApCtrHoursTotal 8-1              Betriebsstundenzahl                                      Read    UNSIGNED32 305-349 -                            -                                   Für zukünftige Verwendung reserviert          |
| 351 | OCTET_STRING | Write | 3023.0 | 3.3          Ungültige Werte | parApTimeOfDay Byte 2         parApTimeOfDay Byte 3               Uhrzeit Ende Modusänderung ZeitStempel CIA                       OCTET_STRING       3023.0 Write |
| 416 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | Interne Heizanforderung - Leistung              Read   UNSIGNED8 1 varProducerInternalHeatDemand   varProducerInternalHeatDemand Byte |
| 417 | INTEGER16 | Read | 5711.1 | 3.3          Ungültige Werte | Interner Heizanforderung - Temperatursollwert   Read   INTEGER16    5711.1 Byte 3                          2 varProducerInternalHeatDemand Byte |
| 418 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | Interne Heizanforderung - HeizanforderungArt    Read   UNSIGNED8 4 |
| 540 | UNSIGNED16 | Read | 1003.1 | 3.3          Ungültige Werte | varACurrentError5 16-9   varACurrentError5 8-1   Code Fehler des Geräts an Instanz 5 (CU-EHC, EEC, SCB, ...)   Read   UNSIGNED16   1003.1 Fehlerstufe des Fehlers am Gerät an Instanz 5 0: Verriegelung |
| 542 | UNSIGNED16 | Read | 1003.1 | 3.3          Ungültige Werte | varACurrentError6 16-9   varACurrentError6 8-1   Code Fehler des Geräts an Instanz 6 (CU-EHC, EEC, SCB, ...)   Read   UNSIGNED16   1003.1 Fehlerstufe des Fehlers am Gerät an Instanz 6 0: Verriegelung |
| 544 | UNSIGNED16 | Read | 1003.1 | 3.3          Ungültige Werte | varACurrentError7 16-9   varACurrentError7 8-1   Code Fehler des Geräts an Instanz 7 (CU-EHC, EEC, SCB, ...)   Read   UNSIGNED16   1003.1 Fehlerstufe des Fehlers am Gerät an Instanz 7 0: Verriegelung |
| 546 | UNSIGNED16 | Read | 1003.1 | 3.3          Ungültige Werte | varACurrentError8 16-9   varACurrentError8 8-1   Code Fehler des Geräts an Instanz 8 (CU-EHC, EEC, SCB, ...)   Read   UNSIGNED16   1003.1 Fehlerstufe des Fehlers am Gerät an Instanz 8 0: Verriegelung |
| 548 | UNSIGNED16 | Read | 1003.1 | 3.3          Ungültige Werte | varACurrentError9 16-9   varACurrentError9 8-1   Code Fehler des Geräts an Instanz 9 (CU-EHC, EEC, SCB, ...)   Read   UNSIGNED16   1003.1 Fehlerstufe des Fehlers am Gerät an Instanz 9 0: Verriegelung |
| 550 | UNSIGNED16 | Read | 1003.1 | 3.3          Ungültige Werte | varACurrentError10 16-9   varACurrentError10 8-1   Code Fehler des Geräts an Instanz 10 (CU-EHC, EEC, SCB, ...) Read   UNSIGNED16   1003.1 Fehlerstufe des Fehlers am Gerät an Instanz 10 0: Verriegelung |
| 643 | VISIBLE_STRING | Read |  | 3.3          Ungültige Werte | parZoneFriendlyNameShort Byte 2   parZoneFriendlyNameShort Byte 3        Kreisbezeichnung kurz     Read     VISIBLE_STRING InternalVariable        "DHW" |
| 646 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | instance                                                          Read    UNSIGNED8       InternalVariable   InternalVariable Kreis gehört 28 |
| 693 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramMonday1 Byte 8            parZoneTimeProgramMonday1 Byte 9 Read/Write OCTET_STRING   3431.n      363E.n |
| 699 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramTuesday1 Byte 0           parZoneTimeProgramTuesday1 Byte 1 Read/Write OCTET_STRING   3432.n      363F.n |
| 713 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramWednesday1 Byte 8    parZoneTimeProgramWednesday1 Byte 9 Read/Write OCTET_STRING   3433.n   3640.n |
| 723 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramThursday1 Byte 8     parZoneTimeProgramThursday1 Byte 9     Read/Write OCTET_STRING   3434.n   3641.n |
| 733 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramFriday1 Byte 8      parZoneTimeProgramFriday1 Byte 9 Read/Write OCTET_STRING   3435.n   3642.n |
| 743 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramSaturday1 Byte 8    parZoneTimeProgramSaturday1 Byte 9 Read/Write OCTET_STRING   3436.n   3643.n |
| 751 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramSunday1 Byte 4      parZoneTimeProgramSunday1 Byte 5 Read/Write OCTET_STRING   3437.n   3644.n |
| 763 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramMonday2 Byte 8      parZoneTimeProgramMonday2 Byte 9 Read/Write OCTET_STRING   3438.n   3645.n |
| 773 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramTuesday2 Byte 8     parZoneTimeProgramTuesday2 Byte 9 Read/Write OCTET_STRING   3439.n   3646.n |
| 780 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramWednesday2 Byte 2   parZoneTimeProgramWednesday2 Byte 3                    Read/Write OCTET_STRING   343A.n   3647.n |
| 793 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramThursday2 Byte 8     parZoneTimeProgramThursday2 Byte 9 Read/Write OCTET_STRING   343B.n   3648.n |
| 803 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramFriday2 Byte 8       parZoneTimeProgramFriday2 Byte 9 Read/Write OCTET_STRING   343C.n   3649.n |
| 813 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramSaturday2 Byte 8    parZoneTimeProgramSaturday2 Byte 9 Read/Write OCTET_STRING   343D.n   364A.n |
| 823 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramSunday2 Byte 8      parZoneTimeProgramSunday2 Byte 9 Read/Write OCTET_STRING   343E.n   364B.n |
| 832 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramMonday3 Byte 6      parZoneTimeProgramMonday3 Byte 7        Zeitprogramm 3   Read/Write OCTET_STRING   343F.n   364C.n |
| 843 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramTuesday3 Byte 8     parZoneTimeProgramTuesday3 Byte 9 Read/Write OCTET_STRING   3440.n   364D.n |
| 853 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramWednesday3Byte 8    parZoneTimeProgramWednesday3Byte 9 Read/Write OCTET_STRING   3441.n   364E.n |
| 860 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramThursday3 Byte 2    parZoneTimeProgramThursday3 Byte 3 Read/Write OCTET_STRING   3442.n   364F.n |
| 873 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramFriday3Byte 8       parZoneTimeProgramFriday3Byte 9 Read/Write OCTET_STRING   3443.n   3650.n |
| 883 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramSaturday3 Byte 8    parZoneTimeProgramSaturday3 Byte 9 Read/Write OCTET_STRING   3444.n   3651.n |
| 889 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramSunday3Byte 0       parZoneTimeProgramSunday3Byte 1         Read/Write OCTET_STRING   3445.n   3652.n 39 |
| 903 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramMonday4 Byte 8     parZoneTimeProgramMonday4 Byte 9 Read/Write OCTET_STRING   3446.n   Not Available |
| 912 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramTuesday4 Byte 6    parZoneTimeProgramTuesday4 Byte 7 Read/Write OCTET_STRING   3447.n   Not Available |
| 923 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramWednesday4Byte 8    parZoneTimeProgramWednesday4Byte 9 Read/Write OCTET_STRING   3448.n   Not Available |
| 933 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramThursday4 Byte 8    parZoneTimeProgramThursday4 Byte 9 Read/Write OCTET_STRING   3449.n   Not Available |
| 941 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramFriday4Byte 4       parZoneTimeProgramFriday4Byte 5        Read/Write OCTET_STRING   344A.n   Not Available |
| 953 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramSaturday4 Byte 8    parZoneTimeProgramSaturday4 Byte 9 Read/Write OCTET_STRING   344B.n   Not Available |
| 963 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneTimeProgramSunday4Byte 8       parZoneTimeProgramSunday4Byte 9 Read/Write OCTET_STRING   344C.n   Not Available |
| 972 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneStartTimeHoliday Byte 2         parZoneStartTimeHoliday Byte 3                Startzeit Ferienbetrieb     Read/Write OCTET_STRING   3421.n      365E.n ZeitStempel CIA |
| 975 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneEndTimeHoliday Byte 2           parZoneEndTimeHoliday Byte 3                  Endzeit Ferienbetrieb       Read/Write OCTET_STRING   3422.n      365F.n ZeitStempel |
| 979 | OCTET_STRING | Read |  | 3.3          Ungültige Werte | parZoneEndTimeModeChange Byte 2        parZoneEndTimeModeChange Byte 3               Modusänderung               Read/Write OCTET_STRING   3423.n      3660.n ZeitStempel CIA |
| 1119 | INTEGER16 | Read | 5601.0 | 3.3          Ungültige Werte | varDhwTankTemperature 16-9      varDhwTankTemperature 8-1                                     Read   INTEGER16    5405.n       5601.0 (unterer Sensor) Speichertemperatur |
| 1120 | INTEGER16 | Read | 5606.0 | 3.3          Ungültige Werte | varDhwTankTemperatureTop 16-9   varDhwTankTemperatureTop 8-1                                  Read   INTEGER16    5433.n       5606.0 (oberer Sensor) |
| 7000 | UNSIGNED8 | Read | 4008.2 | 3.3          Ungültige Werte | vaCascadeApplianceNumber                                                     Read     UNSIGNED8     4008.2 |
| 7003 | UNSIGNED8 | Write | 3705.0 | 3.3          Ungültige Werte | parCascadePermutation                            automatisch alle 7 Tage              UNSIGNED8     3705.0 Write Andere: Der Führungskessel ist |
| 7004 | UNSIGNED8 | Write | 3709.0 | 3.3          Ungültige Werte | parCascadeInterStageTime                         Ausschaltverzögerung                 UNSIGNED8     3709.0 Write der Erzeuger Außentemperatur, ab |
| 7005 | INTEGER16 | r | 3707.0 | 3.3          Ungültige Werte | INTEGER16     3707.0 r 16 -9                                           er 8 -1                                          Parallelbetrieb aktiviert   Write werden Außentemperatur, ab |
| 7006 | INTEGER16 | r |  | 3.3          Ungültige Werte | INTEGER16     370A.0 r 16 -9                                           er 8 -1                                          Parallelbetrieb aktiviert   Write werden |
| 7007 | UNSIGNED8 | Write |  | 3.3          Ungültige Werte | parCascadePowerRiseTime                          Anstiegszeit bis zum              UNSIGNED8   370C.0 Write Erreichen des Sollwerts 7008- |
| 7100 | UNSIGNED8 | Read | 5700.0 | 3.3          Ungültige Werte | varCascadeNumberProducerFirstStart                                         Read    UNSIGNED8   5700.0 Herstellers Vorlauftemperatur |
| 7102 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | varCascadeNumberProducersPresent                 Kaskade erkannten         Read    UNSIGNED8   571C.0 Erzeuger Anzahl der in der |
| 7103 | UNSIGNED8 | Read | 5716.0 | 3.3          Ungültige Werte | varCascadeNbStageAvailable                       Kaskade verfügbaren       Read    UNSIGNED8   5716.0 Stufen Anzahl der in der Kaskade erforderlichen |
| 7104 | UNSIGNED8 | Read | 5717.0 | 3.3          Ungültige Werte | varCascadeNbStageRequired                                                  Read    UNSIGNED8   5717.0 Stufen Kaskaden- |
| 7105 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | varCascadeSystemPowerRequest Byte 1              durch den                 Read    UNSIGNED8 Verbrauchermanager - Leistung Kaskaden- |
| 7106 | INTEGER16 | Read |  | 3.3          Ungültige Werte | varCascadeSystemPowerRequest Byte 3              varCascadeSystemPowerRequest Byte 2              durch den                 Read    INTEGER16   571D.0 Verbrauchermanager - Temperatursollwert Kaskaden- |
| 7107 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | varCascadeSystemPowerRequest Byte 4              durch den                 Read    UNSIGNED8 Verbrauchermanager - HeizanforderungArt Berechneter |
| 7108 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | varCascadeSystemPowerSetpointCalculated Byte 1   Kaskadenleistungssollwe   Read    UNSIGNED8 rt - Leistung 571E.0 Berechneter |
| 7109 | INTEGER16 | Read |  | 3.3          Ungültige Werte | varCascadeSystemPowerSetpointCalculated Byte 3   varCascadeSystemPowerSetpointCalculated Byte 2   Kaskadenleistungssollwe   Read    INTEGER16 rt - Temperatursollwert 47 |
| 7111 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | PowerActualReceived1                                                       Read   UNSIGNED8   570B.1 Gerätes 1 Gerät 1 |
| 7112 | INTEGER16 | Read |  | 3.3          Ungültige Werte | FlowTemperatureReceived1 16-9   FlowTemperatureReceived1 8-1                                               Read   INTEGER16   570C.1 Vorlauftemperatur Gerät 1 Status |
| 7113 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | -        ProducerManagerStatusBitfieldReceived1           3 HZG möglich             Read   UNSIGNED8   570d.1 |
| 7114 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | -        ProducerManagerRequestReceived1                  1 Frostschutz nur Pumpe Read     UNSIGNED8   570E.1 |
| 7115 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | PowerActualReceived3                                                       Read   UNSIGNED8   570B.3 Gerätes 3 Gerät 3 |
| 7116 | INTEGER16 | Read |  | 3.3          Ungültige Werte | FlowTemperatureReceived3 16-9   FlowTemperatureReceived3 8-1                                               Read   INTEGER16   570C.3 Vorlauftemperatur Gerät 3 Status |
| 7117 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | -        ProducerManagerStatusBitfieldReceived3           (Brenner, Verdichter      Read   UNSIGNED8   570d.3 oder Zusatzerzeuger) |
| 7118 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | -        ProducerManagerRequestReceived3          1 Frostschutz nur Pumpe Read     UNSIGNED8   570E.3 |
| 7119 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | PowerActualReceived4                                               Read   UNSIGNED8   570B.4 Gerätes 4 Gerät 4 |
| 7120 | INTEGER16 | Read |  | 3.3          Ungültige Werte | FlowTemperatureReceived4 16-9   FlowTemperatureReceived4 8-1                                       Read   INTEGER16   570C.4 Vorlauftemperatur Gerät 4 Status |
| 7121 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | -        ProducerManagerStatusBitfieldReceived4   3 HZG möglich             Read   UNSIGNED8   570d.4 |
| 7122 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | -        ProducerManagerRequestReceived4                                    Read   UNSIGNED8   570E.4 |
| 7123 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | PowerActualReceived5                                              Read   UNSIGNED8   570B.5 Gerätes 5 Gerät 5 |
| 7124 | INTEGER16 | Read |  | 3.3          Ungültige Werte | FlowTemperatureReceived5 16-9   FlowTemperatureReceived5 8-1                                      Read   INTEGER16   570C.5 Vorlauftemperatur Gerät 5 Status |
| 7125 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | -        ProducerManagerStatusBitfieldReceived5   3 HZG möglich            Read   UNSIGNED8   570d.5 |
| 7126 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | -        ProducerManagerRequestReceived5          1 Frostschutz nur Pumpe Read    UNSIGNED8   570E.5 |
| 7127 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | PowerActualReceived6                                              Read   UNSIGNED8   570B.6 Gerätes 6 Gerät 6 |
| 7128 | INTEGER16 | Read |  | 3.3          Ungültige Werte | FlowTemperatureReceived6 16-9   FlowTemperatureReceived6 8-1                                      Read   INTEGER16   570C.6 Vorlauftemperatur Gerät 6 Status |
| 7129 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | -        ProducerManagerStatusBitfieldReceived6   (Brenner, Verdichter     Read   UNSIGNED8   570d.6 oder Zusatzerzeuger) |
| 7130 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | -        ProducerManagerRequestReceived6          1 Frostschutz nur Pumpe Read    UNSIGNED8   570E.6 |
| 7131 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | PowerActualReceived7                                              Read   UNSIGNED8   570B.7 Gerätes 7 Gerät 7 |
| 7132 | INTEGER16 | Read |  | 3.3          Ungültige Werte | FlowTemperatureReceived7 16-9   FlowTemperatureReceived7 8-1                                      Read   INTEGER16   570C.7 Vorlauftemperatur Gerät 7 Status |
| 7133 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | -        ProducerManagerStatusBitfieldReceived7   3 HZG möglich            Read   UNSIGNED8   570d.7 |
| 7134 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | -        ProducerManagerRequestReceived7          1 Frostschutz nur Pumpe Read    UNSIGNED8   570E.7 |
| 7135 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | PowerActualReceived8                                              Read   UNSIGNED8   570B.8 Gerätes 8 Gerät 8 |
| 7136 | INTEGER16 | Read |  | 3.3          Ungültige Werte | FlowTemperatureReceived8 16-9   FlowTemperatureReceived8 8-1                                      Read   INTEGER16   570C.8 Vorlauftemperatur Gerät 8 Status |
| 7137 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | -        ProducerManagerStatusBitfieldReceived8   3 HZG möglich            Read   UNSIGNED8   570d.8 |
| 7138 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | -        ProducerManagerRequestReceived8          1 Frostschutz nur Pumpe Read    UNSIGNED8   570E.8 |
| 7139 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | PowerActualReceived9                                              Read   UNSIGNED8   570B.9 Gerätes 9 Gerät 9 |
| 7140 | INTEGER16 | Read |  | 3.3          Ungültige Werte | FlowTemperatureReceived9 16-9   FlowTemperatureReceived9 8-1                                      Read   INTEGER16   570C.9 Vorlauftemperatur Gerät 9 Status |
| 7141 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | -        ProducerManagerStatusBitfieldReceived9   oder Zusatzerzeuger)     Read   UNSIGNED8   570d.9 |
| 7142 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | -         ProducerManagerRequestReceived9           1 Frostschutz nur Pumpe Read    UNSIGNED8   570E.9 |
| 7143 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | PowerActualReceived10                                              Read   UNSIGNED8   570B.10 Gerätes 10 Gerät 10 |
| 7144 | INTEGER16 | Read |  | 3.3          Ungültige Werte | FlowTemperatureReceived10 16-9   FlowTemperatureReceived10 8-1                                      Read   INTEGER16   570C.10 Vorlauftemperatur Gerät 10 Status |
| 7145 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | -         ProducerManagerStatusBitfieldReceived10   3 HZG möglich            Read   UNSIGNED8   570d.10 |
| 7146 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | -         ProducerManagerRequestReceived10          1 Frostschutz nur Pumpe Read    UNSIGNED8   570E.10 |
| 7500 | INTEGER16 | Write |  | 3.3          Ungültige Werte | parBufferHysteresis 16-9                 parBufferHysteresis 8-1                                                                       INTEGER16      350E.0 Hysterese Beginn Pufferspeicherladung          Write |
| 7501 | INTEGER16 | Write | 3513.0 | 3.3          Ungültige Werte | parBufferHysteresisStopLoading 16-9      parBufferHysteresisStopLoading 8-1                                                            INTEGER16      3513.0 Write Hysterese Ende Pufferspeicherladung |
| 7600 | INTEGER16 | Read | 5501.1 | 3.3          Ungültige Werte | varBufferTankTemperature1 16 -9         varBufferTankTemperature1 8 -1                                                    Read    INTEGER16    5501.1 Gemessene Pufferspeichertemperatur unten |
| 7601 | INTEGER16 | Read | 5501.2 | 3.3          Ungültige Werte | varBufferTankTemperature2 16 -9     varBufferTankTemperature2 8 -1       Gemessene Pufferspeichertemperatur oben      Read    INTEGER16   5501.2 |
| 7604 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | Read   UNSIGNED8 Byte 1                               angeschlossenen Kreisen angeforderte Wärmegewinnung - Leistung Pufferspeicheranforderung Wärmegewinnung: die |
| 7605 | INTEGER16 | Read | 5517.0 | 3.3          Ungültige Werte | Read   INTEGER16   5517.0 Byte 3                              Byte 2                               angeschlossenen Kreisen angeforderte Wärmegewinnung - Temperatursollwert Pufferspeicheranforderung Wärmegewinnung: die |
| 7606 | UNSIGNED8 | Read |  | 3.3          Ungültige Werte | Read   UNSIGNED8 Byte 4                               angeschlossenen Kreisen angeforderte Wärmegewinnung - WärmeanforderungArt |

## Abgedeckte Register-Kandidaten

| Register | Datentyp | Zugriff | Display-Code | Beschreibungsauszug |
|---:|---|---|---|---|
| 11 | UNSIGNED16 | Read | 2001.2 | DeviceType 16-9                          DeviceType 8-1                           Gerätetyp GTW-08                          Read     UNSIGNED16          2001.2 |
| 128 | UNSIGNED8 | Read |  | -              numberOfDevices             Anzahl der auf dem Gerät vorhandenen elektronischen Platinen               Read     UNSIGNED8 Variables Internal |
| 129 | UNSIGNED16 | Read |  | DeviceTypeBoard1 16-9       DeviceTypeBoard1 8-1        Gerätetyp an Instanz 1(CU-EHC, EEC, SCB, ...)                              Read     UNSIGNED16 Variables Internal |
| 130 | UNSIGNED16 | Read |  | SoftwareVersion1 16-9       SoftwareVersion1 8-1        Softwareversion des Geräts an Instanz 1(CU-EHC, EEC, SCB, ...)             Read     UNSIGNED16 Variables DeviceConfigurationTabl   DeviceConfigurationTableV   Konfigurationstabelle der Version des Geräts  |
| 131 | UNSIGNED16 | Read | 2001.13 | Read    UNSIGNED16       2001.13 eVersion1 16-9            ersion1 8-1                 ...) Internal |
| 132 | UNSIGNED16 | Read |  | HardwareVersion1 16-9       HardwareVersion1 8-1        Hardwareversion des Geräts an Instanz 1(CU-EHC, EEC, SCB, ...)             Read     UNSIGNED16 Variables |
| 133 | UNSIGNED32 | Read | 2001.12 | ArticleNumber1 32-25        ArticleNumber1 24-17 Artikelnummer des Geräts an Instanz 1(CU-EHC, EEC, SCB, ...)         Read    UNSIGNED32       2001.12 |
| 135 | UNSIGNED16 | Read |  | DeviceTypeBoard2 16-9       DeviceTypeBoard2 8-1        Gerätetyp an Instanz 2 (CU-EHC, EEC, SCB, ...)                             Read     UNSIGNED16 Variables Internal |
| 136 | UNSIGNED16 | Read |  | SoftwareVersion2 16-9       SoftwareVersion2 8-1        Softwareversion des Geräts an Instanz 2 (CU-EHC, EEC, SCB, ...)            Read     UNSIGNED16 Variables DeviceConfigurationTabl   DeviceConfigurationTableV   Konfigurationstabelle der Version des Geräts  |
| 137 | UNSIGNED16 | Read | 2001.13 | Read     UNSIGNED16       2001.13 eVersion2 16-9            ersion2 8-1                 SCB, ...) Internal |
| 138 | UNSIGNED16 | Read |  | HardwareVersion2 16-9       HardwareVersion2 8-1        Hardwareversion des Geräts an Instanz 2 (CU-EHC, EEC, SCB, ...)            Read     UNSIGNED16 Variables |
| 139 | UNSIGNED32 | Read | 2001.12 | ArticleNumber2 32-25        ArticleNumber2 24-17 Artikelnummer des Geräts an Instanz 2 (CU-EHC, EEC, SCB, ...)        Read    UNSIGNED32       2001.12 |
| 141 | UNSIGNED16 | Read |  | DeviceTypeBoard3 16-9       DeviceTypeBoard3 8-1        Gerätetyp an Instanz 3 (CU-EHC, EEC, SCB, ...)                             Read     UNSIGNED16 Variables Internal |
| 142 | UNSIGNED16 | Read |  | SoftwareVersion3 16-9       SoftwareVersion3 8-1        Softwareversion des Geräts an Instanz 3 (CU-EHC, EEC, SCB, ...)            Read     UNSIGNED16 Variables DeviceConfigurationTabl   DeviceConfigurationTableV   Konfigurationstabelle der Version des Geräts  |
| 143 | UNSIGNED16 | Read | 2001.13 | Read     UNSIGNED16       2001.13 eVersion3 16-9            ersion3 8-1                 SCB, ...) 14 |
| 144 | UNSIGNED16 | Read |  | HardwareVersion3 16-9       HardwareVersion3 8-1        Hardwareversion des Geräts an Instanz 3 (CU-EHC, EEC, SCB, ...)           Read    UNSIGNED16 Variables |
| 145 | UNSIGNED32 | Read | 2001.12 | ArticleNumber3 32-25        ArticleNumber3 24-17 Artikelnummer des Geräts an Instanz 3 (CU-EHC, EEC, SCB, ...)       Read   UNSIGNED32       2001.12 |
| 147 | UNSIGNED16 | Read |  | DeviceTypeBoard4 16-9       DeviceTypeBoard4 8-1        Gerätetyp an Instanz 4 (CU-EHC, EEC, SCB, ...)                            Read    UNSIGNED16 Variables Internal |
| 148 | UNSIGNED16 | Read |  | SoftwareVersion4 16-9       SoftwareVersion4 8-1        Softwareversion des Geräts an Instanz 4 (CU-EHC, EEC, SCB, ...)           Read    UNSIGNED16 Variables DeviceConfigurationTabl   DeviceConfigurationTableV   Konfigurationstabelle der Version des Geräts an |
| 149 | UNSIGNED16 | Read | 2001.13 | Read    UNSIGNED16       2001.13 eVersion4 16-9            ersion4 8-1                 SCB, ...) Internal |
| 150 | UNSIGNED16 | Read |  | HardwareVersion4 16-9       HardwareVersion4 8-1        Hardwareversion des Geräts an Instanz 4 (CU-EHC, EEC, SCB, ...)           Read    UNSIGNED16 Variables |
| 151 | UNSIGNED32 | Read | 2001.12 | ArticleNumber4 32-25        ArticleNumber4 24-17 Artikelnummer des Geräts an Instanz 4 (CU-EHC, EEC, SCB, ...)       Read   UNSIGNED32       2001.12 |
| 153 | UNSIGNED16 | Read |  | DeviceTypeBoard5 16-9       DeviceTypeBoard5 8-1        Gerätetyp an Instanz 5 (CU-EHC, EEC, SCB, ...)                            Read    UNSIGNED16 Variables Internal |
| 154 | UNSIGNED16 | Read |  | SoftwareVersion5 16-9       SoftwareVersion5 8-1        Softwareversion des Geräts an Instanz 5 (CU-EHC, EEC, SCB, ...)           Read    UNSIGNED16 Variables DeviceConfigurationTabl   DeviceConfigurationTableV   Konfigurationstabelle der Version des Geräts an |
| 155 | UNSIGNED16 | Read | 2001.13 | Read    UNSIGNED16       2001.13 eVersion5 16-9            ersion5 8-1                 SCB, ...) Internal |
| 156 | UNSIGNED16 | Read |  | HardwareVersion5 16-9       HardwareVersion5 8-1        Hardwareversion des Geräts an Instanz 5 (CU-EHC, EEC, SCB, ...)           Read    UNSIGNED16 Variables |
| 157 | UNSIGNED32 | Read | 2001.12 | ArticleNumber5 32-25        ArticleNumber5 24-17 Artikelnummer des Geräts an Instanz 5 (CU-EHC, EEC, SCB, ...)       Read   UNSIGNED32       2001.12 |
| 159 | UNSIGNED16 | Read |  | DeviceTypeBoard6 16-9       DeviceTypeBoard6 8-1        Gerätetyp an Instanz 6 (CU-EHC, EEC, SCB, ...)                            Read    UNSIGNED16 Variables Internal |
| 160 | UNSIGNED16 | Read |  | SoftwareVersion6 16-9       SoftwareVersion6 8-1        Softwareversion des Geräts an Instanz 6 (CU-EHC, EEC, SCB, ...)           Read    UNSIGNED16 Variables DeviceConfigurationTabl   DeviceConfigurationTableV   Konfigurationstabelle der Version des Geräts an |
| 161 | UNSIGNED16 | Read | 2001.13 | Read    UNSIGNED16       2001.13 eVersion6 16-9            ersion6 8-1                 SCB, ...) Internal |
| 162 | UNSIGNED16 | Read |  | HardwareVersion6 16-9       HardwareVersion6 8-1        Hardwareversion des Geräts an Instanz 6 (CU-EHC, EEC, SCB, ...)           Read    UNSIGNED16 Variables |
| 163 | UNSIGNED32 | Read | 2001.12 | ArticleNumber6 32-25        ArticleNumber6 24-17 Artikelnummer des Geräts an Instanz 6 (CU-EHC, EEC, SCB, ...)       Read   UNSIGNED32       2001.12 |
| 165 | UNSIGNED16 | Read |  | DeviceTypeBoard7 16-9       DeviceTypeBoard7 8-1        Gerätetyp an Instanz 7 (CU-EHC, EEC, SCB, ...)                            Read    UNSIGNED16 Variables Internal |
| 166 | UNSIGNED16 | Read |  | SoftwareVersion7 16-9       SoftwareVersion7 8-1        Softwareversion des Geräts an Instanz 7 (CU-EHC, EEC, SCB, ...)           Read    UNSIGNED16 Variables DeviceConfigurationTabl   DeviceConfigurationTableV   Konfigurationstabelle der Version des Geräts an |
| 167 | UNSIGNED16 | Read | 2001.13 | Read    UNSIGNED16       2001.13 eVersion7 16-9            ersion7 8-1                 SCB, ...) Internal |
| 168 | UNSIGNED16 | Read |  | HardwareVersion7 16-9       HardwareVersion7 8-1        Hardwareversion des Geräts an Instanz 7 (CU-EHC, EEC, SCB, ...)           Read    UNSIGNED16 Variables |
| 169 | UNSIGNED32 | Read | 2001.12 | ArticleNumber7 32-25        ArticleNumber7 24-17 Artikelnummer des Geräts an Instanz 7 (CU-EHC, EEC, SCB, ...)       Read   UNSIGNED32       2001.12 |
| 171 | UNSIGNED16 | Read |  | DeviceTypeBoard8 16-9       DeviceTypeBoard8 8-1        Gerätetyp an Instanz 8 (CU-EHC, EEC, SCB, ...)                            Read    UNSIGNED16 Variables Internal |
| 172 | UNSIGNED16 | Read |  | SoftwareVersion8 16-9       SoftwareVersion8 8-1        Softwareversion des Geräts an Instanz 8 (CU-EHC, EEC, SCB, ...)           Read    UNSIGNED16 Variables DeviceConfigurationTabl   DeviceConfigurationTableV   Konfigurationstabelle der Version des Geräts an |
| 173 | UNSIGNED16 | Read | 2001.13 | Read    UNSIGNED16       2001.13 eVersion8 16-9            ersion8 8-1                 SCB, ...) Internal |
| 174 | UNSIGNED16 | Read |  | HardwareVersion8 16-9       HardwareVersion8 8-1        Hardwareversion des Geräts an Instanz 8 (CU-EHC, EEC, SCB, ...)           Read    UNSIGNED16 Variables |
| 175 | UNSIGNED32 | Read | 2001.12 | ArticleNumber8 32-25        ArticleNumber8 24-17 Artikelnummer des Geräts an Instanz 8 (CU-EHC, EEC, SCB, ...)       Read   UNSIGNED32       2001.12 |
| 177 | UNSIGNED16 | Read |  | DeviceTypeBoard9 16-9       DeviceTypeBoard9 8-1        Gerätetyp an Instanz 9 (CU-EHC, EEC, SCB, ...)                            Read    UNSIGNED16 Variables Internal |
| 178 | UNSIGNED16 | Read |  | SoftwareVersion9 16-9       SoftwareVersion9 8-1        Softwareversion des Geräts an Instanz 9 (CU-EHC, EEC, SCB, ...)           Read    UNSIGNED16 Variables DeviceConfigurationTabl   DeviceConfigurationTableV   Konfigurationstabelle der Version des Geräts an |
| 179 | UNSIGNED16 | Read | 2001.13 | Read    UNSIGNED16       2001.13 eVersion9 16-9            ersion9 8-1                 SCB, ...) Internal |
| 180 | UNSIGNED16 | Read |  | HardwareVersion9 16-9       HardwareVersion9 8-1        Hardwareversion des Geräts an Instanz 9 (CU-EHC, EEC, SCB, ...)           Read    UNSIGNED16 Variables |
| 181 | UNSIGNED32 | Read | 2001.12 | ArticleNumber9 32-25        ArticleNumber9 24-17 Artikelnummer des Geräts an Instanz 9 (CU-EHC, EEC, SCB, ...)       Read   UNSIGNED32       2001.12 |
| 183 | UNSIGNED16 | Read |  | DeviceTypeBoard10 16-9 DeviceTypeBoard10 8-1            Gerätetyp an Instanz 10 (CU-EHC, EEC, SCB, ...)                            Read    UNSIGNED16 Variables Internal |
| 184 | UNSIGNED16 | Read |  | SoftwareVersion10 16-9      SoftwareVersion10 8-1       Softwareversion des Geräts an Instanz 10 (CU-EHC, EEC, SCB, ...)           Read    UNSIGNED16 Variables DeviceConfigurationTabl   DeviceConfigurationTableV   Konfigurationstabelle der Version des Geräts a |
| 185 | UNSIGNED16 | Read | 2001.13 | Read    UNSIGNED16       2001.13 eVersion10 16-9           ersion10 8-1                SCB, ...) Internal |
| 186 | UNSIGNED16 | Read |  | HardwareVersion10 16-9 HardwareVersion10 8-1            Hardwareversion des Geräts an Instanz 10 (CU-EHC, EEC, SCB, ...)           Read    UNSIGNED16 Variables |
| 187 | UNSIGNED32 | Read | 2001.12 | ArticleNumber10 32-25       ArticleNumber10 24-17 Artikelnummer des Geräts an Instanz 10 (CU-EHC, EEC, SCB, ...)       Read   UNSIGNED32       2001.12 |
| 189 | UNSIGNED8 | Read |  | NumberOfZones               Anzahl der auf dem Gerät vorhandenen Kreise                                Read    UNSIGNED8 |
| 190 | UNSIGNED8 | Read |  | NumberOfZonesDisabled       Anzahl der auf dem Gerät deaktivierten Kreise                              Read    UNSIGNED8 |
| 191 | UNSIGNED8 | Read |  | NumberOfZonesCH             Anzahl der auf dem Gerät vorhandenen Heizkreise                            Read    UNSIGNED8 |
| 192 | UNSIGNED8 | Read |  | NumberOfZonesCHCooling      Anzahl der auf dem Gerät vorhandenen Heiz-/Kühlkreise                      Read    UNSIGNED8 |
| 193 | UNSIGNED8 | Read |  | NumberOfZonesDHW            Anzahl der auf dem Gerät vorhandenen TWW-Kreise                            Read    UNSIGNED8 NumberOfZonesProcessHe |
| 194 | UNSIGNED8 | Read |  | Anzahl der auf dem Gerät vorhandenen Prozesswärme-Kreise                   Read    UNSIGNED8 at                                                                                                                             Internal NumberOfZonesSwimming           |
| 195 | UNSIGNED8 | Read |  | Anzahl der auf dem Gerät vorhandenen Schwimmbad-Kreise                     Read    UNSIGNED8 Pool |
| 196 | UNSIGNED8 | Read |  | NumberOfZonesOthers         Anzahl der auf dem Gerät vorhandenen sonstigen Kreise (Zeitprogramm)       Read    UNSIGNED8 |
| 256 | UNSIGNED8 | Write |  | -              PowerSetpoint                                                                                                     UNSIGNED8       PDO mapping Heizanforderung                                                     Write An das CU-Gerät zu sendender  |
| 257 | INTEGER16 | Write |  | TemperatureSetpoint 16-9   TemperatureSetpoint 8-1                                                                                           INTEGER16       PDO mapping Heizanforderung                                                     Write Read/ |
| 272 | UNSIGNED8 | Read |  | PowerActualReceivedsss                                                                                   Read     UNSIGNED8       PDO mapping den verbundenen Kesseln empfangen wird) FlowTemperatureReceived |
| 273 | INTEGER16 | Read |  | FlowTemperatureReceived 8-1          Vorlauftemperatur des Geräts                                        Read     INTEGER16       PDO mapping 16-9 ReturnTemperatureReceiv |
| 274 | INTEGER16 | Read |  | ReturnTemperatureReceived 8-1        Rücklauftemperatur des Geräts                                       Read     INTEGER16       PDO mapping ed 16-9 |
| 275 | UNSIGNED8 | Read |  | -                                                                                                                       Read     UNSIGNED8       PDO mapping ved |
| 277 | UNSIGNED16 | Read |  | Appliance Error 16-9         Appliance Error 8-1               Aktueller Fehler Gerät (0xFFFFFF bedeutet kein Fehler)       Read   UNSIGNED16   PDO mapping Priorität Gerätefehler 0: Verriegelung |
| 279 | UNSIGNED16 | Read |  | -                            Appliance status 1                                                                             Read   UNSIGNED16   PDO mapping b4: varTWWElektrZusatzerzEin b5: varWartungGerätErforderlich b6: varLeistungGerätNiedrigResetErforderlic |
| 280 | UNSIGNED16 | Read |  | -                            Appliance status 2                b3: var3WegeVentilGeschlossen                                Read   UNSIGNED16   PDO mapping b4: VarGerätTWWAktiv b5: VarGerätHzgAktiv b6: varGerätKühlenAktiv |
| 384 | INTEGER16 | Read |  | varApTOutside 16-9          varApTOutside 8-1                   Außentemperaturmessung                              Read        INTEGER16       501E.0 Jahreszeitbedingter Modus aktiv 0: Winter |
| 386 | UNSIGNED16 | Write |  | parApSummerWinter 16 -9        parApSummerWinter 8 -1                                                                              UNSIGNED16      303A.0 bedeutet deaktiviert)                               Write Nur verwendet, wenn der Generator die Kühlung pa |
| 388 | INTEGER16 | Write | 3041.0 | parApFrostMinToutside 16 -9     parApFrostMinToutside 8 -1                                                                          INTEGER16       3041.0 aktiviert wird                                      Write Die Heizung wird gestoppt. Warmwasser wird aufr |
| 400 | INTEGER16 | Read | 5013.0 | varApTflow 16 -9          varApTflow 8 -1                     Vorlauftemperatur                                   Read        INTEGER16       5013.0 |
| 401 | INTEGER16 | Read | 5015.0 | varApTreturn 16 -9         varApTreturn 8 -1                   Rücklauftemperatur                                  Read        INTEGER16       5015.0 |
| 402 | INTEGER16 | Read | 5027.0 | varApFlueGasTemperature 16 -9    varApFlueGasTemperature 8 -1        Abgastemperatur                                     Read        INTEGER16       5027.0 |
| 403 | INTEGER16 | Read | 4301.0 | varHpHeatPumpTF 16 -9         varHpHeatPumpTF 8 -1                Vorlauftemperatur Wärmepumpe                        Read        INTEGER16       4301.0 |
| 404 | INTEGER16 | Read | 4302.0 | varHpHeatPumpTR 16 -9         varHpHeatPumpTR 8 -1                Rücklauftemperatur Wärmepumpe                       Read        INTEGER16       4302.0 |
| 405 | UNSIGNED16 | Read |  | varApInternalSetpoint 16 -9    varApInternalSetpoint 8 -1          Interner Sollwert für die Trinkwarmwasserbereitung Read         UNSIGNED16      50A9.0 |
| 406 | UNSIGNED16 | Read | 5302.0 | varChSetpoint 16 -9         varChSetpoint 8 -1                  Heizungssollwert der Anlage                         Read        UNSIGNED16      5302.0 |
| 407 | UNSIGNED16 | Read | 4321.0 | varHpCoolingSetpoint 16 -9     varHpCoolingSetpoint 8 -1           Vorlauftemperatur-Sollwert im Kühlmodus             Read        UNSIGNED16      4321.0 21 |
| 408 | UNSIGNED16 | Read | 5604.0 | varDhwFlowTempSetpoint 16 -9   varDhwFlowTempSetpoint 8 -1                                                          Read   UNSIGNED16   5604.0 Trinkwarmwasserbereitung |
| 409 | UNSIGNED8 | Read | 5016.0 | varApWaterPressure                   Aktueller Wasserdruck                           Read   UNSIGNED8    5016.0 |
| 410 | UNSIGNED16 | Read | 5083.0 | varApFlowmeter 16 -9       varApFlowmeter 8 -1                  Durchfluss                                      Read   UNSIGNED16   5083.0 |
| 413 | UNSIGNED16 | Read |  | varApPowerActual 16 -9      varApPowerActual 8 -1                Tatsächlich erzeugte relative Leistung          Read   UNSIGNED16   501B.0 |
| 414 | UNSIGNED16 | Read | 4215.0 | varHePowerSetpoint 16 -9     varHePowerSetpoint 8 -1              Leistungssollwert in % von Max.                 Read   UNSIGNED16   4215.0 |
| 415 | UNSIGNED8 | Read | 4212.0 | varHeIonisationCurrent               Tatsächlich gemessener Flammenstrom             Read   UNSIGNED8    4212.0 varProducerInternalHeatDemand Byte |
| 419 | UNSIGNED32 | Read |  | varChCtrBurnerStarts 32-25        varChCtrBurnerStarts 24-17           Zähler Brennerstarts                            Read   UNSIGNED32 530B.0 |
| 420 | UNSIGNED32 | Read |  | varChCtrBurnerStarts 16-9         varChCtrBurnerStarts 8-1             Zähler Brennerstarts                            Read   UNSIGNED32 |
| 421 | UNSIGNED32 | Read |  | varChCtrBurnHours 32-25           varChCtrBurnHours 24-17              Zähler Brennerstunden                           Read   UNSIGNED32 530C.0 |
| 422 | UNSIGNED32 | Read |  | varChCtrBurnHours 16-9            varChCtrBurnHours 8-1                Zähler Brennerstunden                           Read   UNSIGNED32 |
| 423 | UNSIGNED32 | Read |  | varApCtrBackup1Starts 32-25       varApCtrBackup1Starts 24-17          Zähler Starts Zusatzerzeuger 1                  Read   UNSIGNED32 50B1.0 |
| 424 | UNSIGNED32 | Read |  | varApCtrBackup1Starts 16-9        varApCtrBackup1Starts 8-1            Zähler Starts Zusatzerzeuger 1                  Read   UNSIGNED32 |
| 425 | UNSIGNED32 | Read |  | varApCtrBackup1Hours 32-25        varApCtrBackup1Hours 24-17           Zähler Stunden Zusatzerzeuger 1                 Read   UNSIGNED32 50AF.0 |
| 426 | UNSIGNED32 | Read |  | varApCtrBackup1Hours 16-9         varApCtrBackup1Hours 8-1             Zähler Stunden Zusatzerzeuger 1                 Read   UNSIGNED32 |
| 427 | UNSIGNED32 | Read |  | varApCtrBackup2Starts 32-25       varApCtrBackup2Starts 24-17          Zähler Starts Zusatzerzeuger 2                  Read   UNSIGNED32 50B2.0 |
| 428 | UNSIGNED32 | Read |  | varApCtrBackup2Starts 16-9        varApCtrBackup2Starts 8-1            Zähler Starts Zusatzerzeuger 2                  Read   UNSIGNED32 |
| 429 | UNSIGNED32 | Read |  | varApCtrBackup2Hours 32-25        varApCtrBackup2Hours 24-17           Zähler Stunden Zusatzerzeuger 2                 Read   UNSIGNED32 50B0.0 |
| 430 | UNSIGNED32 | Read |  | varApCtrBackup2Hours 16-9         varApCtrBackup2Hours 8-1             Zähler Stunden Zusatzerzeuger 2                 Read   UNSIGNED32 |
| 431 | UNSIGNED32 | Read | 5000.0 | varApCtrHoursTotal16-9            varApCtrHoursTotal 8-1               Betriebsstundenzahl                             Read   UNSIGNED32 5000.0 |
| 432 | UNSIGNED32 | Read |  | varApCtrHoursTotal16-9            varApCtrHoursTotal 8-1               Betriebsstundenzahl                             Read   UNSIGNED32 |
| 433 | UNSIGNED32 | Read | 5044.0 | varApChEnergyConsumption 32-25 varApChEnergyConsumption 24-17          NGesamtenergieverbrauch für Heizung             Read   UNSIGNED32   5044.0 22 |
| 434 | UNSIGNED32 | Read |  | varApChEnergyConsumption 16-9   varApChEnergyConsumption 8-1         Gesamtenergieverbrauch für Heizung                    Read        UNSIGNED32 varApDhwEnergyConsumption 32-                                        Gesamtenergieverbrauch für die |
| 435 | UNSIGNED32 | Read | 5045.0 | varApDhwEnergyConsumption 24-17                                                            Read        UNSIGNED32   5045.0 |
| 436 | UNSIGNED32 | Read |  | varApDhwEnergyConsumption 8-1                                                              Read        UNSIGNED32 |
| 437 | UNSIGNED32 | Read | 5046.0 | varApCoolingEnergyConsumption 24-17 Gesamtenergieverbrauch für die Kühlung                 Read        UNSIGNED32   5046.0 32-25 varApCoolingEnergyConsumption |
| 438 | UNSIGNED32 | Read |  | varApCoolingEnergyConsumption 8-1    Gesamtenergieverbrauch für die Kühlung                Read        UNSIGNED32 16-9 reserviert für die Zukunft 439-499 |
| 514 | UNSIGNED16 | Read | 5040.0 | varApCtrServiceBurningHours 8-1                                                                    Read     UNSIGNED16      5040.0 16-9                                                              in Betrieb war varApCtrServiceOperatingHou |
| 515 | UNSIGNED16 | Read | 5041.0 | varApCtrServiceOperatingHours 8-1    Anzahl der Stunden seit der letzten Wartung des Gerätes       Read     UNSIGNED16      5041.0 rs 16-9 varApCtrServiceBurnerStarts |
| 516 | UNSIGNED32 | Read | 5042.0 | varApCtrServiceBurnerStarts 24-17    Anzahl erfolgreicher Verdichterstarts nach der Wartung        Read     UNSIGNED32 32-25 5042.0 varApCtrServiceBurnerStarts |
| 517 | UNSIGNED32 | Read |  | varApCtrServiceBurnerStarts 8-1      Anzahl erfolgreicher Verdichterstarts nach der Wartung        Read     UNSIGNED32 16-9 518-530                                                                          reserved for futur Internal |
| 532 | UNSIGNED16 | Read | 1003.1 | varACurrentError1 16-9        varACurrentError1 8-1                Code Fehler des Geräts an Instanz 1(CU-EHC, EEC, SCB, ...)    Read     UNSIGNED16      1003.1 Fehlerstufe des Fehlers am Gerät an Instanz 1 0: Verriegelung |
| 534 | UNSIGNED16 | Read | 1003.1 | varACurrentError3 16-9        varACurrentError2 8-1                Code Fehler des Geräts an Instanz 2 (CU-EHC, EEC, SCB, ...)   Read     UNSIGNED16      1003.1 Fehlerstufe des Fehlers am Gerät an Instanz 2 0: Verriegelung |
| 536 | UNSIGNED16 | Read | 1003.1 | varACurrentError3 16-9        varACurrentError3 8-1                Code Fehler des Geräts an Instanz 3 (CU-EHC, EEC, SCB, ...)   Read     UNSIGNED16      1003.1 |
| 538 | UNSIGNED16 | Read | 1003.1 | varACurrentError4 16-9   varACurrentError4 8-1   Code Fehler des Geräts an Instanz 4 (CU-EHC, EEC, SCB, ...)   Read   UNSIGNED16   1003.1 Fehlerstufe des Fehlers am Gerät an Instanz 4 0: Verriegelung |
| 645 | UNSIGNED16 | Read |  | DeviceType 16-9                   DeviceType 8-1                         der sich der Kreis         Read    UNSIGNED16      InternalVariable   InternalVariable befindet Geräteinstanz, zu der der |
| 648 | UNSIGNED16 | Read |  | parZoneTFlowSetpoint 16-9                parZoneTFlowSetpoint 8-1                Kreis, wenn Außenfühler      Read/Write UNSIGNED16   3402.n   Not Available fehlt Modus arbeitende Zone |
| 650 | UNSIGNED16 | Read |  | parZoneRoomUserActivitySetpoint1 16-9    parZoneRoomUserActivitySetpoint1 8-1                                 Read/Write UNSIGNED16   340C.n   Not Available Benutzeraktivität je Kreis Temperatursollwert der |
| 651 | UNSIGNED16 | Read |  | parZoneRoomUserActivitySetpoint2 16-9    parZoneRoomUserActivitySetpoint2 8-1                                 Read/Write UNSIGNED16   340C.n   Not Available Benutzeraktivität je Kreis Temperatursollwert der |
| 652 | UNSIGNED16 | Read |  | parZoneRoomUserActivitySetpoint3 16-9    parZoneRoomUserActivitySetpoint3 8-1                                 Read/Write UNSIGNED16   340C.n   Not Available Benutzeraktivität je Kreis Temperatursollwert der |
| 653 | UNSIGNED16 | Read |  | parZoneRoomUserActivitySetpoint4 16-9    parZoneRoomUserActivitySetpoint4 8-1                                 Read/Write UNSIGNED16   340C.n   Not Available Benutzeraktivität je Kreis Temperatursollwert der |
| 654 | UNSIGNED16 | Read |  | parZoneRoomUserActivitySetpoint5 16-9    parZoneRoomUserActivitySetpoint5 8-1                                 Read/Write UNSIGNED16   340C.n   Not Available Benutzeraktivität je Kreis Raumsollwert zur Umschaltung von |
| 655 | UNSIGNED16 | Read |  | parZoneAmbiantNightSetpoint 16-9         parZoneAmbiantNightSetpoint 8-1                                      Read/Write UNSIGNED16   340B.n   Not Available Komfort auf Reduziert im Heizbetrieb Raumtemperatursollwert |
| 656 | UNSIGNED16 | Read |  | parZoneRoomCoolingSetpoint1 16-9         parZoneRoomCoolingSetpoint1 8-1         der Benutzeraktivität je     Read/Write UNSIGNED16   3412.n   Not Available Kreis im Kühlbetrieb Raumtemperatursollwert |
| 657 | UNSIGNED16 | Read |  | parZoneRoomCoolingSetpoint2 16-9         parZoneRoomCoolingSetpoint2 8-1         der Benutzeraktivität je     Read/Write UNSIGNED16   3412.n   Not Available Kreis im Kühlbetrieb Raumtemperatursollwert |
| 658 | UNSIGNED16 | Read |  | parZoneRoomCoolingSetpoint3 16-9         parZoneRoomCoolingSetpoint3 8-1         der Benutzeraktivität je     Read/Write UNSIGNED16   3412.n   Not Available Kreis im Kühlbetrieb Raumtemperatursollwert |
| 659 | UNSIGNED16 | Read |  | parZoneRoomCoolingSetpoint4 16-9         parZoneRoomCoolingSetpoint4 8-1         der Benutzeraktivität je     Read/Write UNSIGNED16   3412.n   Not Available Kreis im Kühlbetrieb Raumtemperatursollwert |
| 660 | UNSIGNED16 | Read |  | parZoneRoomCoolingSetpoint5 16-9         parZoneRoomCoolingSetpoint5 8-1         der Benutzeraktivität je     Read/Write UNSIGNED16   3412.n   Not Available Kreis im Kühlbetrieb Raumsollwert zur Umschaltung von |
| 661 | UNSIGNED16 | Read |  | parZoneAmbiantCoolingNightSetpoint 16-9 parZoneAmbiantCoolingNightSetpoint 8-1                                Read/Write UNSIGNED16   3460.n   Not Available Komfort auf Reduziert im Heizbetrieb 29 |
| 662 | UNSIGNED16 | Read |  | parZoneAmbiantHolidaySetpoint 16-9    parZoneAmbiantHolidaySetpoint 8-1        Raumtemperatur des          Read/Write UNSIGNED16   340A.n   Not Available Kreises in der Ferienzeit Vorrübergehender |
| 663 | UNSIGNED16 | Read |  | parZoneTemporaryRoomSetpoint 16-9     parZoneTemporaryRoomSetpoint 8-1                                     Read/Write UNSIGNED16   3451.n   Not Available Raumsollwert je Kreis Manuell eingestellter gewünschter |
| 664 | UNSIGNED16 | Read |  | parZoneRoomManualSetpoint 16-9        parZoneRoomManualSetpoint 8-1                                        Read/Write UNSIGNED16   3413.n   Not Available Raumtemperatur- Sollwert des Kreises |
| 665 | UNSIGNED16 | Read |  | parZoneDhwComfortSetpoint 16-9        parZoneDhwComfortSetpoint 8-1            Gewünschte Komfort-         Read/Write UNSIGNED16   3425.n      3654.n Warmwassertemperatur |
| 666 | UNSIGNED16 | Read |  | parZoneDhwReducedSetpoint 16-9        parZoneDhwReducedSetpoint 8-1            Gewünschte reduzierte       Read/Write UNSIGNED16   3426.n      3655.n Warmwassertemperatur |
| 667 | UNSIGNED16 | Read |  | parZoneDhwHolidaySetpoint 16-9        parZoneDhwHolidaySetpoint 8-1            Gewünschte Ferien-          Read/Write UNSIGNED16   3427.n      3675.n Warmwassertemperatur |
| 668 | UNSIGNED16 | Read |  | parZoneDhwAntilegionelSetpoint 16-9   parZoneDhwAntilegionelSetpoint 8-1                                   Read/Write UNSIGNED16   3428.n      365D.n Antilegionellen-Sollwert für Kreis Speicher Erforderlicher |
| 669 | UNSIGNED16 | Read |  | parZoneSwimmingPoolSetpoint 16 -9     parZoneSwimmingPoolSetpoint 8 -1         Schwimmbad-                 Read/Write UNSIGNED16   3454.n   Not Available Temperatursollwert Sollwert während |
| 670 | UNSIGNED16 | Read |  | parZoneProcessHeatSetpoint 16 -9      parZoneProcessHeatSetpoint 8 -1          "Prozesswärme"-             Read/Write UNSIGNED16   345B.n      3654.n Heizanforderung Verwenden Sie die Raumregelung und/oder |
| 672 | UNSIGNED16 | Read |  | parZoneTFlowSetpointMax 16-9          parZoneTFlowSetpointMax 8-1                                          Read/Write UNSIGNED16   3401.n      362F.0 Sollwert des Kreises 30 |
| 673 | UNSIGNED16 | Read |  | parZoneTFlowCoolingMixingSetpoint 16-9   parZoneTFlowCoolingMixingSetpoint 8-1   Vorlauftemperatur-            Read/Write UNSIGNED16   341A.n   Not Available Sollwert beim Kühlen Steigung der |
| 674 | UNSIGNED8 | Read |  | parZoneSlope                                                          Read/Write UNSIGNED8    3416.n   Not Available Heizkennlinie des Kreises Grundtemperatur der |
| 675 | UNSIGNED16 | Read |  | parZoneHCZPD 16-9                        parZoneHCZPD 8-1                        Heizkennlinie im              Read/Write UNSIGNED16   3414.n   Not Available Komfortbetrieb Grundtemperatur der |
| 676 | UNSIGNED16 | Read |  | parZoneHCZPN 16-9                        parZoneHCZPN 8-1                                                      Read/Write UNSIGNED16   3415.n   Not Available Heizkennlinie im reduzierten Betrieb |
| 677 | UNSIGNED16 | Read |  | parZoneMaxPreHeatTime 16-9               parZoneMaxPreHeatTime 8-1                                             Read/Write UNSIGNED16   346C.n   Not Available Max. Vorheizzeit Umschaltung zwischen berechnetem Sollwert |
| 678 | UNSIGNED16 | Read |  | parZoneMixingValveShift 16-9             parZoneMixingValveShift 8-1                                           Read/Write UNSIGNED16   3409.n   Not Available Verbrauchermanager für den Mischerkreis gesendet wird |
| 679 | UNSIGNED16 | Read |  | parZoneMixingValveBandwith 16-9          parZoneMixingValveBandwith 8-1          stattfindet: Wenn der         Read/Write UNSIGNED16   3405.n   Not Available Kreis kein Mischventil hat, wird der Parameter für diesen Kreis ignoriert. |
| 680 | UNSIGNED16 | Read | 3606.0 | parZoneDhwHysterisis 16-9                parZoneDhwHysterisis 8-1                                              Read/Write UNSIGNED16   342C.n      3606.0 Speicherladung Verschiebung TWW- |
| 681 | UNSIGNED16 | Read | 3622.0 | parZoneDhwCalorifierOffset 16-9          parZoneDhwCalorifierOffset 8-1                                        Read/Write UNSIGNED16   3467.n      3622.0 Bereiter Vorlauftemperatur- Sollwert über die |
| 682 | UNSIGNED16 | Read | 3605.0 | parZoneDhwCalorifierSetpointRaise 16-9   parZoneDhwCalorifierSetpointRaise 8-1                                 Read/Write UNSIGNED16   3468.n      3605.0 Speichertemperatur Delta T erhöhen, um den Speicher zu erwärmen |
| 683 | UNSIGNED16 | Read |  | parZoneProcessHeatHysterisis 16-9           parZoneProcessHeatHysterisis 8-1            Prozesswärme pro Kreis     Read/Write UNSIGNED16     345C.n   Not Available eingeschaltet Hysterese für |
| 684 | UNSIGNED16 | Read |  | parZoneProcessHeatOffset 16-9               parZoneProcessHeatOffset 8-1                Prozesswärme pro Kreis     Read/Write UNSIGNED16     345D.n   Not Available ausgeschaltet Vorlauftemperatur- Sollwert über die |
| 685 | UNSIGNED16 | Read |  | Read/Write UNSIGNED16     3469.n   Not Available 16-9                                      8-1                                         Speichertemperatur Delta T erhöhen, um den Speicher zu erwärmen |
| 686 | UNSIGNED16 | Read |  | parZoneDhwCalorifierHysterisis 16-9         parZoneDhwCalorifierHysterisis 8-1          der                        Read/Write UNSIGNED16     342C.n      3659.n Warmwasserbereitung Verzögerung für Nachlauf |
| 687 | UNSIGNED8 | Read | 3614.0 | parZonePumpPostRun                                                     Read/Write UNSIGNED8      3408.n      3614.0 der Pumpe des Kreises Vom Benutzer gewähltes Zeitprogramm |
| 1100 | INTEGER16 | Read |  | varZoneTflow 16-9                      varZoneTflow 8-1                                                          Read      INTEGER16       5405.n      501A.0 die Temperatur des austretenden Trinkwarmwassers. |
| 1101 | UNSIGNED16 | Read | 5604.0 | varZoneTemperatureSetpoint 16 -9       varZoneTemperatureSetpoint 8-1                Vorlauftemperatur-          Read      UNSIGNED16      5408.n      5604.0 Sollwert Aktuell gewünschter |
| 1102 | INTEGER16 | Read |  | varZoneTRoomSetpoint 16 -9             varZoneTRoomSetpoint 8-1                      Raumtemperatur-             Read      INTEGER16       5419.n   Not Available Sollwert |
| 1103 | INTEGER16 | Read |  | varZoneTOutside 16 -9                  varZoneTOutside 8-1                           Kreis-Außentemperatur       Read      INTEGER16       542E.n   Not Available Aktuelle Raumtemperatur |
| 1104 | INTEGER16 | Read |  | varZoneTRoom 16 -9                     varZoneTRoom 8-1                                                      Read       INTEGER16          5404.n   Not Available für den Kreis Raumtemperaturmessung mit hoher Auflösung für |
| 1105 | INTEGER16 | Read |  | varZoneRoomTemperatureMeasured 16 -9   varZoneRoomTemperatureMeasured 8-1            die Regelung der        Read/Write INTEGER16          5434.n   Not Available Raumtemperatur des Kreismoduls Ein/Aus Heizanforderung |
| 1115 | UNSIGNED32 | Read |  | varZoneCtrPumpRunHours 32-25    varZoneCtrPumpRunHours 24-17        denen die Pumpe laufen    Read   UNSIGNED32 muss 541A.n        560D.0 Anzahl der Stunden, in |
| 1116 | UNSIGNED32 | Read |  | varZoneCtrPumpRunHours 16-9     varZoneCtrPumpRunHours 8-1          denen die Pumpe laufen    Read   UNSIGNED32 muss |
| 1117 | UNSIGNED32 | Read |  | varZoneCtrPumpStarts 32-25      varZoneCtrPumpStarts 24-17          Anzahl der Pumpenstarts   Read   UNSIGNED32 541B.n       560A.0 |
| 1118 | UNSIGNED32 | Read |  | varZoneCtrPumpStarts 16-9       varZoneCtrPumpStarts 8-1                                      Read   UNSIGNED32 Anzahl der Pumpenstarts Speichertemperatur Warmwasserspeicher |
| 7101 | INTEGER16 | Read | 5701.0 | varProducerManagerSystemFlowTemperature 16 -9    varProducerManagerSystemFlowTemperature 8 -1                               Read    INTEGER16   5701.0 Kaskade Anzahl der in der |