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
- [ ] Bitfeld-Register identifizieren
- [ ] Einzelne Bits als `binary_sensor` oder Attribute aufbereiten
- [ ] Beschriftung aus Doku übernehmen

### Multi-Register Strings
- [ ] String-Register über mehrere Adressen identifizieren
- [ ] Zusammenführen und als lesbaren String exponieren

### Zeit- und Datumsregister
- [ ] Zeit-/Datumsregister identifizieren
- [ ] High-/Low-Word korrekt zusammensetzen
- [ ] Als datetime-Entity oder lesbares Attribut exponieren

## Phase 4 — Scan-Delta
- [ ] `tmp/blw_scan/blw_live_addresses_summary.csv` gegen `register_map.csv` abgleichen
- [ ] Antwortende, aber undokumentierte Register in `UNDOCUMENTED.md` dokumentieren
- [ ] Keine Bedeutungen raten; nur Rohwert/Adresse/Typ dokumentieren

## Phase 5 — Qualitätskontrolle
- [ ] Alle Brötje-Entitäten in HA auf `unavailable`/fehlerhafte Werte prüfen
- [ ] HA-Log auf Warnungen/Fehler der Integration prüfen
- [ ] `ENTITY_STATUS.md` aktualisieren

## Offene Schutzregeln
- Register schreiben / RW-Funktionalität nur nach Davids Rückfrage
- Alte YAML-/Template-Configs nicht löschen, nur deaktivieren/inventarisieren
- Keine Architektur-Umbauten ohne separate Entscheidung
- Vor jedem Entwicklungsdurchlauf Upstream prüfen
