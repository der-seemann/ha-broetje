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
- Nie mehr als 5 Register auf einmal

## Block-Status
Jeden Block immer mit einem dieser Status protokollieren:

| Status | Bedeutung |
|---|---|
| `TODO` | noch nicht begonnen |
| `IN_PROGRESS` | läuft gerade |
| `BLOCKED` | nicht weiterführbar, Grund dokumentieren |
| `DEPLOYED_UNVERIFIED` | deployed, aber Verifikation fehlt noch |
| `REGISTRY_ONLY` | Entity in Registry, aber disabled_by=integration |
| `TEMP_ENABLED_VERIFIED` | temporär aktiviert und in /api/states geprüft |
| `LIVE_VERIFIED` | war aktiv, direkt in /api/states geprüft |
| `RELEASED` | Commit + Tag + GitHub-Release erstellt |

---

## Definition of Done (harte Anforderung)

Kein Commit, kein Tag, kein Release ohne diese Checks in dieser Reihenfolge:

### 1. Code geändert

### 2. Lokale Checks erfolgreich
```bash
. ~/projects/ha-broetje/.venv/bin/activate
ruff check custom_components/broetje_heating
python -m compileall -q custom_components/broetje_heating
python -m json.tool custom_components/broetje_heating/manifest.json >/dev/null
```
Schlägt einer fehl → Block bleibt `IN_PROGRESS`, kein Deploy.

### 3. Deployment nach HA
```bash
rsync -a ~/projects/ha-broetje/custom_components/broetje_heating/ \
 root@homeassistant.local:/config/custom_components/broetje_heating/
```

### 4. HA-Core-Restart mit Retry
```bash
ssh -i ~/.openclaw/secrets/rpi4_ha_ed25519 root@homeassistant.local 'ha core restart'

for i in $(seq 1 10); do
 if ssh -i ~/.openclaw/secrets/rpi4_ha_ed25519 root@homeassistant.local 'ha core info' 2>/dev/null | grep -q running; then
 echo "HA reachable after attempt $i"
 break
 fi
 echo "HA not reachable, attempt $i/10"
 [ "$i" -eq 10 ] && echo "BLOCKED: HA not reachable after 10 attempts" && exit 1
 sleep 60
done
```
Nach 10 Versuchen → Block als `BLOCKED` markieren, Telegram-Notiz, nächsten Block.

### 5. Manifest-Version auf HA prüfen
```bash
ssh -i ~/.openclaw/secrets/rpi4_ha_ed25519 root@homeassistant.local \
 'grep version /config/custom_components/broetje_heating/manifest.json'
```
Muss mit lokalem manifest.json übereinstimmen.

### 6. Entity-Registry prüfen
Für jede neue Entity:
- `entity_id` korrekt?
- `platform` korrekt?
- `unique_id` plausibel?
- `disabled_by` = leer/null oder `integration`?

### 7. Live-State-Verifikation (abhängig vom Entity-Status)

**A) Entity aktiv (disabled_by = null):**
- Entity muss in `/api/states` erscheinen → Status: `LIVE_VERIFIED`
- State, Attribute und unavailable/unknown dokumentieren

**B) Entity disabled_by=integration:**
- Das ist nur `REGISTRY_ONLY` — kein vollständiger Nachweis
- Entity temporär aktivieren:
 ```
 HA → Einstellungen → Entitäten → Entity aktivieren
 oder per REST API: POST /api/services/homeassistant/enable_entity
 ```
- Integration neu laden oder HA neu starten (mit Retry-Loop)
- `/api/states` prüfen → Status: `TEMP_ENABLED_VERIFIED`
- Optional danach wieder deaktivieren
- Im Protokoll klar unterscheiden: `REGISTRY_ONLY` ≠ `TEMP_ENABLED_VERIFIED`

**Nicht erlaubt:**
> "Entities verifiziert" wenn `disabled_by=integration` und kein `/api/states`-Check.

