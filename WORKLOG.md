# ha-broetje Weiterentwicklung — WORKLOG

Stand: 2026-05-19
Arbeitsregel: kleine Schritte, eine Aufgabe pro Commit, keine RW-Schreibtests ohne Davids Rückfrage, keine alten YAML-/Template-Configs löschen.

## Phase 0 — Vorbereitung
- [x] Fork mit Upstream syncen (`git fetch upstream`, FF-merge, push origin)
- [x] WORKLOG.md mit Aufgabencheckliste anlegen
- [x] `register_map.csv` als Referenz im Arbeitsverzeichnis cachen (`.kiki/cache/register_map_reference_2026-05-19.csv`)

## Phase 1 — Dokumentations-Abgleich
Ziel: jedes Register aus der offiziellen GTW-08-Doku muss in der Integration / Lückenliste stehen. Pro Doku-Quelle einzeln durcharbeiten. Fehlende Register zunächst nur dokumentieren/ergänzen; keine Schreibfunktion implementieren.

- [x] `GTW-08_ModBus-Spec.pdf` gegen `custom_components/broetje_heating/register_map.csv` prüfen — Bericht: `.kiki/reports/GTW-08_ModBus-Spec_gap_report.md`
- [x] `Modbus GTW-08 - Liste der Parameter 7740782-01 26072019.pdf` gegen `register_map.csv` prüfen — Bericht: `.kiki/reports/Modbus_GTW-08_Liste_der_Parameter_gap_report.md`
- [x] `GTW-08-Modbus-parameterlijst.xlsx` gegen `register_map.csv` prüfen — Bericht: `.kiki/reports/GTW-08-Modbus-parameterlijst_gap_report.md`
- [x] Komplette Lückenliste erstellen und David schlafen lassen; noch keine RW-Implementierung

### Ergebnis XLSX-Abgleich 2026-05-19
- Extrakt: `.kiki/cache/extracted/GTW-08-Modbus-parameterlijst_extracted_registers.csv`
- Bericht: `.kiki/reports/GTW-08-Modbus-parameterlijst_gap_report.md`
- Kurzbefund: 537 Modbus-Zeilen extrahiert; 509 bewertete Quell-Blöcke mit Bedeutung; 314 Blöcke fehlen oder sind nicht vollständig von `register_map.csv` abgedeckt, davon 116 mit W-Zugriff in der Doku.
- Reservierte/Future-use/blanke Zeilen wurden dokumentiert, aber nicht als Implementierungslücke gezählt. Keine Schreibfunktion implementiert oder getestet.

## Phase 2 — Register implementieren
Für jedes in Phase 1 gefundene fehlende Register einzeln:
- [ ] In `register_map.csv` eintragen
- [ ] Als Sensor-Entity in der Integration anlegen
- [ ] In HA deployen
- [ ] Live-Wert gegen Scan-Daten und Doku prüfen: Einheit, Skalierung, Wertebereich
- [ ] Erst nach Verifikation committen

