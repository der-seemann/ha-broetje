"""Constants for the Brötje Heatpump integration."""

from typing import Final

DOMAIN: Final = "broetje_heating"

# Default values
DEFAULT_PORT: Final = 502
DEFAULT_UNIT_ID: Final = 1
DEFAULT_SCAN_INTERVAL: Final = 30

# Configuration keys
CONF_UNIT_ID: Final = "unit_id"

# Manufacturer info
MANUFACTURER: Final = "Brötje"

# Register types
REG_INPUT: Final = "input"
REG_HOLDING: Final = "holding"

# Scale factors from Brötje documentation
SCALE_TEMP: Final = 1 / 64  # 0.015625 - for temperature values
SCALE_CURVE: Final = 1 / 50  # 0.02 - for heating curve slope
SCALE_POWER: Final = 1 / 10  # 0.1 - for power in kW
SCALE_PERCENT_100: Final = 1 / 100  # 0.01 - for percentages scaled by 100
SCALE_HOURS: Final = 1 / 3600  # for hours stored as seconds

# Operating mode enumeration (Betriebsart)
OPERATING_MODES: Final = {
    0: "protection",  # Schutzbetrieb
    1: "auto",  # Automatik
    2: "reduced",  # Reduziert
    3: "comfort",  # Komfort
}

# DHW Operating mode enumeration (Trinkwasser Betriebsart)
DHW_OPERATING_MODES: Final = {
    0: "off",  # Aus
    1: "on",  # Ein
    2: "eco",  # Eco
}

# DHW Release mode enumeration (Freigabe)
DHW_RELEASE_MODES: Final = {
    0: "24h",  # 24h/Tag
    1: "heating_program",  # Zeitprogramme Heizkreise
    2: "dhw_program",  # Zeitprogramm 4/TWW
}

# Legionella function mode enumeration
LEGIONELLA_MODES: Final = {
    0: "off",  # Aus
    1: "periodic",  # Periodisch
    2: "fixed_day",  # Fixer Wochentag
}

# Weekday enumeration
WEEKDAYS: Final = {
    1: "monday",
    2: "tuesday",
    3: "wednesday",
    4: "thursday",
    5: "friday",
    6: "saturday",
    7: "sunday",
}

# Burner power enumeration (Brennerleistung)
BURNER_POWER_MODES: Final = {
    1: "partial_load",  # Teillast
    2: "full_load",  # Volllast
    3: "max_heating_load",  # Maximale Heizlast
}

