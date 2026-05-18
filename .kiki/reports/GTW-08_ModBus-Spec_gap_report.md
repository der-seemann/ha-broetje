# GTW-08_ModBus-Spec.pdf Gap Report

Quelle: `GTW-08_ModBus-Spec.pdf` (pdftotext layout extraction).
Ziel: Abgleich gegen `custom_components/broetje_heating/register_map.csv`.

Heuristik: Zeilen mit führender Registeradresse plus Datentyp (`UINT8`, `INT16`, `ENUM8`, ...). Keine Bedeutungen geraten; unsichere Details bleiben im Excerpt.

- Extrahierte eindeutige Register: 108
- Bereits in register_map.csv vorhanden: 63
- Fehlend in register_map.csv: 45

## Fehlende Register

| Register | Datentyp | Zugriff | Display-Code | Tabelle | Beschreibungsauszug |
|---:|---|---|---|---|---|
| 7000 | UINT8 | R/W |  | Tab.46     Main cascade registers | Numero di nodo del dispositivo       1 Unità                  0 - 255              R/W |
| 7001 | ENUM8 | R/W | NP014 | Tab.46     Main cascade registers | Modalità cascata                     0: Automatico            0-2                  R/W         NP014 1: Riscaldamento 2: Raffrescamento |
| 7002 | ENUM8 | R/W | NP006 | Tab.46     Main cascade registers | Kaskadenfunktion                    0: Kaskade              0-1                   R/W         NP006 1: Parallelbetrieb |
| 7009 | ENUM8 | R/W | NP011 | Tab.46     Main cascade registers | Auswahl der Kaskadenführungs­       0: Temperatur           0-1                   R/W         NP011 strategie: Temperatur /- Leis­      1: Leistung tungsgeführt |
| 7011 | ENUM8 | R/W | NP223 | Tab.46     Main cascade registers | Il tipo di permutazione dell'ordine 0: Periodo fisso          0-1                  R/W         NP223 di avvio                            1: Ore di funziona­ mento |
| 7012 | UINT16 | R/W | NP281 | Tab.46     Main cascade registers | Intervalle de temps avant com­     1 heures               1 - 9999               R/W         NP281 mutation des générateurs |
| 7014 | ENUM8 | R/W | NP225 | Tab.46     Main cascade registers | Strategia di controllo della poten­ 0: Ultima on, prima       0-2                  R/W         NP225 za                                  off 1: Prima on, ultima off 2: Ultima on,ultima off |
| 7015 | UINT8 | R/W | NP227 | Tab.46     Main cascade registers | Generador preferido para la pro­   Unidades 1            0 - 255               L/E         NP227 ducción de calefacción central |
| 7016 | UINT8 | R/W | NP228 | Tab.46     Main cascade registers | Generador no preferido para la     Unidades 1            0 - 255               L/E         NP228 producción de calefacción cen­ tral |
| 7017 | UINT8 | R/W | NP282 | Tab.46     Main cascade registers | Inschakelwaarde voor de ver­       %                      0 - 100             L/S           NP282 traagde activering van de vol­ gende warmteopwekker |
| 7018 | UINT8 | R/W | NP283 | Tab.46     Main cascade registers | Uitschakelwaarde voor de ver­      %                      0 - 100             L/S           NP283 traagde deactivering van de warmteopwekker |
| 7019 | UINT8 | R/W | NP284 | Tab.46     Main cascade registers | Inschakelwaarde vervroegde ac­     %                      0 - 100             L/S           NP284 tivering van volgende warmteop­ wekker |
| 7020 | UINT8 | R/W | NP285 | Tab.46     Main cascade registers | Uitschakelwaarde vervroegde        %                      0 - 100             L/S           NP285 deactivering van de warmteop­ wekker |
| 7023 | ENUM8 | R/W | NP287 | Tab.49     Cascade pump registers | Selección de tipo de    0: Sin bomba               0-3                        L/E          NP287 bomba primaria          1: Activado/desacti­ vado 2: PWM Caldera 3: 0-10 volt |
| 7024 | ENUM8 | R/W | NP288 | Tab.49     Cascade pump registers | Selección de tipo de    0: Sin bomba               0-3                        L/E          NP288 bomba secundaria        1: Activado/desacti­ vado 2: PWM Caldera 3: 0-10 volt |
| 7102 | UINT8 | R | NM028 | Tab.46     Main cascade registers | Cascada Número de generado­                              0 - 255               L           NM028 res presentes reconocidos en la cascada |
| 7103 | UINT8 | R | NM022 | Tab.46     Main cascade registers | Anzahl der Stufen die in der Kas­                           0 - 255               R           NM022 kade verfügbar sind |
| 7104 | UINT8 | R | NM023 | Tab.46     Main cascade registers | Nombre d'allures nécessaires                                  0 - 255      R           NM023 pour satisfaire les besoins de la cascade |
| 7105 | UINT8 |  |  | Tab.46     Main cascade registers | Puissance requise par le ges­  1%                             0 - 100      R tionnaire des consommateurs de la cascade : Puissance |
| 7106 | INT16 |  |  | Tab.46     Main cascade registers | Puissance requise par le ges­  0,01 °C                        -20 - 120    R tionnaire des consommateurs de la cascade : Température |
| 7107 | ENUM8 |  |  | Tab.46     Main cascade registers | Puissance requise par le ges­        0: Automatique                        R tionnaire des consommateurs de       1: Chauffage la cascade : Demande de chauf­       2: Rafraîchissement fe                                   |
| 7108 | UINT8 |  |  | Tab.46     Main cascade registers | Cascata Ponto de definição de       1%                     0 - 100             R Potência do Sistema calculado: Potência |
| 7109 | INT16 |  |  | Tab.46     Main cascade registers | Cascata Ponto de definição de       0,01 °C                -20 - 120           R Potência do Sistema calculado: Temperatura |
| 7110 | ENUM8 |  |  | Tab.46     Main cascade registers | Cascada Consigna de potencia        0: Automático                               L del sistema calculada: Demanda      1: Calefacción de calor                            2: Refrigeración 3: Calor de proceso 4: Secado del  |
| 7151 | UINT32 | R | NM112 | Tab.46     Main cascade registers | Het gevraagde vermogen (kW)         0,1 kW                                        R           NM112 aan het cascadesysteem. |
| 7155 | INT16 | R | NM170 | Tab.46     Main cascade registers | Percentuale di potenza richiesta      0,1%                                         R           NM170 dalla cascata |
| 7157 | ENUM8 | R | NM166 | Tab.46     Main cascade registers | Stato della pompa primaria della      0: Non attivo                                R           NM166 cascata                               1: Attivato |
| 7158 | ENUM8 | R | NM167 | Tab.46     Main cascade registers | Stato della pompa secondaria          0: Non attivo                                R           NM167 della cascata                         1: Attivato |
| 7159 | ENUM8 | R | NM163 | Tab.46     Main cascade registers | Stato della cascata                   Vedere la tabella se­                        R           NM163 guente Tab.267, pa­ gina 137 |
| 7160 | UINT32 | R | NC000 | Tab.46     Main cascade registers | Heures de fonctionnement de la       1 heures                                         R          NC000 cascade utilisées pour le chauf­ fage. |
| 7162 | UINT32 | R | NC001 | Tab.46     Main cascade registers | Heures de cascade utilisées          1 heures                                         R          NC001 pour l'eau chaude sanitaire |
| 7164 | INT16 | R | NM165 | Tab.46     Main cascade registers | Temper. retorno medida en sis­   0,01 °C                     -327,68 - 327,68   L          NM165 tema en cascada en la botella de equilibrio (LLH) del lado secun­ dario |
| 7165 | UINT8 |  |  | Tab.46     Main cascade registers | Cascade, central primary pump      1                         0 - 14             R status - producer circuit of low loss header |
| 7166 | UINT8 |  |  | Tab.46     Main cascade registers | pwm signal after transfer function 0,1%                        0 - 100                R to control pcb-hardware for pump producer circuit |
| 7167 | UINT8 |  |  | Tab.46     Main cascade registers | pwm signal after transfer function 0,1%                        0 - 100                R to control pcb-hardware for pump consumer circuit |
| 7168 | INT16 | R | EM012 | Tab.46     Main cascade registers | Temperatura di mandata della          0,01 °C                -327,68 - 327,68            R         EM012 cascata misurata sul lato secon­ dario del separatore idraulico (LLH) |
| 7200 | UINT8 | R/W | NP231 | Tab.46     Main cascade registers | L'ordine di attivazione dei gene­                            0 - 255                     R/W       NP231 ratori |
| 7201 | UINT8 |  |  | Tab.46     Main cascade registers | Liste des générateurs identifiés                               0 - 255                R/W dans le système en cascade : Numéro |
| 7202 | ENUM8 |  |  | Tab.46     Main cascade registers | Liste des générateurs identifiés     0: non connecté                                  R/W dans le système en cascade :         1: Disponible État                                 2: Non disponible |
| 7203 | UINT16 | R/W | EP001 | Tab.46     Main cascade registers | La potenza minima che il gene­                                                           R/W       EP001 ratore può fornire. potenza bassa |
| 7205 | UINT16 | R/W | EP086 | Tab.46     Main cascade registers | La potenza massima che il gene­                                                          R/W       EP086 ratore è in grado di fornire. Pieno carico |
| 7207 | UINT16 | R | NM113 | Tab.46     Main cascade registers | Elenco dei generatori corrente­                              0 - 255                     R         NM113 mente attivi nell'impianto a ca­ scata |
| 7208 | UINT16 | R | NM171 | Tab.46     Main cascade registers | Temporary poducer activation or­                             0 - 255                     R         NM171 der |
| 7209 | ENUM8 | R | EM058 | Tab.46     Main cascade registers | Stato principale attuale del gene­                           Vedere la tabella se­       R         EM058 ratore.                                                      guente Tab.267, pa­ gina 137 |
| 7228 | UINT32 | R | EM228 | Tab.46     Main cascade registers | Serial number                         1                      0 - 4294967295           R           EM228 Tab.47     Appliance status 7209 Status           Description                   Explanation 0                Standby |