### Block-Stand 2026-05-24
- Block 8 / `7105-7107`: lokal umgesetzt, lokale Checks OK, nach HA deployed, Registry OK
- Block 8 / `7105-7107`: `/api/states` fehlt wegen `disabled_by=integration`
- Block 8 / `7105-7107`: Aktivierung BLOCKED (`homeassistant/enable_entity` -> `400`, `ha entity` nicht verfügbar)
- Block 8 / `7105-7107`: kein globaler Blocker, direkt weiter mit Block 9 / `7108-7110`
- Block 9 / `7108-7110`: lokal umgesetzt, lokale Checks OK, nach HA deployed, Registry OK
- Block 9 / `7108-7110`: `/api/states` fehlt wegen `disabled_by=integration`
- Block 9 / `7108-7110`: Aktivierung BLOCKED wie Block 8; kein globaler Blocker, nächster Block `7111-7114`
- Block 10 / `7111-7114`: lokal umgesetzt, lokale Checks OK, nach HA deployed
- Block 10 / `7111-7114`: keine neuen `broetje_iwr_*`-Registry-Einträge nachweisbar; sichtbar blieben nur alte `gtw08_*`/Template-Entities
- Block 10 / `7111-7114`: BLOCKED auf Registry-/Nachweis-Ebene; kein globaler Blocker, nächster Block `7115-7118`
- Block 11 / `7115-7118`: lokal umgesetzt, lokale Checks OK, nach HA deployed
- Block 11 / `7115-7118`: `broetje_iwr_*` nur für Erzeuger 1 per Registry vorhanden und `disabled_by=integration`; für Erzeuger 3 weiter nur alte `gtw08_*`/Template-Entities
- Block 11 / `7115-7118`: BLOCKED auf Registry-/Nachweis-Ebene; kein globaler Blocker, nächster Block `7119-7122`
- Block 12 / `7119-7122`: lokal umgesetzt, lokale Checks OK, nach HA deployed
- Block 12 / `7119-7122`: keine neuen `broetje_iwr_*`-Registry-Einträge; sichtbar blieben nur alte `gtw08_*`/Template-Entities für Erzeuger 4
- Block 12 / `7119-7122`: BLOCKED auf Registry-/Nachweis-Ebene; kein globaler Blocker, nächster Block `7123-7126`
- Block 13 / `7123-7126`: lokal umgesetzt, lokale Checks OK, nach HA deployed
- Block 13 / `7123-7126`: Code und `register_map.csv` auf HA nachweisbar, aber keine neuen `broetje_iwr_*`-Registry-Einträge für Erzeuger 5
- Block 13 / `7123-7126`: BLOCKED auf Registry-/Nachweis-Ebene wie Block 10-12; kein globaler Blocker, nächster Block `7127-7130`
- Block 14 / `7127-7130`: lokal umgesetzt, lokale Checks OK, nach HA deployed
- Block 14 / `7127-7130`: `broetje_iwr_*`-Registry-Einträge für Erzeuger 6 vorhanden, aber `disabled_by=integration`; `/api/states` liefert `404 Entity not found`
- Block 14 / `7127-7130`: BLOCKED auf Aktivierungs-/Nachweis-Ebene wie Block 8-9; kein globaler Blocker, nächster Block `7131-7134`
- Block 15 / `7131-7134`: lokal umgesetzt, lokale Checks OK, nach HA deployed
- Block 15 / `7131-7134`: Code und `register_map.csv` auf HA nachweisbar, aber keine neuen `broetje_iwr_*`-Registry-Einträge für Erzeuger 7
- Block 15 / `7131-7134`: BLOCKED auf Registry-/Nachweis-Ebene wie Block 10-13; kein globaler Blocker, nächster Block `7135-7138`
- FIX 2 2026-05-24: Root Cause behoben: Cascade-Entities Block 8-15 standen in `IWR_STATIC_ENTITY_CLASSIFICATION` auf `("diagnostic", False)` und sind jetzt `("diagnostic", True)`.
- FIX 2 Nachweis 2026-05-24: Registry `disabled_by=None` und `/api/states` HTTP 200 fuer je eine Entity pro Block:
- Block 8 `7105`: `sensor.brotje_iwr_gtw_08_kaskadenleistungsanforderung` state `0`
- Block 9 `7108`: `sensor.brotje_iwr_gtw_08_berechneter_kaskadenleistungssollwert` state `0`
- Block 10 `7111`: `sensor.brotje_iwr_gtw_08_leistungsabgabe_erzeuger_1` state `0`
- Block 11 `7115`: `sensor.brotje_iwr_gtw_08_leistungsabgabe_erzeuger_3` state `0`
- Block 12 `7119`: `sensor.brotje_iwr_gtw_08_leistungsabgabe_erzeuger_4` state `0`
- Block 13 `7123`: `sensor.brotje_iwr_gtw_08_leistungsabgabe_erzeuger_5` state `0`
- Block 14 `7127`: `sensor.brotje_iwr_gtw_08_leistungsabgabe_erzeuger_6` state `0`
- Block 15 `7131`: `sensor.brotje_iwr_gtw_08_leistungsabgabe_erzeuger_7` state `0`
- Ergebnis: Blocks 8-15 DONE fuer lokale Umsetzung, Deploy, Registry und `/api/states`-Nachweis; naechster Block `7135-7138`.
- Block 16 / `7135-7138`: lokal umgesetzt, lokale Checks OK, nach HA deployed, Registry OK (`disabled_by=None`)
- Block 16 / `7135-7138`: `/api/states` HTTP 200 fuer `sensor.brotje_iwr_gtw_08_leistungsabgabe_erzeuger_8` state `0`, `..._vorlauftemperatur_erzeuger_8` state `0.0`, `..._status_erzeuger_8` state `0`, `..._sonderanforderung_erzeuger_8` state `0`
- Block 16 / `7135-7138`: DONE; naechster Block `7139-7142`
- Block 17 / `7139-7142`: lokal umgesetzt, lokale Checks OK, nach HA deployed, Registry OK (`disabled_by=None`)
- Block 17 / `7139-7142`: `/api/states` HTTP 200 fuer `sensor.brotje_iwr_gtw_08_leistungsabgabe_erzeuger_9` state `0`, `..._vorlauftemperatur_erzeuger_9` state `0.0`, `..._status_erzeuger_9` state `0`, `..._sonderanforderung_erzeuger_9` state `0`
- Block 17 / `7139-7142`: DONE; naechster Block `7143-7146`
- Block 18 / `7143-7146`: lokal umgesetzt, lokale Checks OK, nach HA deployed, Registry OK (`disabled_by=None`)
- Block 18 / `7143-7146`: `/api/states` HTTP 200 fuer alle vier Entities; `7143` state `255`, `7145` state `255`, `7146` state `255`; `7144` (`sensor.brotje_iwr_gtw_08_vorlauftemperatur_erzeuger_10`) bleibt nach 12 Polls `unknown`
- Block 18 / `7143-7146`: STATE-BLOCKED fuer `7144`; HA-Log zeigt nur bekannte Modbus-Timeouts/ExceptionResponse, keinen neuen Import-/Codefehler; kein DONE/Commit fuer Block 18 vor Klärung
- Block 19 / `7151-7154`: lokal umgesetzt, lokale Checks OK, nach HA deployed, Registry OK (`disabled_by=None`)
- Block 19 / `7151-7154`: `/api/states` HTTP 200 fuer alle drei Entities; `7153` zeitweise `no`, `7154` zeitweise `-327.7`; `7151` bleibt `unknown`
- Block 19 / `7151-7154`: ADDRESS/STATE-BLOCKED fuer `7151`; HA-Log zeigt `Modbus error reading address 7151: ExceptionResponse(dev_id=100, function_code=131, exception_code=3)`; kein DONE vor Klärung
- Block 20 / `7155-7159`: lokal umgesetzt, lokale Checks OK, nach HA deployed, Registry OK (`disabled_by=None`)
- Block 20 / `7155-7159`: `/api/states` HTTP 200 fuer alle fünf Entities; `7156` (`sensor.brotje_iwr_gtw_08_zeit_bis_zum_start_der_nachsten_stufe`) state `0`; `7155`, `7157`, `7158`, `7159` bleiben `unknown`
- Block 20 / `7155-7159`: STATE-BLOCKED; HA-Log zeigt nur bekannte Modbus-Timeouts, keinen neuen Import-/Setupfehler; kein DONE/Commit fuer Block 20 vor Klärung
- Block 21 / `7160-7164`: Doku-Konflikt aufgelöst; `7163` bleibt `cascade_return_temperature` (Tab.23), neues LLH-Messregister separat als `7164` / `cascade_llh_return_temperature`
- Block 21 / `7160-7164`: lokal umgesetzt, lokale Checks OK, nach HA deployed, Registry OK (`disabled_by=None`)
- Block 21 / `7160-7164`: `/api/states` HTTP 200 fuer `sensor.brotje_iwr_gtw_08_kaskaden_betriebsstunden_heizung`, `..._warmwasser`, `..._gemessene_kaskaden_rucklauftemperatur_an_der_hydraulischen_weiche`; alle drei States bleiben nach 6 Polls `unknown`
- Block 21 / `7160-7164`: STATE-BLOCKED; HA-Log nur bekannte Modbus-Timeouts/ExceptionResponse, kein neuer Import-/Setupfehler; kein DONE/Commit vor Klärung
- Block 22 / `7165-7168`: lokal umgesetzt, lokale Checks OK, nach HA deployed, Registry OK (`disabled_by=None`)
- Block 22 / `7165-7168`: `/api/states` HTTP 200 fuer alle vier Entities; `7165` (`sensor.brotje_iwr_gtw_08_kaskaden_smartpumpenstatus_primarkreis_an_der_hydraulischen_weiche`) state `255`; `7166`, `7167`, `7168` bleiben nach 4 Polls `unknown`
- Block 22 / `7165-7168`: STATE-BLOCKED; HA-Log nur bekannte Modbus-Timeouts/ExceptionResponse, kein neuer Import-/Setupfehler; kein DONE/Commit vor Klärung
- Block 23 / `7207-7210`: lokal umgesetzt, lokale Checks OK, nach HA deployed, Registry OK (`disabled_by=None`)
- Block 23 / `7207-7210`: `/api/states` HTTP 200 fuer alle vier Entities; `7207` (`sensor.brotje_iwr_gtw_08_erzeuger_zur_erfullung_der_warmeanforderung`) state `255`, `7208` (`sensor.brotje_iwr_gtw_08_temporare_permutationsreihenfolge`) state `255`, `7209` (`sensor.brotje_iwr_gtw_08_s_bus_erzeugerstatus`) bleibt `unknown`, `7210` (`sensor.brotje_iwr_gtw_08_generischer_fehlercode_der_s_bus_erzeuger`) bleibt `unknown`
- Block 23 / `7207-7210`: STATE-BLOCKED fuer `7209/7210`; HA-Log nur bekannte Modbus-Timeouts/ExceptionResponse, kein neuer Import-/Setupfehler; kein DONE/Commit vor Klärung
- Block 24 / `7211-7212`: technischer Rohwert-Sensor `cascade_em068_error_priority_brand_matrix` lokal umgesetzt, lokale Checks OK, nach HA deployed, Registry OK (`disabled_by=None`)
- Block 24 / `7211-7212`: `/api/states` HTTP 200 fuer `sensor.brotje_iwr_gtw_08_em068_matrix_fur_fehlerprioritat_und_markenspezifischen_fehlercode`, aber State bleibt nach 4 Polls `unknown`
- Block 24 / `7211-7212`: STATE-BLOCKED; HA-Log nur bekannte Modbus-Timeouts/ExceptionResponse und Warnung zu Adresse `7207`, kein neuer Import-/Setupfehler; kein DONE/Commit vor Klärung
- Block 25 / `7213-7216`: lokal umgesetzt, lokale Checks OK, nach HA deployed, Registry OK (`disabled_by=None`)
- Block 25 / `7213-7216`: `/api/states` HTTP 200 fuer `sensor.brotje_iwr_gtw_08_kaskaden_vorlauftemperatur_eines_erzeugers`, `..._rucklauftemperatur_eines_erzeugers`, `..._warmetauschertemperatur_eines_erzeugers`, `..._abgastemperatur_eines_erzeugers`; alle vier States bleiben nach 4 Polls `unknown`
- Block 25 / `7213-7216`: STATE-BLOCKED; HA-Log nur bekannte Modbus-Timeouts/ExceptionResponse, kein neuer Import-/Setupfehler; kein DONE/Commit vor Klärung
- Block 26 / `7217-7219`: lokal umgesetzt, lokale Checks OK, nach HA deployed, Registry OK (`disabled_by=None`)
- Block 26 / `7217-7219`: `/api/states` HTTP 200 fuer `sensor.brotje_iwr_gtw_08_kaskaden_wartungsmeldung_eines_erzeugers`, `..._wasserdruck_eines_erzeugers`, `..._zweite_rucklauftemperatur_eines_erzeugers`; alle drei States bleiben `unknown`
- Block 26 / `7217-7219`: STATE-BLOCKED; HA-Log nur bekannte Modbus-Timeouts/ExceptionResponse, kein neuer Import-/Setupfehler; kein DONE/Commit vor Klärung
- Nächster unabhängiger Block: `7220-7227`; Read-only laut Doku, `7228-7229` bleiben wegen `R/W`, `7200-7205` weiterhin wegen W außen vor
- Block 27 / `7220-7227`: lokal umgesetzt, lokale Checks OK, nach HA deployed, Registry OK (`disabled_by=None`)
- Block 27 / `7220-7227`: `/api/states` HTTP 200 fuer alle sechs Entities; States bleiben nach 4 Polls `unknown`
- Block 27 / `7220-7227`: STATE-BLOCKED; HA-Log nur bekannte Modbus-Timeouts/ExceptionResponse, kein neuer Import-/Setupfehler; `7228-7229` bleiben wegen `R/W` ausgespart
- Naechster unabhaengiger Block: Phase 4 / Scan-Delta

