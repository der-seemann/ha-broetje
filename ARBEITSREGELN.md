# Arbeitsregeln ha-broetje

## Grundregeln
- Nur Python in `custom_components/broetje_heating/` — keine YAML-Packages
- `/config/packages/gtw08_*` nicht anfassen
- Kein RW auf Register
- Rückfragen per Telegram sammeln, NICHT warten — weiter mit nächstem Block
- Einmal täglich Zusammenfassung per Telegram

## Block-Größe
- Normal: 3–5 Register pro Commit
- Bei Fehlern oder komplexen Typen (Bitfeld, UINT32): 1–2 Register pro Commit
- Nie mehr als 5 Register auf einmal — lieber mehr kleine Commits

## Pro Block
1. Scan-Check: Register in `blw_live_addresses_summary.csv` vorhanden?
2. Implementieren (Python)
3. `ruff check` + `python -m compileall -q`
4. Versionsnummer: Bugfix → beta.X+1 / neues Feature → minor+1 beta.0
5. `CHANGELOG.md` aktualisieren (Stichpunkte)
6. `commit` + `push` → `gh release create --prerelease` → Deploy → HA restart
7. Live-Werte prüfen — unplausibel → Telegram, weiter

## Deploy
```bash
rsync -a ~/projects/ha-broetje/custom_components/broetje_heating/ \
 root@homeassistant.local:/config/custom_components/broetje_heating/
ssh -i ~/.openclaw/secrets/rpi4_ha_ed25519 root@homeassistant.local 'ha core restart'
```

## Verifikation
Per SSH oder HA REST API (Token aus `~/.openclaw/secrets/homeassistant_token.txt`).
SSH-Key: `~/.openclaw/secrets/rpi4_ha_ed25519`

## Fehler-Routine
Bei jedem Fehler (Tool-Fehler, Timeout, Exception):

1. **Einmal retry** — exakt gleiche Aufgabe nochmal versuchen
2. **Immer noch Fehler → Block verkleinern**: Aufgabe auf 1–2 Register reduzieren, neu versuchen
3. **Weiter Fehler → überspringen**: Block als `[SKIP]` in WORKLOG.md markieren, Telegram-Notiz, nächsten Block
4. **Nie wegen eines Fehlers komplett stoppen** — immer mit dem nächsten Block weitermachen

Timeout-Vorbeugung:
- Komplexe Shell-Pipes auf mehrere einzelne Befehle aufteilen
- Kein `set -euo pipefail` in langen Heredocs — lieber einzelne Kommandos
- SSH-Befehle kurz halten, Logik lokal ausführen

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
