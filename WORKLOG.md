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
- [ ] `Modbus GTW-08 - Liste der Parameter 7740782-01 26072019.pdf` gegen `register_map.csv` prüfen
- [ ] `GTW-08-Modbus-parameterlijst.xlsx` gegen `register_map.csv` prüfen
- [ ] Komplette Lückenliste erstellen und David schlafen lassen; noch keine RW-Implementierung

## Phase 2 — Register implementieren
Für jedes in Phase 1 gefundene fehlende Register einzeln:
- [ ] In `register_map.csv` eintragen
- [ ] Als Sensor-Entity in der Integration anlegen
- [ ] In HA deployen
- [ ] Live-Wert gegen Scan-Daten und Doku prüfen: Einheit, Skalierung, Wertebereich
- [ ] Erst nach Verifikation committen

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