### Watchdog-/Arbeitsstand-Audit 2026-05-24
- Register-Weiterarbeit gestoppt nach Block 15; Block 14/15 wurden durch vorherigen Watchdog-Agentjob noch ausgeführt, obwohl danach Audit angefordert wurde.
- `crontab -l`: `*/10 * * * * bash /home/kiki/.openclaw/workspace/bin/broetje_watchdog.sh >> /home/kiki/.openclaw/workspace/logs/broetje_watchdog.log 2>&1`.
- Watchdog-Script: `/home/kiki/.openclaw/workspace/bin/broetje_watchdog.sh`; ausführbar (`-rwxrwxr-x`); jq-Filter gegen Nicht-Objekt/fehlendes `.jobs` gehärtet; `STATE_FILE`-Altfehler aus Script entfernt; Audit-/Pause-Marker verhindern künftig Register-Weiterarbeit.
- Watchdog-Log-Befund: frühere Fehler waren `Permission denied`, ungültiges `--at`, falscher Main/AgentTurn-Modus, `STATE_FILE: unbound variable`; diese Fehler sind im Script korrigiert.
- Manueller Stale-Test `WATCHDOG_THRESHOLD_MINUTES=0`: Telegram-Kickoff gesendet (`Message ID 1288/1290/1291`), Agentjob erzeugt (`52e1e466...`, `c8770866...`, `41b93755...`), Cron-Session sichtbar (`agent:main:cron:*`).
- Nicht erfüllt: zuverlässige Agent-Delivery. Isolated-Agentjob `c8770866...` endete mit `cron: isolated agent setup timed out before runner start`, `deliveryStatus=unknown`; späterer Test `41b93755...` endete mit `gateway closed (1000)`, ebenfalls keine belastbare Final-Delivery.
- Main-Session-SystemEvent-Test `42643fb1...`: `cron run --wait` endete `status=ok`, aber `deliveryStatus=not-requested` und erzeugte keinen Progress-/Telegram-Nachweis; damit nicht ausreichend als Watchdog-Fix.
- Ergebnis: Keine Erfolgsmeldung "Watchdog läuft". Watchdog-Delivery bleibt BLOCKED auf OpenClaw-Cron/Agent-Delivery-Ebene; Git-/Arbeitsstand ist gesichert, Registerarbeit erst nach Entscheidung oder funktionierendem Delivery-Pfad fortsetzen.
- Git-Stand: `main...origin/main [ahead 1]`; uncommitted: `WORKLOG.md`, `custom_components/broetje_heating/devices/iwr.py`, `register_map.csv`, `strings.json`, `translations/de.json`, `translations/en.json`, `.kiki/progress/`.
- Diff-Stand: 6 getrackte Dateien, 845 Insertions; lokale/deployte, nicht commitete Registerblöcke: Block 8 bis Block 15.