# Status codes (Statuscodes) - used by HC1 Status, Buffer Status, etc.
# From Brötje documentation Table 5 "Status codes (2 byte value)"
STATUS_CODES: Final = {
    0: "unknown",
    1: "slt_tripped",  # STB angesprochen
    2: "fault",  # Störung
    3: "limiter_tripped",  # Wächter angesprochen
    4: "manual_control",  # Handbetrieb aktiv
    5: "chimney_sweep_high",  # Schornsteinfegerfkt, Volllast
    6: "chimney_sweep_low",  # Schornsteinfegerfkt, Teillast
    7: "chimney_sweep_active",  # Schornsteinfegerfkt aktiv
    8: "locked_manual",  # Gesperrt, manuell
    9: "locked_automatic",  # Gesperrt, automatisch
    10: "locked",  # Gesperrt
    11: "protective_start",  # Anfahrentlastung
    12: "protective_start_low",  # Anfahrentlastung, Teillast
    13: "return_limitation",  # Rücklaufbegrenzung
    14: "return_limitation_low",  # Rücklaufbegrenzung, Teillast
    15: "released",  # Freigegeben
    16: "released_low",  # Freigegeben, Teillast
    17: "overrun_active",  # Nachlauf aktiv
    18: "in_operation",  # In Betrieb
    19: "released_2",  # Freigegeben
    20: "min_limitation",  # Minimalbegrenzung
    21: "min_limitation_low",  # Minimalbegrenzung, Teillast
    22: "min_limitation_active",  # Minimalbegrenzung aktiv
    23: "frost_prot_plant",  # Anlagefrostschutz aktiv
    24: "frost_protection",  # Frostschutz aktiv
    25: "off",  # Aus
    26: "emergency_operation",  # Notbetrieb
    27: "locked_externally",  # Gesperrt, extern
    51: "no_request",  # Keine Anforderung
    52: "frost_prot_collector",  # Kollektorfrostschutz aktiv
    53: "recooling_active",  # Rückkühlung aktiv
    54: "max_tank_temp",  # Max Speichertemp erreicht
    55: "evaporation_prot",  # Verdampfungsschutz aktiv
    56: "overtemp_prot",  # Überhitzschutz aktiv
    57: "max_charging_temp",  # Max Ladetemp erreicht
    58: "charging_dhw",  # Ladung Trinkwasser
    59: "charging_buffer",  # Ladung Pufferspeicher
    60: "charging_pool",  # Ladung Schwimmbad
    61: "min_charge_temp_not_reached",  # Min Ladetemp nicht erreicht
    62: "temp_diff_insufficient",  # Temp'differenz ungenügend
    63: "radiation_insufficient",  # Einstrahlung ungenügend
    67: "forced_charging",  # Zwangsladung aktiv
    68: "partial_charging",  # Teilladung aktiv
    69: "charging_active",  # Ladung aktiv
    70: "charged_max_tank",  # Geladen, max Speichertemp
    71: "charged_max_charging",  # Geladen, max Ladetemp
    72: "charged_forced",  # Geladen, Zwanglad Solltemp
    73: "charged_required",  # Teilgeladen, Solltemperatur
    74: "part_charged_required",  # Teilgeladen, Solltemperatur
    75: "charged",  # Geladen
    76: "cold",  # Kalt
    77: "recooling_collector",  # Rückkühlung via Kollektor
    78: "recooling_heat_gen",  # Rückkühlung via Erz/Hk's
    79: "discharging_prot",  # Entladeschutz aktiv
    80: "charge_time_limit",  # Ladezeitbegrenzung aktiv
    81: "charging_locked",  # Ladung gesperrt
    82: "charging_lock_active",  # Ladesperre aktiv
    83: "forced_max_tank",  # Zwang, max Speichertemp
    84: "forced_max_charging",  # Zwang, max Ladetemperatur
    85: "forced_legionella",  # Zwang, Legionellensollwert
    86: "forced_nominal",  # Zwang, Nennsollwert
    87: "el_charging_legionella",  # Ladung Elektro, Leg'sollwert
    88: "el_charging_nominal",  # Ladung Elektro, Nennsollwert
    89: "el_charging_reduced",  # Ladung Elektro, Red'sollwert
    90: "el_charging_frost",  # Ladung Elektro, Fros'sollwert
    91: "el_heater_released",  # Elektroeinsatz freigegeben
    92: "push_legionella",  # Push, Legionellensollwert
    93: "push_nominal",  # Push, Nennsollwert
    94: "push_active",  # Push aktiv
    95: "charging_legionella",  # Ladung, Legionellensollwert
    96: "charging_nominal",  # Ladung, Nennsollwert
    97: "charging_reduced",  # Ladung, Reduziertsollwert
    98: "charged_legionella",  # Geladen, Legio'temperatur
    99: "charged_nominal_temp",  # Geladen, Nenntemperatur
    100: "charged_reduced_temp",  # Geladen, Reduz'temperatur
    101: "frost_prot_room",  # Raumfrostschutz aktiv
    102: "floor_curing",  # Estrichfunktion aktiv
    103: "restricted_boiler",  # Eingeschränkt, Kesselschutz
    104: "restricted_dhw",  # Eingeschränkt, TWW-Vorrang
    105: "restricted_buffer",  # Eingeschränkt, Puffer
    106: "heating_restricted",  # Heizbetrieb eingeschränkt
    107: "forced_draw_buffer",  # Zwangsabnahme Puffer
    108: "forced_draw_dhw",  # Zwangsabnahme TWW
    109: "forced_draw_source",  # Zwangsabnahme Erzeuger
    110: "forced_draw",  # Zwangsabnahme
    111: "opt_start_boost",  # Einschaltopt+Schnellaufheiz
    112: "optimum_start",  # Einschaltoptimierung
    113: "boost_heating",  # Schnellaufheizung
    114: "comfort_heating",  # Heizbetrieb Komfort
    115: "optimum_stop",  # Ausschaltoptimierung
    116: "reduced_heating",  # Heizbetrieb Reduziert
    117: "frost_prot_flow",  # Vorlauffrostschutz aktiv
    118: "summer_operation",  # Sommerbetrieb
    119: "eco_24h",  # Tages-Eco aktiv
    120: "setback_reduced",  # Absenkung Reduziert
    121: "setback_frost",  # Absenkung Frostschutz
    122: "room_temp_limit",  # Raumtemp'begrenzung
    124: "charging_restricted",  # Ladung eingeschränkt
    137: "heating_mode",  # Heizbetrieb
    141: "boiler_frost_prot",  # Kesselfrostschutz aktiv
    142: "recooling_dhw_hc",  # Rückkühlung via TWW/Hk's
    143: "charged_min_temp",  # Geladen, Min Ladetemp
    147: "hot",  # Warm
    151: "charging_dhw_buffer_pool",  # Lad'ng TWW+Puffer+Sch'bad
    152: "charging_dhw_buffer",  # Ladung Trinkwasser+Puffer
    153: "charging_dhw_pool",  # Ladung Trinkwasser+Sch'bad
    154: "charging_buffer_pool",  # Ladung Puffer+Schwimmbad
    155: "heating_mode_source",  # Heizbetrieb Erzeuger
    156: "heated_max_pool",  # Geheizt, max Schw'badtemp
    157: "heated_setpoint_source",  # Geheizt, Sollwert Erzeuger
    158: "heated_setpoint_solar",  # Geheizt, Sollwert Solar
    159: "heated",  # Geheizt
    160: "heating_solar_off",  # Heizbetrieb Solar Aus
    161: "heating_source_off",  # Heizbetrieb Erzeuger Aus
    162: "heating_off",  # Heizbetrieb Aus
    166: "operation_hc",  # In Betrieb für Heizkreis
    167: "part_load_hc",  # In Teillastbetrieb für HK
    168: "operation_dhw",  # In Betrieb für Trinkwasser
    169: "part_load_dhw",  # In Teillastbetrieb für TWW
    170: "operation_hc_dhw",  # In Betrieb für HK, TWW
    171: "part_load_hc_dhw",  # In Teillastbetrieb für HK.TWW
    172: "locked_solid_fuel",  # Gesperrt, Feststoffkessel
    173: "released_hc_dhw",  # Freigegeben für HK, TWW
    174: "released_dhw",  # Freigegeben für TWW
    175: "released_hc",  # Freigegeben für HK
    176: "locked_outside_temp",  # Gesperrt, Aussentemperatur
    197: "electric_on",  # Elektro Ein
    198: "locked_economy",  # Gesperrt, Ökobetrieb
    199: "consumption",  # Zapfbetrieb
    200: "ready",  # Bereit
    203: "full_charging",  # Durchladung aktiv
    204: "locked_heating",  # Gesperrt, Heizbetrieb
    205: "locked_source",  # Gesperrt, Erzeuger
    206: "locked_buffer",  # Gesperrt, Puffer
    207: "comp_runtime_min",  # Verd'laufzeit Min aktiv, Kühl
    211: "lockout_position",  # Störstellung
    212: "start_prevention",  # Startverhinderung
    213: "shutdown",  # Ausserbetriebsetzung
    214: "safety_time",  # Sicherheitszeit
    215: "startup",  # Inbetriebsetzung
    216: "standby",  # Standby
    217: "home_run",  # Heimlauf
    218: "prepurge",  # Vorlüften
    219: "postpurge",  # Nachlüften
    220: "controller_stop",  # Reglerstopp aktiv
    221: "keep_hot_on",  # Warmhaltebetrieb ein
    222: "keep_hot_active",  # Warmhaltebetrieb aktiv
    223: "frost_prot_instant",  # Frostschutz Durchl'erhitzer
    224: "ignition",  # Zünden
    225: "settling_time",  # Einschwingzeit
    226: "exotic_gas",  # Exotengasbetrieb
    227: "drift_test",  # Drifttest aktiv
    228: "special_operation",  # Sonderbetrieb
    231: "start_drift_test",  # Start manueller Drifttest
    232: "flue_gas_switchoff",  # Abgastemp, Abschaltung
    233: "flue_gas_output_red",  # Abgastemp, Leist'begrenzung
    234: "flue_gas_too_high",  # Abgastemperatur zu hoch
    235: "water_pressure_low",  # Wasserdruck zu niedrig
    236: "party_function",  # Partyfunktion aktiv
    237: "transfer_legionella",  # Umladung, Legionellensollwert
    238: "transfer_nominal",  # Umladung, Nennsollwert
    239: "transfer_reduced",  # Umladung, Reduziertsollwert
    240: "transfer_active",  # Umladung aktiv
    241: "residual_heat",  # Restwärmenutzung
    242: "restratification",  # Umschichtung aktiv
    243: "keep_hot_released",  # Warmhaltebetrieb freigegeb'
    244: "source_released",  # Erzeuger freigegeben
    245: "slt_limits_output",  # STB begrenzt Leistung
    246: "mains_undervoltage",  # Netzunterspannung
    247: "temp_drop_prot",  # Unterkühlschutz aktiv
    248: "continuous_pump",  # Pumpendauerlauf
    298: "warmer_function",  # Wärmerfunktion aktiv
    299: "cooler_function",  # Kälterfunktion aktiv
    300: "adverse_wind",  # Gegenwindfunktion aktiv
}
