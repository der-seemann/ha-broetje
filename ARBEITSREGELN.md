# Arbeitsregeln ha-broetje

## Grundregeln
- Nur Python in `custom_components/broetje_heating/` — keine YAML-Packages
- `/config/packages/gtw08_*` nicht anfassen
- Kein RW auf Register
- Rückfragen per Telegram sammeln, NICHT warten — weiter mit nächstem Block
- Einmal täglich Zusammenfassung per Telegram

## Pro Block
1. Scan-Check: Register in `blw_live_addresses_summary.csv` vorhanden?
2. Implementieren (Python)
3. `ruff check` + `python -m compileall -q`
4. Versionsnummer: Bugfix → beta.X+1 / neues Feature → minor+1 beta.0
5. `CHANGELOG.md` aktualisieren (Stichpunkte)
6. `commit` + `push` → `gh release create --prerelease` → `rsync` → HA restart
7. Live-Werte prüfen — unplausibel → Telegram, weiter

Block-Größe: 5–15 Register pro Commit.

## Deploy
```
rsync -a ~/projects/ha-broetje/custom_components/broetje_heating/ \
 /config/custom_components/broetje_heating/
ha core restart
```

## Verifikation
Nur per HA REST API (Token aus `~/.openclaw/secrets/homeassistant_token.txt`).
Kein SSH auf homeassistant.local.

---

## To-Do

### Phase 3 — Bitfelder & UINT32-Paare
- [ ] Boiler-Bitfelder (aus QC-Report, 22 gesamt) → je Bit ein `binary_sensor`
- [ ] Zone-Bitfelder
- [ ] Boiler UINT32/INT32-Paare (30 gesamt) → High+Low zusammensetzen
- [ ] Zone UINT32-Paare

### Phase 4 — Scan-Delta
- [ ] `blw_live_addresses_summary.csv` vs. `register_map.csv` abgleichen
- [ ] Undokumentierte Register → `UNDOCUMENTED.md` (nur dokumentieren, keine Annahmen)

### Phase 5 — QC
- [ ] Alle Entities auf `unavailable`/fehlerhafte Werte prüfen
- [ ] HA-Log auf Integrationswarnungen prüfen
- [ ] `ENTITY_STATUS.md` aktualisieren
- [ ] Finales Release erstellen