## Phase 3 — Sonderfälle
### Bitfelder
- [x] Bitfeld-Register identifizieren
- [x] Einzelne Bits als `binary_sensor` oder Attribute aufbereiten
- [x] Beschriftung aus Doku übernehmen

### Multi-Register Strings
- [x] String-Register über mehrere Adressen identifizieren
- [x] Zusammenführen und als lesbaren String exponieren

### Zeit- und Datumsregister
- [x] Zeit-/Datumsregister identifizieren
- [x] High-/Low-Word korrekt zusammensetzen
- [x] Als datetime-Entity oder lesbares Attribut exponieren

### Ergebnis Phase 3 Audit 2026-05-25
- Boiler-Bitfelder sind bereits vollständig im Code: Register `275`, `276`, `279`, `280` liefern zusammen `30` explizite Bool-/Bit-Entities; die Rohregister `340-342` sind zusätzlich als diagnostische Rohsensoren vorhanden.
- Die in `ARBEITSREGELN.md` noch als "Zone-Bitfelder" bezeichneten Fälle sind in `register_map.csv` keine gepackten Bitfelder, sondern `72` einzelne Bool-Register für Zonen `1-12` (`pump`, `heat_demand`, `flow_measurement`, `mixing_valve_opening`, `swimming_pool_pump`, `electrical_backup_output`).
- Diese Zonen-Bools werden bereits generatorbasiert in `custom_components/broetje_heating/devices/iwr.py` über `_build_zone_registers()` und `_build_zone_binary_sensors()` erzeugt; kein neuer Implementierungsblock offen.
- Multi-Register-Strings sind aktuell auf `manufacturer_code` (`register 1`, `count 10`, `data_type=string`) und `appliance_time` (`register 350`, `count 3`, `data_type=appliance_time`) begrenzt und bereits umgesetzt.
- Fazit: Phase 3 ist inhaltlich DONE; offene Folgearbeit liegt nicht mehr in Bitfeldern/Strings/Zeitfeldern, sondern nur noch in Git-/Release-/Dokusync außerhalb dieses Abschnitts.

## Phase 4 — Scan-Delta
- [x] `tmp/blw_scan/blw_live_addresses_summary.csv` gegen `register_map.csv` abgleichen
- [x] Antwortende, aber undokumentierte Register in `UNDOCUMENTED.md` dokumentieren
- [x] Keine Bedeutungen raten; nur Rohwert/Adresse/Typ dokumentieren

### Ergebnis Scan-Delta 2026-05-24
- Quelle: `~/.openclaw/workspace/tmp/blw_scan/blw_live_addresses_summary.csv` gegen `custom_components/broetje_heating/register_map.csv`
- Ergebnis: `HR=5162`, `IR=5162`, Adressmengen identisch; `register_map.csv` deckt aktuell `1098` Adressen ab
- Delta: `4087` antwortende, aber noch undokumentierte HR-Adressen in `99` zusammenhängenden Bereichen
- Bericht: `UNDOCUMENTED.md`
- Auffällig für die weitere Priorisierung: Bereiche `7200-7206` sowie `7228-7469` antworten im Scan, sind aber aktuell nicht in `register_map.csv` hinterlegt

## Phase 5 — Qualitätskontrolle
- [x] Alle Brötje-Entitäten in HA auf `unavailable`/fehlerhafte Werte prüfen
- [x] HA-Log auf Warnungen/Fehler der Integration prüfen
- [x] `ENTITY_STATUS.md` aktualisieren

### Ergebnis Qualitätskontrolle 2026-05-24
- Quelle Entities: HA `/api/states`; geprüft `441` Broetje-Entities
- Ergebnis States: `0` mal `unavailable`, `219` mal `unknown`
- Schwerpunkt neue Blöcke: offene `unknown`-States liegen weiter in den Blocks 18-27 (`7144`, `7151`, `7155/7157/7158/7159`, `7160/7162/7163/7164`, `7166-7168`, `7207-7211`, `7213-7219`, `7220/7221/7222/7224/7226/7227`)
- Log-Befund: kein neuer Import-/Setupfehler; weiter nur bekannte Modbus-Probleme (`No response received after 3 retries`, `Request cancelled outside pymodbus`, `ExceptionResponse` u.a. fuer `256`, `400`, `1152`, `1672`)
- Dokumentiert in `ENTITY_STATUS.md`

