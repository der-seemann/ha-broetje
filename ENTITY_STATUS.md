# ENTITY_STATUS

Stand: 2026-05-25 02:52 CEST

## Snapshot
- Quelle: Home Assistant State-API auf dem HA-Host via `https://homeassistant.local:8123`
- Gepruefte Broetje-Entities: `399`
- `unknown`: `0`
- `unavailable`: `105`
- `device_not_available`: `8`
- `last_read_status=ok`: `293`
- `last_read_status=sentinel_no_data`: `1`
- `last_read_status=read_error`: `0`
- `last_read_status=incomplete_batch_retry_failed`: `0`
- `last_read_status=invalid_value`: `0`

## Aktueller Reststand
- Es gibt keine Broetje-Entities mehr mit `state=unknown`.
- Es gibt keine Broetje-Entities mehr mit `last_read_status in {read_error, incomplete_batch_retry_failed, invalid_value}`.
- Das einzige verbleibende `last_read_status=sentinel_no_data` ist `sensor.brotje_iwr_gtw_08_boiler_betriebsart_aussengerat`; die Entity liefert bereits korrekt `state=device_not_available` mit Rohwert `["0xFFFF"]`.
- Der breite Restbestand ist jetzt sauber als `unavailable` bzw. `device_not_available` klassifiziert statt als generisches HA-`unknown`.

## Relevante Folgefixes bis zum Endstand
- Nicht-Enum-Sensoren mit `last_read_status=sentinel_no_data` werden in `custom_components/broetje_heating/sensor.py` als `unavailable` exponiert.
- Enum-Sentinels `0xFFFF` und `0x00FF` liefern fuer die betroffenen IWR-/Zonen-Enums jetzt `device_not_available` statt `unknown`.
- Register mit `last_read_status in {read_error, incomplete_batch_retry_failed, invalid_value}` werden fuer Sensoren und Binary-Sensoren als `unavailable` exponiert statt als `unknown`.
- `custom_components/broetje_heating/coordinator.py` und `entity.py` exponieren fuer Diagnosezwecke weiter `last_read_status`, Rohregister und Modbus-Fehlerdetails als Attribute.

## Bewertung
- Phase 5/6 Ziel erreicht: keine Broetje-Entity haengt mehr auf generischem `unknown`.
- Die verbliebenen `unavailable`-/`device_not_available`-Faelle sind jetzt transparent als No-Data-/Nicht-verfuegbar-Zustaende klassifiziert statt als undeutliche Integrationsfehler.
- Offene Folgearbeit liegt aktuell nicht mehr in der Laufzeitbehandlung, sondern nur noch in Git-/Release-/Dokusync.