## Bereits abgedeckte Register

| Register | Datentyp | Display-Code | Beschreibungsauszug |
|---:|---|---|---|
| 128 | UINT8 |  | Dispositivi connessi            1 unità                 0 - 16                R È possibile utilizzare la tabella seguente per trovare l'istanza dell'oggetto per il codice di errore del dispositivo specifico. |
| 189 | UINT8 |  | Counter of zone detected                                  0 - 127            R Tab.25     Zone function with display code CP02X and device type Zone        1         2       3         4         5         6          7     |
| 256 | UINT8 |  | Power                                            %                               R/W |
| 257 | UINT16 |  | Temperature                                      0.01 °C                         R/W |
| 258 | ENUM8 |  | Algorithm type                                   Tab.19, page 15                 R/W |
| 259 | ENUM8 |  | Heat demand type                                 Tab.20, page 15                 R/W |
| 272 | UINT8 |  | Actual power system                              1                               R Tab.19       Algorithm type Value        Description 0            Remote management for both temperature and power |
| 275 | UINT8 |  | Bitfield heat demand per      See the following table           0 – 255               R zone; Nbr zone, power set­    Tab.13, page 11 point, temp setpoint and type of heat demand |
| 277 | UINT16 |  | Lista de errores de todos los                                  0 – 65535            L dispositivos conectados al sistema |
| 279 | UINT8 |  | Lista da informação relativa   Consulte o quadro seguin­                       R ao estado da saída 2 de to­    te Sep.289, página 152 dos os dispositivos conecta­ dos ao sistema |
| 280 | UINT8 |  | Lista da informação relativa   Consulte o quadro seguin­                       R ao estado da saída 2 de to­    te Sep.290, página 152 dos os dispositivos conecta­ dos ao sistema |
| 384 | INT16 |  | Instantaneous outside tem­         0,01 °C                      -70 – 70              R perature |
| 385 | ENUM8 |  | Mod stagionale attiva (esta­      0:                              0–3                     R te / inverno)                     Inverno 1: Protezione antigelo 2: Banda estiva neutra 3: Estate |
| 400 | INT16 | AM016 | Température Départ Système reçue du gestionnaire de 0,01 °C                   -327,68 -          AM016 charge                                                                        327,68 |
| 401 | INT16 | AM018 | Température Retour Système reçue par le gestionnaire 0,01 °C                  -327,68 -          AM018 de consommateurs                                                              327,68 |
| 402 | INT16 | AM036 | Temperatura fumi in uscita        0,01 °C                         -20 – 120               R           AM036 dall'apparecchio it   5 Configurazione |
| 403 | INT16 | HM001 | Temperatura di mandata del­ 0,01 °C                           -20 – 120         R           HM001 la pompa di calore |
| 404 | INT16 | HM002 | Temperatura di ritorno della     0,01 °C                      -20 – 120         R           HM002 pompa di calore |
| 408 | UINT16 | DM004 | Température de consigne          0,01 °C                  0 – 655,35          R           DM004 départ eau chaude sanitaire |
| 409 | UINT8 | AM019 | Pression d'eau du circuit de l'appareil                        0,1 bar        0,0 – 3,0          AM019 5.7.3      Relever les températures de départ et de retour |
| 411 | ENUM8 | AM012 | Stato principale attuale del­    Vedere la tabella seguente                     R           AM012 l'apparecchio.                   Tab.236, pagina 124 |
| 412 | ENUM8 | AM014 | Subestado atual do apare­      Consulte o quadro seguin­                       R           AM014 lho.                           te Sep.292, página 153 |
| 413 | UINT16 | AM024 | Actueel relatief vermogen        %                        0 – 100             R           AM024 van het apparaat |
| 415 | UINT8 | GM008 | Nombre total de démarrages       0,1 µA                   0 – 25              R           GM008 du générateur de chaleur. Pour chauffage et eau chau­ de sanitaire |
| 419 | UINT32 | PC002 | Nombre total de démarrages       1 Unités                 0 – 4294967295      R           PC002 du générateur de chaleur. Pour chauffage et eau chau­ de sanitaire |
| 421 | UINT32 | PC003 | Número total de horas que el 1 horas                     0 – 4294967295     L          PC003 equipo ha producido energía para calefacción y agua ca­ liente sanitaria |
| 423 | UINT32 | AC030 | Número de arranques de la       Unidades 1               0 – 4294967295     L          AC030 primera fase de respaldo eléctrico |
| 425 | UINT32 | AC028 | Número de horas de funcio­      1 horas                  0 – 4294967295     L          AC028 namiento de la primera fase de respaldo eléctrico |
| 427 | UINT32 | AC031 | Numero di avviamenti del se­ 1 Unità                          0 – 4294967295    R           AC031 condo stadio di backup elet­ trico |
| 429 | UINT32 | AC029 | Número de horas de funcio­ 1 Horas                             0 – 4294967295        R           AC029 namento da segunda fase do apoio elétrico |
| 431 | UINT32 | AC001 | Numero di ore in cui l'appa­     1 Ore                        0 – 4294967295    R           AC001 recchio è stato collegato alla rete elettrica |
| 433 | UINT32 | AC005 | Energia consumida em               1 kWh                       0 – 4294967295        R           AC005 aquecimento central (kWh) |
| 435 | UINT32 | AC006 | Energia consumida em água          1 kWh                       0 – 4294967295        R           AC006 quente sanitária (kWh) |
| 437 | UINT32 | AC007 | Consommation d'énergie            1 kWh                      0 – 4294967295       R           AC007 pour le froid (kWh) |
| 439 | UINT32 |  | Totaal energieverbruik (kWh) 1 kWh                        0 – 4294967295      R/W 5 Configuratie    nl |
| 441 | UINT32 | AC018 | Vom Zusatzerzeuger ver­         1 kWh                       0 – 4294967295       R/W        AC018 brauchte Energie |
| 443 | UINT32 |  | Somme des énergies thermi­ 1 kWh                             0 – 4294967295       R/W ques produites (kWh) |
| 445 | UINT32 | AC008 | Erogazione di energia termi­     1 kWh                        0 – 4294967295    R/W         AC008 ca per il riscaldamento cen­ trale (kWh) |
| 447 | UINT32 | AC009 | Suministro de energía térmi­      1 kWh                       0 – 4294967295       L/E        AC009 ca para el agua caliente sa­ nitaria (kWh) |
| 449 | UINT32 | AC010 | Erogazione di energia termi­      1 kWh                        0 – 4294967295         R/W         AC010 ca per il raffrescamento (kWh) |
| 451 | UINT32 | AC019 | Vom elektrischen oder hyd­      1 kWh                       0 – 4294967295       R/W        AC019 raulischen Zusatzerzeuger gelieferte Energie |
| 459 | UINT16 | AM010 | Die aktuelle Drehzahl der       0,1%                        0 – 100              R/W        AM010 Pumpe |
| 460 | UINT32 | AM047 | Potenza effettiva dell'appa­      0,01 kW                      0 – 4294967295         R           AM047 recchio |
| 512 | ENUM8 | AM011 | È al momento richiesto un intervento di ma­        0: No                    R                          AM011 nutenzione?                                        1: Sì |
| 513 | UINT8 |  | Aktuelle oder nächste Wartungsmeldungen             0: Keine                    R 1: A 2: B 3: C 4: Benutzerdefiniert 5:D |
| 514 | UINT16 | AC002 | Number of hours that the appliance has              2 hours                  R                         AC002 been producing energy since last service |
| 515 | UINT16 | AC003 | Nombre d'heures de fonctionnement depuis       2 heures                 R                      AC003 le dernier entretien de l'appareil |
| 516 | UINT32 | AC004 | Numero di avvii del generatore di calore dal­ 1 Unità                       R                          AC004 l'ultimo intervento di manutenzione. 5.11       Codici di errore |
| 531 | UINT8 |  | Number entries of the 'cur­ 0: No error                 0-1                    R rent error' structure       1: At least 1 error on any appliance If you find an error, you can use object instance 128 to find out how many |
| 1100 | INT16 | CM040 | Measure Zone Flow Temperature or           0,01 °C                -10 –      R           CM040 DHW temperature                                                   140 |
| 1101 | UINT16 | CM070 | Setpoint di temperatura di mandata at­   0,01 °C                0 – 150     R            CM070 tuale della zona |
| 1102 | INT16 | CM190 | Consigne de température ambiance sou­ 0,1 °C                    5 – 30    R           CM190 haitée pour le circuit |
| 1107 | ENUM8 | CM130 | Activité en cours pour le circuit          0: Off                0–3      R           CM130 1 : Eco 2 : Confort 3 : Anti légionellose |
| 1108 | ENUM8 | CM120 | Modo de funcionamento da zona               0: Programação        0–3       R           CM120 horária 1: Manual 2: Desligado 3: Temporário |
| 1110 | UINT8 | CM050 | Status of the Pump of zone                 0: No                  0–1        R           CM050 1: Yes |
| 1111 | UINT8 | CM010 | Measure Zone Flow Temperature or           0: No                  0–1        R           CM010 DHW temperature                            1: Yes Tab.33     All main zones registers Zone        1         2            3    |
| 1115 | UINT32 | CC001 | Nombre d'heures de fonctionnement de       1 Heu­        0 - 4294967295        R           CC001 la pompe du circuit                        res |
| 1117 | UINT32 | CC010 | Numbers of times the pump of the zone      1 Units       0 - 4294967295        R            CC010 has started Tab.35     All main zones counter registers Zone       1           2          3        4           5         6 |
| 7101 | INT16 | NM001 | Température de départ de la cascade                            0,01 °C        -327,68 –          NM001 327,68 |
| 7163 | INT16 | NM165 | Rücklauftemperatur Kaskade                                0,01 °C         -327,68 –        NM165 327,68 5.8       Heizkreis-Zuordnung |
| 7169 | INT16 | EM013 | Temper. retorno medida en sis­   0,01 °C                    -327,68 - 327,68        L           EM013 tema en cascada en la botella de equilibrio (LLH) del lado secun­ dario |
| 9230 | UINT16 | HM031 | Berekende onmiddellijke           0,001                         0–1                 R           HM031 COP |
| 9231 | UINT16 | HM032 | Seuil du COP qui génère le        0,001                      0–1                  R           HM032 basculement entre la pompe à chaleur et la chaudière Tab.68    Champs de bits de 275 |