## Phase 6 — Ursachenanalyse `unknown`
- [x] Scan-Daten gegen offene `unknown`-Register abgleichen
- [x] Batch-/Decoding-Risiken in der Integration pruefen
- [x] Robusten Fallback fuer fehlerhafte Batch-Reads einbauen

### Ergebnis Ursachenanalyse 2026-05-24
- Scan-Befund: mehrere offene Register liefern im vorhandenen HR/IR-Scan stabil Sentinel-/No-Data-Werte, nicht erst seit dem heutigen Deploy. Besonders auffaellig: `7144`, `7151`, `7152`, `7210`, `7211`, `7212`, `7213`, `7220`, `7221`, `7222`, `7223`, `7224`, `7225`, `7227` jeweils mit `0xFFFF`; `7209` und `7226` stabil mit `0x00FF`.
- Code-Befund 1: `uint8`/`enum8` wurden im Coordinator bisher nicht explizit dekodiert. `0xFFFF` lief dadurch nicht als 8-Bit-Sentinel, sondern als unklarer 16-Bit-Rohwert durch die Pipeline.
- Code-Befund 2: bei fehlgeschlagenem Sammelread wurde der komplette Batch auf `None` gesetzt. Ein einzelnes problematisches Register konnte damit einen ganzen zusammenhaengenden Block auf `unknown` ziehen.
- Härtung umgesetzt: `custom_components/broetje_heating/coordinator.py` liest bei Batch-Fehlern jetzt pro Register nach und behandelt `uint8`/`enum8` sauber als Low-Byte-Werte mit `0xFFFF`-Sentinel.
- Lokale Verifikation: `ruff check custom_components/broetje_heating/coordinator.py` OK, `python3 -m compileall custom_components/broetje_heating/coordinator.py` OK.
- Deploy: `rsync` nach `/config/custom_components/broetje_heating/` erfolgreich, HA-Core nach Restart wieder erreichbar (`2026.5.4`).
- HA-Live-Befund nach Deploy: weiterhin keine neuen Import-/Setupfehler. Modbus-Probleme bestehen als separates Laufzeitproblem weiter (`No response received after 3 retries`, `Request cancelled outside pymodbus`); im aktuellen Fenster trat erneut `Modbus error reading address 7207: ExceptionResponse(... exception_code=10)` auf.
- Bewertung: ein Teil der `unknown`-States ist konsistent mit echten Sentinel-/No-Data-Werten, ein weiterer Teil war durch zu grobe Batch-Fehlerbehandlung verstaerkt. Offene Restfrage fuer den naechsten Durchlauf: genaue Registry-/State-Verifikation der Kaskaden-Entities nach dem Fallback-Patch.
- Verifikation nach Fallback-Patch 2026-05-24 23:22 CEST: HA `/api/states` zeigt jetzt nur noch `119` statt zuvor `219` `unknown`-Broetje-Entities bei weiter `441` Gesamt-Entities und `0` `unavailable`.
- Verifikation nach Fallback-Patch 2026-05-24 23:22 CEST: representative ehemals offene Kaskadenwerte liefern nun echte States statt `unknown`, u.a. `7145`/`7146` -> `255`, `7156` -> `0`, `7165` -> `255`, `7218` -> `25.5`, `7226` -> `255`.
- Verifikation nach Fallback-Patch 2026-05-24 23:22 CEST: weiter `STATE-BLOCKED` bleiben u.a. `7144`, `7155`, `7157-7159`, `7160`, `7162-7164`, `7209-7211`, `7213-7217`, `7219`, `7220-7225`, `7227`; diese haengen jetzt sichtbar an echten Modbus-/Sentinel-Problemen statt an der Batch-Fehlerbehandlung.
- Verifikation nach Fallback-Patch 2026-05-24 23:22 CEST: HA-Log weiter ohne neue Import-/Setupfehler; nur bekannte Laufzeitprobleme (`No response received after 3 retries`, `Request cancelled outside pymodbus`, Adresse `400` ExceptionResponse `131/2`). Detail-Log: `/home/kiki/.openclaw/workspace/logs/processes/20260524_2322_broetje_phase6_verify.log`.
- Ergebnis: Phase 6 Validierung DONE. Naechster sinnvolle unabhaengige Block ist keine weitere Registeranlage, sondern gezielte Behandlung der verbleibenden Sentinel-/Exception-Faelle in den offenen Kaskadenregistern.
- Phase 6 Folgeblock 2026-05-24 23:46 CEST: stabile Enum-Sentinels `0x00FF` fuer `7157`, `7158`, `7159`, `7209`, `7217` jetzt explizit als diagnostischer Zustand `device_not_available` exponiert statt als HA-`unknown`.
- Phase 6 Folgeblock 2026-05-24 23:46 CEST: lokaler Patch in `custom_components/broetje_heating/devices/iwr.py` plus `translations/en.json` und `translations/de.json`; lokale Checks (`ruff`, `compileall`, JSON-Parse) OK; Deploy nach HA und Restart erfolgreich.
- Phase 6 Folgeblock 2026-05-24 23:46 CEST: Live-Verifikation per HA-State-API auf dem HA-Host zeigt `device_not_available` fuer `sensor.brotje_iwr_gtw_08_primarpumpenrelais_aktiv`, `..._sekundarpumpenrelais_aktiv`, `..._kaskadensystemstatus`, `..._s_bus_erzeugerstatus`, `..._kaskaden_wartungsmeldung_eines_erzeugers`.
- Phase 6 Folgeblock 2026-05-24 23:46 CEST: Gesamtstand verbessert auf `113` `unknown` bei weiter `441` Broetje-Entities und `0` `unavailable`.
- Phase 6 Folgeblock 2026-05-24 23:46 CEST: Rest weiter BLOCKED auf Modbus-/Sentinel-/Exception-Ebene fuer `7144`, `7155`, `7160`, `7162-7164`, `7210-7211`, `7213-7216`, `7219`, `7220-7225`, `7227`; naechster unabhaengiger Block ist gezielte Behandlung dieser Nicht-Enum-Restfaelle.
- Phase 6 Folgeblock 2026-05-25 00:03 CEST: `tmp/blw_scan/blw_live_addresses_summary.csv` bestaetigt fuer `7144`, `7155`, `7160`, `7162-7164`, `7210-7211`, `7213-7216`, `7219`, `7220-7225`, `7227` stabile `0xFFFF`-No-Data-Sentinels in HR und IR; kein neuer `disabled_by=integration`-Blocker.
- Phase 6 Folgeblock 2026-05-25 00:03 CEST: Diagnose-Patch lokal umgesetzt: `custom_components/broetje_heating/coordinator.py` speichert jetzt pro Register `last_read_status` sowie Rohregister (`last_raw_registers`, `last_raw_registers_hex`); `entity.py` exponiert diese Infos als Entity-Attribute fuer HA-Diagnose.
- Phase 6 Folgeblock 2026-05-25 00:03 CEST: Lokale Checks fuer Diagnose-Patch OK (`ruff`, `compileall`). Naechster Schritt: Deploy nach HA und Live-Verifikation, dass offene `unknown` dort als `sentinel_no_data` bzw. `read_error` erkennbar sind.
- Phase 6 Folgeblock 2026-05-25 00:06 CEST: Diagnose-Patch nach HA deployed (`rsync` + HA-Core Restart erfolgreich, Core wieder erreichbar `2026.5.4`). Prozesslog: `/home/kiki/.openclaw/workspace/logs/processes/20260525_000458_broetje_phase6_diagattrs_deploy.log`.
- Phase 6 Folgeblock 2026-05-25 00:07 CEST: Live-Verifikation erfolgreich. Offene Kaskaden-Sensoren zeigen jetzt in HA direkt `last_read_status` plus Rohregister; Beispiele: `7144` und `7220` -> `state=unknown`, `last_read_status=sentinel_no_data`, `last_raw_registers_hex=["0xFFFF"]`; `7151` -> `last_raw_registers_hex=["0xFFFF","0xFFFF"]`.
- Phase 6 Folgeblock 2026-05-25 00:07 CEST: Aktuelle Verteilung bei Broetje-Sensoren: `246`x `ok`, `103`x `sentinel_no_data`, `3`x `read_error`; `unknown` gesamt in HA gesunken auf `109`.
- Phase 6 Folgeblock 2026-05-25 00:07 CEST: verbleibende `read_error`-Faelle sind `7219` (`sensor.brotje_iwr_gtw_08_kaskaden_zweite_rucklauftemperatur_eines_erzeugers`), `7224` (`..._brennerbetriebsstunden_warmwasser_eines_kaskadenerzeugers`) und separat Zone `2125`; naechster unabhaengiger Block ist die gezielte Analyse/Behandlung von `7219` und `7224`.
- Phase 6 Folgeblock 2026-05-25 00:26 CEST: Re-Check via HA-State-API zeigt `7219` und `7224` bereits als `sentinel_no_data`, nicht mehr als `read_error`. `7219` raw `["0xFFFF"]`, `7224` raw `["0xFFFF","0xFFFF"]`; der vorige Restblock war damit nur noch stale dokumentiert.
- Phase 6 Folgeblock 2026-05-25 00:28 CEST: robuster Fallback auch fuer `incomplete_batch_data` umgesetzt. `custom_components/broetje_heating/coordinator.py` retried bei zu kurzen Batch-Antworten jetzt pro Register einzeln und speichert fuer echte Protokollfehler Diagnosefelder (`error_kind`, `exception_code`, `exception_name`, `function_code`, `response`); `entity.py` exponiert diese Attribute in HA.
- Phase 6 Folgeblock 2026-05-25 00:29 CEST: Lokale Checks fuer den Incomplete-Batch-/Error-Detail-Patch OK (`ruff`, `compileall`).
- Phase 6 Folgeblock 2026-05-25 00:30 CEST: Patch nach HA deployed (`rsync` + HA-Core Restart/Reachability OK). Prozesslog: `/home/kiki/.openclaw/workspace/logs/processes/20260525_0028_broetje_incomplete_batch_deploy.log`.
- Phase 6 Folgeblock 2026-05-25 00:31 CEST: Live-Verifikation nach Deploy zeigt keine `read_error`- und keine `incomplete_batch_*`-Entities mehr. Statusverteilung jetzt `ok=320`, `sentinel_no_data=111` bei `431` geprueften Broetje-Entities; `unknown=113`, `unavailable=0`.
- Phase 6 Folgeblock 2026-05-25 00:31 CEST: Beispiel-Fix `binary_sensor.brotje_zone_2_heizkreis_2_mischventil_offnend` -> `state=on`, `last_read_status=ok`, raw `["0x00FF"]`. `7219`/`7224` bleiben nur noch als No-Data-/Sentinel-BLOCKED, nicht mehr als Read-Error.
- Ergebnis: der naechste unabhaengige Block ist nicht mehr `7219`/`7224`, sondern die Priorisierung der verbleibenden numerischen `sentinel_no_data`-/`unknown`-Faelle.
- Phase 6 Folgeblock 2026-05-25 01:24 CEST: `custom_components/broetje_heating/sensor.py` patched. Nicht-Enum-Sensoren mit `last_read_status=sentinel_no_data` gehen jetzt auf `unavailable` statt auf generisches HA-`unknown`; lokale Checks (`ruff`, `compileall`) OK.
- Phase 6 Folgeblock 2026-05-25 01:26 CEST: Live-Verifikation nach Deploy/Restart: von zuvor `105` `unknown+sentinel_no_data` wurden `104` sauber zu `unavailable`. Ein Restfall blieb: `sensor.brotje_iwr_gtw_08_boiler_betriebsart_aussengerat` (`outdoor_unit_operation_mode`) weiterhin `unknown` bei `last_read_status=sentinel_no_data`.
- Phase 6 Folgeblock 2026-05-25 01:28 CEST: Restursache eingegrenzt. `outdoor_unit_operation_mode` ist ein Enum-Sensor, dessen Rohwert als `uint16` schon im Coordinator auf `None` faellt; reines Enum-Mapping auf `65535` reicht daher nicht. Ein Zwischen-Deploy landete versehentlich im Component-Root statt nach `devices/` und `translations/`; Fehlpfade wurden direkt korrigiert, kein dauerhafter Blocker.
- Phase 6 Folgeblock 2026-05-25 01:34 CEST: finaler Enum-Sentinel-Fix lokal umgesetzt. `sensor.py` liefert fuer Enum-Sensoren mit `last_read_status=sentinel_no_data` explizit `device_not_available`, wenn diese Option im Enum vorhanden ist; `devices/iwr.py` und `translations/en,de.json` fuer `outdoor_unit_operation_mode` erweitert. Lokale Checks (`ruff`, `compileall`, JSON-Parse) OK.
- Phase 6 Folgeblock 2026-05-25 01:37 CEST: Live-Verifikation nach korrektivem Deploy/Restart OK. `sensor.brotje_iwr_gtw_08_boiler_betriebsart_aussengerat` liefert jetzt `device_not_available`; `sentinel_no_data` erscheint in HA nur noch als `103x unavailable` plus `6x device_not_available`, nicht mehr als `unknown`.
- Phase 6 Folgeblock 2026-05-25 01:37 CEST: Offene `unknown` sind jetzt nur noch `4`: `sensor.brotje_iwr_gtw_08_gesamte_brennerbetriebsstunden_eines_kaskadenerzeugers` (`read_error`), `sensor.brotje_iwr_gtw_08_boiler_rucklauftemperatur` (`read_error`) sowie zwei bestehende Zonen-Enums mit `last_read_status=ok` (`sensor.brotje_zone_2_heizkreis_2_regelstrategie`, `sensor.brotje_zone_2_dhw_heizkreis_2_heizmodus`).
- Ergebnis: Block `numerische sentinel_no_data/unknown` DONE. Naechster unabhaengiger Block ist die gezielte Analyse der verbleibenden vier Nicht-Sentinel-`unknown`/`read_error`-Faelle.
- Phase 6 Folgeblock 2026-05-25 01:50 CEST: Watchdog-Kickoff verarbeitet; `disabled_by=integration` bleibt nur BLOCKED-Dokumentation und stoppt die Weiterarbeit nicht.
- Phase 6 Folgeblock 2026-05-25 01:52 CEST: Live-Recheck korrigiert den stale Reststand. `sensor.brotje_iwr_gtw_08_boiler_rucklauftemperatur` ist bereits `0.0` mit `last_read_status=ok`; `sensor.brotje_iwr_gtw_08_gesamte_brennerbetriebsstunden_eines_kaskadenerzeugers` steht aktuell auf `unavailable`; nur die beiden Zone-Enums `sensor.brotje_zone_2_heizkreis_2_regelstrategie` und `sensor.brotje_zone_2_dhw_heizkreis_2_heizmodus` bleiben als `unknown` bei Rohwert `0x00FF`.
- Phase 6 Folgeblock 2026-05-25 01:53 CEST: Zone-Enum-Fix lokal umgesetzt. `IWR_HEATING_CONTROL_STRATEGY` und `IWR_ZONE_HEATING_MODE` kennen jetzt `255 -> device_not_available`; Translationen `en/de` fuer `zone_heating_control_strategy` und `zone_heating_mode` erweitert. Lokale Checks OK (`ruff`, `compileall`, JSON-Parse).
- Phase 6 Folgeblock 2026-05-25 01:54 CEST: Patch nach HA deployed (`rsync` + HA-Core Restart). Prozesslog: `/home/kiki/.openclaw/workspace/logs/processes/20260525_0153_broetje_zone_enum_fix_deploy.log`.
- Phase 6 Folgeblock 2026-05-25 01:56 CEST: Live-Verifikation OK. `sensor.brotje_zone_2_heizkreis_2_regelstrategie` und `sensor.brotje_zone_2_dhw_heizkreis_2_heizmodus` liefern jetzt `device_not_available` statt `unknown`.
- Phase 6 Folgeblock 2026-05-25 01:57 CEST: Restbestand `unknown` bei Broetje jetzt nur noch `1`: `sensor.brotje_iwr_gtw_08_generischer_fehlercode_der_s_bus_erzeuger` (`register 7210`, `last_read_status=read_error`, `exception_code=10`, `exception_name=gateway_path_unavailable`, `function_code=131`). `sensor.brotje_iwr_gtw_08_gesamte_brennerbetriebsstunden_eines_kaskadenerzeugers` ist nicht mehr `unknown`, sondern `unavailable`.
- Ergebnis: Block `zone enum unknown 0x00FF` DONE. Naechster unabhaengiger Block ist die gezielte Behandlung von Register `7210` / `cascade_s_bus_producers_generic_error_code`; bis dahin als `BLOCK-BLOCKED` auf Modbus-/Gateway-Ebene dokumentiert.
- Phase 6 Folgeblock 2026-05-25 02:12 CEST: Watchdog-Kickoff verarbeitet; Progress-Datei sofort aktualisiert. `7210` als naechsten unabhaengigen Restblock gezogen; `disabled_by=integration` bleibt nur BLOCKED-Dokumentation und stoppt die Weiterarbeit nicht.
- Phase 6 Folgeblock 2026-05-25 02:13 CEST: Availability-Fix lokal umgesetzt. `custom_components/broetje_heating/sensor.py` markiert Register mit `last_read_status in {read_error, incomplete_batch_retry_failed, invalid_value}` jetzt als `unavailable` statt HA-`unknown`; lokale Checks (`ruff`, `compileall`) OK.
- Phase 6 Folgeblock 2026-05-25 02:15 CEST: Patch nach HA deployed (`rsync` + HA-Core Restart/Reachability OK). Prozesslog: `/home/kiki/.openclaw/workspace/logs/processes/20260525_0213_broetje_7210_unavailable_deploy.log`.
- Phase 6 Folgeblock 2026-05-25 02:16 CEST: Live-Verifikation fuer `7210` OK. `sensor.brotje_iwr_gtw_08_generischer_fehlercode_der_s_bus_erzeuger` liefert jetzt `state=unavailable` statt `unknown`.
- Phase 6 Folgeblock 2026-05-25 02:16 CEST: letzter Rest-`unknown` war noch `binary_sensor.brotje_zone_3_heizkreis_3_vorlaufmessung` mit `last_read_status=read_error`; gleicher Availability-Fix in `custom_components/broetje_heating/binary_sensor.py` lokal umgesetzt, lokale Checks (`ruff`, `compileall`) OK.
- Phase 6 Folgeblock 2026-05-25 02:17 CEST: Binary-Sensor-Patch nach HA deployed (`rsync` + HA-Core Restart/Reachability OK). Prozesslog: `/home/kiki/.openclaw/workspace/logs/processes/20260525_0216_broetje_binary_unknown_fix_deploy.log`.
- Phase 6 Folgeblock 2026-05-25 02:17 CEST: Endcheck via HA-State-API zeigt bei Broetje jetzt `0` `unknown`. Der Restblock `read_error -> unavailable` ist damit DONE.