### 8. HA-Core-Log prüfen
```bash
ssh -i ~/.openclaw/secrets/rpi4_ha_ed25519 root@homeassistant.local \
 'ha core logs' | grep -i "broetje\|traceback\|error\|setup" | tail -30
```
- Keine neuen Tracebacks seit Deployment
- Keine neuen Setup-/Config-Flow-Fehler
- Modbus-Timeouts separat bewerten — nicht mit Codefehlern vermischen

### 9. Commit + Tag + Release
Erst nach erfolgreichem Durchlauf aller obigen Punkte:
```bash
git commit -m "feat: ..."
git push
export GH_TOKEN="$(cat ~/.openclaw/secrets/github_pat_der_seemann.txt)"
gh release create vX.Y.Z-beta.N --prerelease \
 --title "vX.Y.Z-beta.N" \
 --notes-file CHANGELOG.md \
 --repo der-seemann/ha-broetje
```
**Wichtig:** `GH_TOKEN` nie im Klartext in Logs oder Chat — immer aus Datei lesen.

### 10. Fortschritt protokollieren
Pro Block in `.kiki/progress/YYYY-MM-DD_progress.md`:
- Blockname + Register
- geänderte Dateien
- lokale Check-Ergebnisse
- Deploy-Ergebnis
- HA-Version nach Deploy
- Registry-Ergebnis (mit Status-Label)
- State-Ergebnis (mit Status-Label)
- Log-Ergebnis
- Commit/Tag/Release
- offene Punkte oder BLOCKED-Grund

---

## Fehler-Routine

| Fehlerart | Reaktion |
|---|---|
| Tool-/Shell-Fehler | Einmal retry mit atomarem Kommando |
| Weiter Fehler | Block auf 1–2 Register verkleinern, neu versuchen |
| HA nicht erreichbar | Retry-Loop (10×, 60s Pause) |
| Nach 10 Versuchen kein HA | `BLOCKED`, Telegram, nächster Block |
| Modbus-Timeout/ExceptionResponse | Separat dokumentieren, nicht als Code-Fehler werten |
| Lokale Checks fehlgeschlagen | Kein Deploy, Bug fixen, neu prüfen |

**Nie wegen eines Fehlers komplett stoppen** — immer mit dem nächsten unabhängigen Block weitermachen.

Timeout-Vorbeugung:
- Keine langen Shell-Pipes — lieber mehrere einzelne Kommandos
- Kein `set -x` bei Secret-Kommandos
- Kein `GH_TOKEN='ghp_...'` direkt im Kommando — immer `$(cat ...)`

---

## Dev-Umgebung einrichten (einmalig)
```bash
cd ~/projects/ha-broetje
python3 -m venv .venv
. .venv/bin/activate
pip install ruff
```

## Versionierung
- Bugfix / kleine Ergänzung: beta.X+1
- Neuer Feature-Block: minor+1, beta.0 neu starten
- Release immer mit `prerelease: true`

---

## To-Do

### Phase 3 — Bitfelder & UINT32-Paare
- [ ] Boiler-Bitfelder (22 gesamt) → je Bit ein `binary_sensor`
- [ ] Zone-Bitfelder
- [ ] Boiler UINT32/INT32-Paare (30 gesamt) → High+Low zusammensetzen
- [ ] Zone UINT32-Paare

### Phase 4 — Scan-Delta
- [ ] `blw_live_addresses_summary.csv` vs. `register_map.csv` abgleichen
- [ ] Undokumentierte Register → `UNDOCUMENTED.md` (nur dokumentieren, keine Annahmen)
- [ ] Falls Datei fehlt: `BLOCKED` markieren, mit Phase 5 weitermachen

### Phase 5 — QC
- [ ] Alle Entities auf `unavailable`/fehlerhafte Werte prüfen
- [ ] HA-Log auf Integrationswarnungen prüfen
- [ ] `ENTITY_STATUS.md` aktualisieren
- [ ] Finales Release erstellen