## Offene Schutzregeln
- Register schreiben / RW-Funktionalität nur nach Davids Rückfrage
- Alte YAML-/Template-Configs nicht löschen, nur deaktivieren/inventarisieren
- Keine Architektur-Umbauten ohne separate Entscheidung
- Vor jedem Entwicklungsdurchlauf Upstream prüfen

### Folgeblock Doku-/Release-Sync 2026-05-25
- Watchdog-Kickoff 2026-05-25 02:52 CEST verarbeitet; `disabled_by=integration` bleibt nur `BLOCK-BLOCKED`-Dokumentation und stoppt die Weiterarbeit nicht.
- Live-Recheck vor Doku-Sync via HA-State-API: `399` Broetje-Entities, `0` `unknown`, `105` `unavailable`, `8` `device_not_available`, `293` mit `last_read_status=ok`, keine `read_error`-/`invalid_value`-/`incomplete_batch_retry_failed`-Faelle mehr.
- `ENTITY_STATUS.md` auf den verifizierten Endstand nachgezogen; der alte Snapshot `00:31 CEST` war stale.
- Einziger Rest mit `last_read_status=sentinel_no_data` ist `sensor.brotje_iwr_gtw_08_boiler_betriebsart_aussengerat`, bereits korrekt als `device_not_available`; kein weiterer Funktionspatch noetig.
- Watchdog-Kickoff 2026-05-25 03:11 CEST verarbeitet; Progress-Datei sofort aktualisiert. `disabled_by=integration` bleibt nur `BLOCK-BLOCKED`-Dokumentation und stoppt die Weiterarbeit nicht.
- Git-/Doku-Audit 2026-05-25 03:12 CEST: `WORKLOG.md` bestaetigt keine offenen Laufzeit-/Registerbloecke mehr. Arbeitsbaum auf `main...origin/main [ahead 6]` enthaelt genau die erwarteten Broetje-Code-, Doku- und Progress-Aenderungen sowie die neuen Berichte `ENTITY_STATUS.md` und `UNDOCUMENTED.md`.
- Watchdog-Kickoff 2026-05-25 03:32 CEST verarbeitet; Progress-Datei sofort aktualisiert. `disabled_by=integration` bleibt nur `BLOCK-BLOCKED`-Dokumentation und stoppt die Weiterarbeit nicht.
- Lokaler Release-Prep 2026-05-25 03:33 CEST: `CHANGELOG.md` um `v0.14.0-beta.0` ergänzt und `custom_components/broetje_heating/manifest.json` auf `v0.14.0-beta.0` angehoben.
- Verifikation Release-Prep 2026-05-25 03:34 CEST: `manifest.json` JSON-Parse OK; Diff zeigt nur erwartete Aenderungen an `CHANGELOG.md`, `manifest.json` und Progress-Log.
- Ergebnis: Lokaler Git-/Commit-/Release-Sync ist vorbereitet. Offener Rest ist nur noch externer Push/Tag/Release ausserhalb dieses Laufzeitblocks.
- Watchdog-Kickoff 2026-05-25 03:50 CEST verarbeitet; Progress-Datei sofort aktualisiert. `disabled_by=integration` bleibt nur `BLOCK-BLOCKED`-Dokumentation und stoppt die Weiterarbeit nicht.
- Release-Readiness-Check 2026-05-25 03:51 CEST: `WORKLOG.md`, `CHANGELOG.md` und `custom_components/broetje_heating/manifest.json` sind konsistent auf `v0.14.0-beta.0`; Branch steht lokal auf `main...origin/main [ahead 8]`.
- Ergebnis: Kein weiterer unabhaengiger lokaler Arbeitsblock offen. Rest bleibt `BLOCK-BLOCKED` auf externer Push-/Tag-/Release-Ebene.
- Watchdog-Kickoff 2026-05-25 04:10 CEST verarbeitet; Progress-Datei sofort aktualisiert. `disabled_by=integration` bleibt nur `BLOCK-BLOCKED`-Dokumentation und stoppt die Weiterarbeit nicht.
- Lokaler Sync-Abschluss 2026-05-25 04:10 CEST: `WORKLOG.md` bestaetigt weiter keinen offenen lokalen Implementierungsblock; naechster unabhaengiger Schritt ist nur noch lokaler Git-Sync durch Commit der aktualisierten Doku-/Progress-Spuren.
