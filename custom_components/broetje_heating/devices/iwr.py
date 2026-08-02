"""IWR/GTW-08 device register, sensor, and enum definitions.

Based on GTW-08 Modbus Specification (7854678 - v.01 - 15092023).
"""

from __future__ import annotations

from typing import Any, Final

from ..const import (
    FEATURE_BUFFER_TANK,
    FEATURE_CASCADE,
    FEATURE_COOLING,
    FEATURE_HYBRID,
    REG_HOLDING,
    SUBDEV_BOILER,
    SUBDEV_BUFFER_TANK,
    SUBDEV_HYBRID,
    SUBDEV_SERVICE,
)

ZONE_ADDR_OFFSET: Final = 512
ZONE_TYPE_BASE_ADDR: Final = 640
ZONE_FUNCTION_BASE_ADDR: Final = 641

# Entity classification: (entity_category, entity_registry_enabled_default)
#   entity_category: None = primary, "diagnostic" = diagnostic
#   entity_registry_enabled_default: True = enabled, False = disabled by default
# Keys not listed default to (None, True).

IWR_STATIC_ENTITY_CLASSIFICATION: Final[dict[str, tuple[str | None, bool]]] = {
    # ===== Appliance core measurements — Primary =====
    "flow_temperature": (None, True),
    "return_temperature": (None, True),
    "outside_temperature": (None, True),
    "water_pressure": (None, True),
    "actual_power": (None, True),
    "cop": (None, True),
    "hybrid_cop": (None, True),
    "system_power": (None, True),
    "relative_power": (None, True),
    "pump_speed": (None, True),
    # ===== High-level status — Primary =====
    "main_status": (None, True),
    "sub_status": (None, True),
    "seasonal_mode": (None, True),
    "ch_enabled": (None, True),
    "dhw_enabled": (None, True),
    "dhw_eco_comfort_mode": (None, True),
    "cooling_enabled": (None, True),
    "service_notification": (None, True),
    # ===== Key binary status — Primary =====
    "status_heat_pump_on": (None, True),
    "status_flame_on": (None, True),
    "status_service_required": (None, True),
    "status_water_pressure_low": (None, True),
    "error_present": (None, True),
    "service_required": (None, True),
    "output_pump": (None, True),
    "output_dhw_active": (None, True),
    "output_ch_active": (None, True),
    "output_cooling_active": (None, True),
    "appliance_time_sensor": ("diagnostic", True),
    "low_noise_mode_state_sensor": ("diagnostic", True),
    "special_status_shutdown": ("diagnostic", False),
    "special_status_heating": ("diagnostic", False),
    "special_status_cooling": ("diagnostic", False),
    "special_status_screed_drying": ("diagnostic", False),
    "special_status_electric": ("diagnostic", False),
    "special_status_frost_protection": ("diagnostic", False),
    "special_status_summer_winter": ("diagnostic", False),
    "special_status_summer_neutral_band": ("diagnostic", False),
    # ===== Energy totals — Primary =====
    "total_energy_consumed": (None, True),
    "total_thermal_delivered": (None, True),
    "energy_consumed_ch": (None, True),
    "energy_consumed_dhw": (None, True),
    "thermal_delivered_ch": (None, True),
    "thermal_delivered_dhw": (None, True),
    "total_operating_hours": (None, True),
    "total_starts": (None, True),
    # ===== Main controller counters — Diagnostic, enabled =====
    "main_control_burner_starts": ("diagnostic", True),
    "main_control_burning_hours": ("diagnostic", True),
    "main_control_hours_after_service": ("diagnostic", True),
    "main_control_successful_compressor_starts_after_service": ("diagnostic", True),
    "main_control_backup1_starts": ("diagnostic", True),
    "main_control_backup1_hours": ("diagnostic", True),
    "main_control_backup2_starts": ("diagnostic", True),
    "main_control_backup2_hours": ("diagnostic", True),
    "main_control_active_hours": ("diagnostic", True),
    # ===== Appliance temperatures — Diagnostic, enabled =====
    "hp_flow_temperature": ("diagnostic", True),
    "hp_return_temperature": ("diagnostic", True),
    "exhaust_gas_temperature": ("diagnostic", True),
    "cu_flow_temperature": ("diagnostic", True),
    "cu_return_temperature": ("diagnostic", True),
    "cascade_flow_temperature": ("diagnostic", True),
    "cascade_return_temperature": ("diagnostic", True),
    "flow_rate": ("diagnostic", True),
    # ===== Setpoints and control — Diagnostic, enabled =====
    "ch_setpoint": ("diagnostic", True),
    "internal_dhw_setpoint": ("diagnostic", True),
    "dhw_flow_setpoint": ("diagnostic", True),
    "cooling_setpoint": ("diagnostic", True),
    "power_setpoint": ("diagnostic", True),
    "cooling_forced": ("diagnostic", True),
    # ===== Service counters — Diagnostic, enabled =====
    "hours_since_service": ("diagnostic", True),
    "hours_producing_since_service": ("diagnostic", True),
    "starts_since_service": ("diagnostic", True),
    # ===== Detailed energy breakdown — Diagnostic, enabled =====
    "energy_consumed_cooling": ("diagnostic", True),
    "energy_consumed_backup": ("diagnostic", True),
    "thermal_delivered_cooling": ("diagnostic", True),
    "energy_delivered_backup": ("diagnostic", True),
    "backup1_starts": ("diagnostic", True),
    "backup1_operating_hours": ("diagnostic", True),
    "backup2_starts": ("diagnostic", True),
    "backup2_operating_hours": ("diagnostic", True),
    "mains_power_hours": ("diagnostic", True),
    # ===== Appliance parameters — Diagnostic, disabled by default =====
    "summer_winter_threshold": ("diagnostic", False),
    "neutral_band": ("diagnostic", False),
    "frost_protection_threshold": ("diagnostic", False),
    "force_summer_mode": ("diagnostic", False),
    "control_power": (None, False),
    "control_temperature": (None, False),
    "control_algorithm_type": (None, False),
    "control_heat_demand_type": (None, False),
    "control_cooling_temperature": ("diagnostic", False),
    "cop_threshold": ("diagnostic", False),
    "hybrid_cop_threshold": ("diagnostic", False),
    "ionization_current": ("diagnostic", False),
    # ===== Status backup indicators — Diagnostic, disabled by default =====
    "status_backup1_on": ("diagnostic", False),
    "status_backup2_on": ("diagnostic", False),
    "status_dhw_backup_on": ("diagnostic", False),
    "status_power_down_needed": ("diagnostic", False),
    # ===== Bitfield internals — Diagnostic, disabled by default =====
    "demand_direct_zones": ("diagnostic", False),
    "demand_mixing_circuits": ("diagnostic", False),
    "demand_valves_open_safety": ("diagnostic", False),
    "demand_manual_heat": ("diagnostic", False),
    "demand_cooling_allowed": ("diagnostic", False),
    "demand_dhw_allowed": ("diagnostic", False),
    "demand_heat_engine_active": ("diagnostic", False),
    "output_3way_valve_open": ("diagnostic", False),
    "output_3way_valve": ("diagnostic", False),
    "output_3way_valve_closed": ("diagnostic", False),
    # ===== Discovery / system metadata — Diagnostic, disabled by default =====
    "manufacturer_code": ("diagnostic", False),
    "gateway_device_type": ("diagnostic", False),
    "zone_count": ("diagnostic", False),
    "zones_disabled": ("diagnostic", False),
    "zones_ch": ("diagnostic", False),
    "zones_ch_cooling": ("diagnostic", False),
    "zones_dhw": ("diagnostic", False),
    "zones_process_heat": ("diagnostic", False),
    "zones_swimming_pool": ("diagnostic", False),
    "zones_others": ("diagnostic", False),
    "buffer_tank_active": ("diagnostic", False),
    "cascade_role": ("diagnostic", False),
    "devices_connected": ("diagnostic", False),
    "appliance_error_priority": ("diagnostic", False),
    "current_generic_error_code": ("diagnostic", False),
    "cascade_producer_active_number": ("diagnostic", False),
    "cascade_number_of_producers": ("diagnostic", False),
    "cascade_number_of_stages_available": ("diagnostic", False),
    "cascade_number_of_stages_required": ("diagnostic", False),
    "cascade_power_request_power": ("diagnostic", True),
    "cascade_power_request_temperature_setpoint": ("diagnostic", True),
    "cascade_power_request_heat_demand_type": ("diagnostic", True),
    "cascade_system_power_setpoint_power": ("diagnostic", True),
    "cascade_system_power_setpoint_temperature_setpoint": ("diagnostic", True),
    "cascade_system_power_setpoint_heat_demand_type": ("diagnostic", True),
    "cascade_appliance_1_power_output": ("diagnostic", True),
    "cascade_appliance_1_flow_temperature": ("diagnostic", True),
    "cascade_appliance_1_status": ("diagnostic", True),
    "cascade_appliance_1_special_request": ("diagnostic", True),
    "cascade_appliance_3_power_output": ("diagnostic", True),
    "cascade_appliance_3_flow_temperature": ("diagnostic", True),
    "cascade_appliance_3_status": ("diagnostic", True),
    "cascade_appliance_3_special_request": ("diagnostic", True),
    "cascade_appliance_4_power_output": ("diagnostic", True),
    "cascade_appliance_4_flow_temperature": ("diagnostic", True),
    "cascade_appliance_4_status": ("diagnostic", True),
    "cascade_appliance_4_special_request": ("diagnostic", True),
    "cascade_appliance_5_power_output": ("diagnostic", True),
    "cascade_appliance_5_flow_temperature": ("diagnostic", True),
    "cascade_appliance_5_status": ("diagnostic", True),
    "cascade_appliance_5_special_request": ("diagnostic", True),
    "cascade_appliance_6_power_output": ("diagnostic", True),
    "cascade_appliance_6_flow_temperature": ("diagnostic", True),
    "cascade_appliance_6_status": ("diagnostic", True),
    "cascade_appliance_6_special_request": ("diagnostic", True),
    "cascade_appliance_7_power_output": ("diagnostic", True),
    "cascade_appliance_7_flow_temperature": ("diagnostic", True),
    "cascade_appliance_7_status": ("diagnostic", True),
    "cascade_appliance_7_special_request": ("diagnostic", True),
    "cascade_appliance_8_power_output": ("diagnostic", True),
    "cascade_appliance_8_flow_temperature": ("diagnostic", True),
    "cascade_appliance_8_status": ("diagnostic", True),
    "cascade_appliance_8_special_request": ("diagnostic", True),
    "cascade_appliance_9_power_output": ("diagnostic", True),
    "cascade_appliance_9_flow_temperature": ("diagnostic", True),
    "cascade_appliance_9_status": ("diagnostic", True),
    "cascade_appliance_9_special_request": ("diagnostic", True),
    "cascade_appliance_10_power_output": ("diagnostic", True),
    "cascade_appliance_10_flow_temperature": ("diagnostic", True),
    "cascade_appliance_10_status": ("diagnostic", True),
    "cascade_appliance_10_special_request": ("diagnostic", True),
    "cascade_requested_power_heat_demand": ("diagnostic", True),
    "cascade_requested_power_percentage": ("diagnostic", True),
    "cascade_time_to_start_next_stage": ("diagnostic", True),
    "cascade_primary_pump_relay_active": ("diagnostic", True),
    "cascade_secondary_pump_relay_active": ("diagnostic", True),
    "cascade_system_state": ("diagnostic", True),
    "cascade_operating_hours_heating": ("diagnostic", True),
    "cascade_operating_hours_dhw": ("diagnostic", True),
    "cascade_llh_return_temperature": ("diagnostic", True),
    "cascade_primary_llh_smart_pump_status": ("diagnostic", True),
    "cascade_primary_pump_control_output": ("diagnostic", True),
    "cascade_secondary_pump_control_output": ("diagnostic", True),
    "cascade_llh_flow_temperature": ("diagnostic", True),
    "cascade_appliances_needed_for_heat_demand": ("diagnostic", True),
    "cascade_temporary_permutation_order": ("diagnostic", True),
    "cascade_s_bus_producers_status": ("diagnostic", True),
    "cascade_s_bus_producers_generic_error_code": ("diagnostic", True),
    "cascade_em068_error_priority_brand_matrix": ("diagnostic", True),
    "cascade_appliance_flow_temperature": ("diagnostic", True),
    "cascade_appliance_return_temperature": ("diagnostic", True),
    "cascade_appliance_heat_exchanger_temperature": ("diagnostic", True),
    "cascade_appliance_flue_gas_temperature": ("diagnostic", True),
    "cascade_appliance_service_notification": ("diagnostic", True),
    "cascade_appliance_water_pressure": ("diagnostic", True),
    "cascade_appliance_second_return_temperature": ("diagnostic", True),
    "cascade_appliance_current_pump_speed": ("diagnostic", True),
    "cascade_appliance_actual_relative_power": ("diagnostic", True),
    "cascade_appliance_total_burner_hours": ("diagnostic", True),
    "cascade_appliance_dhw_burner_hours": ("diagnostic", True),
    "cascade_producer_order_node_id": ("diagnostic", True),
    "cascade_appliance_device_type": ("diagnostic", True),
    "cascade_outside_temperature_connected": ("diagnostic", True),
    "cascade_outside_temperature_used": ("diagnostic", True),
    "board1_device_type": ("diagnostic", True),
    "board1_software_version": ("diagnostic", True),
    "board1_config_table_version": ("diagnostic", True),
    "board1_hardware_version": ("diagnostic", True),
    "board1_article_number": ("diagnostic", True),
    "board2_device_type": ("diagnostic", True),
    "board2_software_version": ("diagnostic", True),
    "board2_config_table_version": ("diagnostic", True),
    "board2_hardware_version": ("diagnostic", True),
    "board2_article_number": ("diagnostic", True),
    "board3_device_type": ("diagnostic", True),
    "board3_software_version": ("diagnostic", True),
    "board3_config_table_version": ("diagnostic", True),
    "board3_hardware_version": ("diagnostic", True),
    "board3_article_number": ("diagnostic", True),
    "board4_device_type": ("diagnostic", True),
    "board4_software_version": ("diagnostic", True),
    "board4_config_table_version": ("diagnostic", True),
    "board4_hardware_version": ("diagnostic", True),
    "board4_article_number": ("diagnostic", True),
    "board5_device_type": ("diagnostic", True),
    "board5_software_version": ("diagnostic", True),
    "board5_config_table_version": ("diagnostic", True),
    "board5_hardware_version": ("diagnostic", True),
    "board5_article_number": ("diagnostic", True),
    "board6_device_type": ("diagnostic", True),
    "board6_software_version": ("diagnostic", True),
    "board6_config_table_version": ("diagnostic", True),
    "board6_hardware_version": ("diagnostic", True),
    "board6_article_number": ("diagnostic", True),
    "board7_device_type": ("diagnostic", True),
    "board7_software_version": ("diagnostic", True),
    "board7_config_table_version": ("diagnostic", True),
    "board7_hardware_version": ("diagnostic", True),
    "board7_article_number": ("diagnostic", True),
    "board8_device_type": ("diagnostic", True),
    "board8_software_version": ("diagnostic", True),
    "board8_config_table_version": ("diagnostic", True),
    "board8_hardware_version": ("diagnostic", True),
    "board8_article_number": ("diagnostic", True),
    "board9_device_type": ("diagnostic", True),
    "board9_software_version": ("diagnostic", True),
    "board9_config_table_version": ("diagnostic", True),
    "board9_hardware_version": ("diagnostic", True),
    "board9_article_number": ("diagnostic", True),
    "board10_device_type": ("diagnostic", True),
    "board10_software_version": ("diagnostic", True),
    "board10_config_table_version": ("diagnostic", True),
    "board10_hardware_version": ("diagnostic", True),
    "board10_article_number": ("diagnostic", True),
    # ===== Board errors — Diagnostic, disabled by default =====
    "board1_error_code": ("diagnostic", False),
    "board1_error_severity": ("diagnostic", False),
    "board2_error_code": ("diagnostic", False),
    "board2_error_severity": ("diagnostic", False),
    "board3_error_code": ("diagnostic", False),
    "board3_error_severity": ("diagnostic", False),
    "board4_error_code": ("diagnostic", False),
    "board4_error_severity": ("diagnostic", False),
    "board5_error_code": ("diagnostic", False),
    "board5_error_severity": ("diagnostic", False),
    "board6_error_code": ("diagnostic", False),
    "board6_error_severity": ("diagnostic", False),
    "board7_error_code": ("diagnostic", False),
    "board7_error_severity": ("diagnostic", False),
    "board8_error_code": ("diagnostic", False),
    "board8_error_severity": ("diagnostic", False),
    "board9_error_code": ("diagnostic", False),
    "board9_error_severity": ("diagnostic", False),
    "board10_error_code": ("diagnostic", False),
    "board10_error_severity": ("diagnostic", False),
    "buffer_tank_temperature_bottom": ("diagnostic", True),
    "buffer_tank_temperature_top": ("diagnostic", True),
    "buffer_tank_pump_state": ("diagnostic", True),
    "buffer_tank_mode": ("diagnostic", True),
}

# Zone entity classification keyed by translation_key (zone-number-agnostic).
IWR_ZONE_ENTITY_CLASSIFICATION: Final[dict[str, tuple[str | None, bool]]] = {
    # ===== Zone essentials — Primary =====
    "zone_room_temp": (None, True),
    "zone_room_temp_measured": (None, True),
    "zone_flow_temp": (None, True),
    "zone_flow_setpoint": (None, True),
    "zone_room_setpoint": (None, True),
    "zone_heating_mode": (None, True),
    "zone_pump": (None, True),
    "zone_heat_demand": (None, True),
    "zone_activity": (None, True),
    "zone_operating_mode": (None, True),
    # ===== Zone energy/runtime — Primary =====
    "zone_pump_hours": (None, True),
    "zone_pump_starts": (None, True),
    # ===== Zone medium-advanced — Diagnostic, enabled =====
    "zone_outside_temp": ("diagnostic", True),
    "zone_time_program_selected": ("diagnostic", True),
    "zone_night_setback": ("diagnostic", True),
    "zone_heating_curve_gradient": ("diagnostic", True),
    "zone_heating_curve_footpoint": ("diagnostic", True),
    "zone_max_flow_setpoint": ("diagnostic", True),
    "zone_fixed_flow_setpoint": ("diagnostic", True),
    # ===== Zone writable entities — Primary, enabled =====
    "zone_room_setpoint_manual": (None, True),
    "zone_control_mode": (None, True),
    # ===== Zone commissioning metadata — Diagnostic, disabled by default =====
    "zone_function": ("diagnostic", False),
    "zone_device_type": ("diagnostic", False),
    "zone_type": ("diagnostic", False),
    "zone_heating_control_strategy": ("diagnostic", False),
    # ===== Zone deep tuning — Diagnostic, disabled by default =====
    "zone_comfort_setpoint_1": ("diagnostic", False),
    "zone_comfort_setpoint_2": ("diagnostic", False),
    "zone_comfort_setpoint_3": ("diagnostic", False),
    "zone_comfort_setpoint_4": ("diagnostic", False),
    "zone_comfort_setpoint_5": ("diagnostic", False),
    "zone_cooling_room_setpoint_1": ("diagnostic", False),
    "zone_cooling_room_setpoint_2": ("diagnostic", False),
    "zone_cooling_room_setpoint_3": ("diagnostic", False),
    "zone_cooling_room_setpoint_4": ("diagnostic", False),
    "zone_cooling_room_setpoint_5": ("diagnostic", False),
    "zone_cooling_night_setback": ("diagnostic", False),
    "zone_holiday_setpoint": ("diagnostic", False),
    "zone_temporary_setpoint": ("diagnostic", False),
    "zone_dhw_comfort_setpoint": (None, True),
    "zone_dhw_reduced_setpoint": (None, True),
    "zone_dhw_holiday_setpoint": (None, True),
    "zone_dhw_antilegionella_setpoint": (None, True),
    "zone_swimming_pool_setpoint": ("diagnostic", False),
    "zone_process_heat_setpoint": ("diagnostic", False),
    "zone_cooling_mixing_setpoint": ("diagnostic", False),
    "zone_heating_curve_footpoint_night": ("diagnostic", False),
    "zone_max_preheat_time": ("diagnostic", False),
    "zone_mixing_valve_shift": ("diagnostic", False),
    "zone_mixing_valve_bandwidth": ("diagnostic", False),
    "zone_dhw_hysteresis": ("diagnostic", False),
    "zone_dhw_calorifier_offset": ("diagnostic", False),
    "zone_dhw_calorifier_raise": ("diagnostic", False),
    "zone_process_heat_hysteresis": ("diagnostic", False),
    "zone_process_heat_offset": ("diagnostic", False),
    "zone_process_heat_calorifier_raise": ("diagnostic", False),
    "zone_dhw_calorifier_hysteresis": ("diagnostic", True),
    "zone_pump_post_run": ("diagnostic", False),
    # ===== Zone low-level flags — Diagnostic, disabled by default =====
    "zone_flow_measurement": ("diagnostic", False),
    "zone_mixing_valve_opening": ("diagnostic", False),
    "zone_swimming_pool_pump": ("diagnostic", False),
    "zone_electrical_backup_output": ("diagnostic", False),
}

# Board discovery entities — all diagnostic, disabled by default.
IWR_BOARD_ENTITY_CLASSIFICATION: Final[tuple[str | None, bool]] = ("diagnostic", True)

# ===== IWR/GTW-08 Scale Factors =====
# These differ from ISR scale factors
IWR_SCALE_TEMP: Final = 0.01  # 0.01 °C resolution
IWR_SCALE_PRESSURE: Final = 0.1  # 0.1 bar resolution
IWR_SCALE_POWER: Final = 0.01  # 0.01 kW resolution
IWR_SCALE_COP: Final = 0.001  # COP resolution
IWR_SCALE_PUMP: Final = 0.1  # 0.1% pump speed
IWR_SCALE_ROOM_TEMP: Final = 0.1  # 0.1 °C for room temperature setpoints

# ===== IWR Enum Maps =====

# Tab.16 AM012 - Main appliance status
IWR_MAIN_STATUS: Final = {
    0: "standby",
    1: "heat_demand",
    2: "generator_start",
    3: "generator_ch",
    4: "generator_dhw",
    5: "generator_stop",
    6: "pump_post_run",
    7: "cooling_active",
    8: "controlled_stop",
    9: "blocking_mode",
    10: "locking_mode",
    11: "load_test_min",
    12: "load_test_ch_max",
    13: "load_test_dhw_max",
    15: "manual_heat_demand",
    16: "frost_protection",
    17: "deaeration",
    18: "control_unit_cooling",
    19: "reset_in_progress",
    20: "auto_filling",
    21: "halted",
    22: "forced_calibration",
    23: "factory_test",
    24: "hydronic_balancing",
    200: "device_mode",
    254: "unknown",
}

# Tab.17 AM014 - Sub status
IWR_SUB_STATUS: Final = {
    0: "standby",
    1: "anti_cycling",
    2: "close_hydraulic_valve",
    3: "close_pump",
    4: "waiting_for_start_cond",
    10: "close_ext_gas_valve",
    11: "start_to_glue_gas_valve",
    12: "close_flue_gas_valve",
    13: "fan_to_pre_purge",
    14: "wait_for_release_signal",
    15: "burner_on_command",
    16: "vps_test",
    17: "pre_ignition",
    18: "ignition",
    19: "flame_check",
    20: "interpurge",
    21: "generator_starting",
    30: "normal_int_setpoint",
    31: "limited_int_setpoint",
    32: "normal_power_control",
    33: "grad_level1_power_ctrl",
    34: "grad_level2_power_ctrl",
    35: "grad_level3_power_ctrl",
    36: "protect_flame_pwr_ctrl",
    37: "stabilization_time",
    38: "cold_start",
    39: "ch_resume",
    40: "su_remove_burner",
    41: "fan_to_post_purge",
    42: "open_ext_flue_gas_valve",
    43: "stop_fan_to_flue_gv_rpm",
    44: "stop_fan",
    45: "limited_pwr_on_tflue_gas",
    46: "auto_filling_install",
    47: "auto_filling_top_up",
    48: "reduced_set_point",
    49: "offset_adaption",
    60: "pump_post_running",
    61: "open_pump",
    62: "open_hydraulic_valve",
    63: "start_anticycle_time",
    65: "compressor_relieved",
    66: "hp_tmax_backup_on",
    67: "outdoor_limit_hp_off",
    68: "hp_stop_by_hybrid",
    69: "defrost_with_hp",
    70: "defrost_with_backup",
    71: "defrost_hp_backup",
    72: "source_pump_backup",
    73: "hp_flow_over_tmax",
    74: "source_pump_post_run",
    75: "hp_off_high_humidity",
    76: "hp_off_water_flow",
    78: "humidity_setpoint",
    79: "generators_relieved",
    80: "hp_relieved_cooling",
    81: "hp_stop_outdoor_temp",
    82: "hp_off_flow_tmax",
    83: "deair_pump_valve_ch",
    84: "deair_pump_valve_dhw",
    85: "deair_valve_ch",
    86: "deair_valve_dhw",
    88: "bl_backup_off",
    89: "bl_hp_off",
    90: "bl_hp_backup_off",
    91: "low_tariff",
    92: "pv_with_hp",
    93: "pv_hp_and_backup",
    94: "smart_grid",
    95: "waiting_for_waterpress",
    96: "no_producer_available",
    97: "increased_min_power",
    98: "decreased_max_power",
    102: "free_cool_pump_off",
    103: "free_cool_pump_on",
    104: "source_pump_pre_run",
    105: "calibration",
    106: "blocking_active",
    107: "warm_up",
    108: "defrost_curative",
    109: "defrost_preventive",
    200: "initialising_done",
    201: "initialising_csu",
    202: "init_identifiers",
    203: "init_bl_parameter",
    204: "init_safety_unit",
    205: "init_blocking",
    254: "state_unknown",
    255: "su_out_of_resets_wait",
}

# Seasonal mode (register 385)
IWR_SEASONAL_MODE: Final = {
    0: "winter",
    1: "frost_protection",
    2: "summer_neutral",
    3: "summer",
}

# Zone activity (CM130, register 1107 etc.)
IWR_ZONE_ACTIVITY: Final = {
    0: "off",
    1: "eco",
    2: "comfort",
    3: "anti_legionella",
}

# Zone operating mode (CM120, register 1108 etc.)
IWR_ZONE_OPERATING_MODE: Final = {
    0: "scheduling",
    1: "manual",
    2: "off",
    3: "temporary",
}

# Service notification type (register 513)
IWR_SERVICE_NOTIFICATION: Final = {
    0: "none",
    1: "a",
    2: "b",
    3: "c",
    4: "custom",
    5: "d",
    255: "device_not_available",
}

# Error severity (registers 533, 535, etc.)
IWR_ERROR_SEVERITY: Final = {
    0: "locking",
    3: "blocking",
    6: "warning",
    254: "device_not_available",
    255: "no_error",
}

# Zone function type (Tab.25/26, CP02X, registers 641 etc.)
IWR_ZONE_FUNCTION: Final = {
    0: "disable",
    1: "direct",
    2: "mixing_circuit",
    3: "swimming_pool",
    4: "high_temperature",
    5: "fan_convector",
    6: "dhw_tank",
    7: "electrical_dhw",
    8: "time_program",
    9: "process_heat",
    10: "dhw_layered",
    11: "dhw_internal_tank",
    12: "dhw_commercial_tank",
    13: "occupied",
    254: "dhw_primary",
}

# Device category lookup for 0xZZYY device type (Tab.26)
IWR_DEVICE_CATEGORY: Final = {
    0x00: "CU-GH",
    0x01: "CU-OH",
    0x02: "EHC",
    0x14: "MK",
    0x19: "SCB",
    0x1B: "EEC",
    0x1E: "Gateway",
}

# Zone control mode (CP32X, Tab.36/42, registers 649 etc.)
IWR_ZONE_CONTROL_MODE: Final = {
    0: "scheduling",
    1: "manual",
    2: "off",
}

# Tab.19 - Algorithm type (register 258)
IWR_ALGORITHM_TYPE: Final = {
    0: "remote_temp_and_power",
    1: "remote_power",
    2: "remote_temperature",
    3: "monitoring_only",
}

# Tab.20 - Heat demand type (register 259)
IWR_HEAT_DEMAND_TYPE: Final = {
    0: "standby",
    7: "heating",
    8: "cooling",
}

# Generic on/off enum (registers 389, 500, 501, 503)
IWR_ON_OFF: Final = {
    0: "off",
    1: "on",
}

# Zone current heating mode (register 1109 etc.)
IWR_ZONE_HEATING_MODE: Final = {
    0: "standby",
    1: "heating",
    2: "cooling",
    255: "device_not_available",
}

# Zone type (register 640 etc.)
IWR_ZONE_TYPE: Final = {
    0: "not_present",
    1: "ch_only",
    2: "ch_and_cooling",
    3: "dhw",
    4: "process_heat",
    5: "swimming_pool",
    254: "other",
}

# Heating control strategy (register 671 etc.)
IWR_HEATING_CONTROL_STRATEGY: Final = {
    0: "auto",
    1: "room",
    2: "outdoor",
    3: "outdoor_and_room",
    255: "device_not_available",
}

# Time program selection (register 688 etc.)
IWR_TIME_PROGRAM_SELECTED: Final = {
    0: "time_program_1",
    1: "time_program_2",
    2: "time_program_3",
}

# Cooling enabled mode (register 502)
IWR_COOLING_ENABLED: Final = {
    0: "off",
    1: "active_cooling",
    2: "free_cooling",
}

# DHW ECO / COMFORT mode (register 479, DP051)
IWR_DHW_ECO_COMFORT: Final = {
    0: "eco_hp_only",
    1: "comfort_hp_boiler",
}

# Boiler / appliance enums from the GTW-08 parameter list.
IWR_INTERNAL_HEAT_DEMAND_TYPE: Final = {
    0: "none",
    1: "dhw_primary",
    2: "dhw_high_priority",
    3: "process_heat",
    4: "screed_drying",
    5: "dhw_medium_priority",
    6: "dhw_low_priority",
    7: "central_heating",
    8: "cooling",
    9: "electrical_active",
    10: "electrical_reactive",
}

IWR_OUTDOOR_UNIT_OPERATION_MODE: Final = {
    0: "standby",
    1: "heating",
    2: "dhw_high_priority",
    3: "cooling",
    65535: "device_not_available",
}

IWR_HYBRID_MODE_SELECTED: Final = {
    0: "no_hybrid",
    1: "hybrid_cost",
    2: "hybrid_primary_energy",
    3: "hybrid_co2",
}

IWR_LOGIC_CONTACT: Final = {
    0: "open",
    1: "closed",
}

IWR_BLOCKING_INPUT_SETTING: Final = {
    0: "not_used",
    1: "full_blocking",
    2: "partial_blocking",
    3: "user_reset_locking",
    4: "backup_relieved",
    5: "generator_relieved",
    6: "generator_and_backup_relieved",
    7: "high_tariff_low_tariff",
    8: "photovoltaic_heat_pump_only",
    9: "photovoltaic_heat_pump_and_backup",
    10: "smart_grid_ready",
    11: "heating_cooling",
    12: "central_heating_blocking",
}

IWR_LOW_NOISE_MODE_STATE: Final = {
    0: "no_silent_mode",
    1: "silent_mode_level_1",
    2: "silent_mode_level_2",
    3: "silent_mode_level_3",
    4: "silent_mode_level_4",
    5: "silent_mode_level_5",
}

IWR_BUFFER_TANK_MODE: Final = {
    0: "decoupling_tank",
    1: "storage_tank",
}

IWR_NO_YES: Final = {
    0: "no",
    1: "yes",
    255: "device_not_available",
}

IWR_CASCADE_SYSTEM_STATE: Final = {
    0: "standby",
    1: "heat_demand",
    2: "burner_start",
    3: "burning_ch",
    4: "burning_dhw",
    5: "burner_stop",
    6: "pump_post_run",
    7: "cooling_active",
    8: "controlled_stop",
    9: "blocking_mode",
    10: "locking_mode",
    11: "cs_mode_l_ch",
    12: "cs_mode_h_ch",
    13: "cs_mode_h_dhw",
    14: "cs_mode_custom",
    15: "manual_hd_ch_on",
    16: "boiler_frost_prot",
    17: "de_air",
    18: "cu_cooling",
    19: "reset_in_progress",
    20: "auto_filling",
    21: "halted",
    22: "forced_calibration",
    23: "factory_test",
    24: "hydraulic_balancing_mode",
    200: "device_mode",
    254: "unknown",
    255: "device_not_available",
}

IWR_CASCADE_ROLE: Final = {
    0: "no",
    1: "cascade_master",
    2: "cascade_slave",
}

IWR_BACKUP_TYPE: Final = {
    0: "no_backup",
    1: "1_stage_electrical_backup",
    2: "2_stages_electrical_backup",
    3: "boiler_backup",
}

# Collected enum maps for IWR device
IWR_ENUM_MAPS: Final = {
    "iwr_main_status": IWR_MAIN_STATUS,
    "iwr_sub_status": IWR_SUB_STATUS,
    "iwr_seasonal_mode": IWR_SEASONAL_MODE,
    "iwr_zone_activity": IWR_ZONE_ACTIVITY,
    "iwr_zone_operating_mode": IWR_ZONE_OPERATING_MODE,
    "iwr_service_notification": IWR_SERVICE_NOTIFICATION,
    "iwr_error_severity": IWR_ERROR_SEVERITY,
    "iwr_algorithm_type": IWR_ALGORITHM_TYPE,
    "iwr_heat_demand_type": IWR_HEAT_DEMAND_TYPE,
    "iwr_zone_control_mode": IWR_ZONE_CONTROL_MODE,
    "iwr_zone_function": IWR_ZONE_FUNCTION,
    "iwr_on_off": IWR_ON_OFF,
    "iwr_cooling_enabled": IWR_COOLING_ENABLED,
    "iwr_zone_type": IWR_ZONE_TYPE,
    "iwr_zone_heating_mode": IWR_ZONE_HEATING_MODE,
    "iwr_heating_control_strategy": IWR_HEATING_CONTROL_STRATEGY,
    "iwr_time_program_selected": IWR_TIME_PROGRAM_SELECTED,
    "iwr_dhw_eco_comfort": IWR_DHW_ECO_COMFORT,
    "iwr_internal_heat_demand_type": IWR_INTERNAL_HEAT_DEMAND_TYPE,
    "iwr_outdoor_unit_operation_mode": IWR_OUTDOOR_UNIT_OPERATION_MODE,
    "iwr_hybrid_mode_selected": IWR_HYBRID_MODE_SELECTED,
    "iwr_logic_contact": IWR_LOGIC_CONTACT,
    "iwr_blocking_input_setting": IWR_BLOCKING_INPUT_SETTING,
    "iwr_low_noise_mode_state": IWR_LOW_NOISE_MODE_STATE,
    "iwr_buffer_tank_mode": IWR_BUFFER_TANK_MODE,
    "iwr_no_yes": IWR_NO_YES,
    "iwr_cascade_system_state": IWR_CASCADE_SYSTEM_STATE,
    "iwr_cascade_role": IWR_CASCADE_ROLE,
    "iwr_backup_type": IWR_BACKUP_TYPE,
}

# ===== Zone Address Tables =====
# From Tab.33 and Tab.35 in the GTW-08 Modbus specification.
# Zones 1-12 addresses for each register type.

ZONE_ADDRESSES: Final = {
    # Tab.33 - Main zone registers (read-only)
    "CM040": [1100, 1612, 2124, 2636, 3148, 3660, 4172, 4684, 5196, 5708, 6220, 6732],
    "CM070": [1101, 1613, 2125, 2637, 3149, 3661, 4173, 4685, 5197, 5709, 6221, 6733],
    "CM190": [1102, 1614, 2126, 2638, 3150, 3662, 4174, 4686, 5198, 5710, 6222, 6734],
    "CM130": [1107, 1619, 2131, 2643, 3155, 3667, 5121, 5633, 6145, 6657, 7169, 7681],
    "CM120": [1108, 1620, 2132, 2644, 3156, 3668, 5122, 5634, 6146, 6658, 7170, 7682],
    "CM050": [1110, 1622, 2134, 2646, 3158, 3670, 5124, 5636, 6148, 6660, 7172, 7684],
    "CM010": [1111, 1623, 2135, 2647, 3159, 3671, 5125, 5637, 6149, 6661, 7173, 7685],
    # Tab.35 - Zone counter registers (read-only)
    "CC001": [1115, 1627, 2139, 2651, 3163, 3675, 4187, 4699, 5211, 5723, 6235, 6747],
    "CC010": [1117, 1629, 2141, 2652, 3165, 3677, 4189, 4771, 5213, 5725, 6237, 6749],
    # Tab.25 - Zone function type CP02X (R, base 641, +512/zone)
    "CP02X": [641, 1153, 1665, 2177, 2689, 3201, 3713, 4225, 4737, 5249, 5761, 6273],
    # Tab.25 - Zone device type (R, base 645, +512/zone)
    "DEV": [645, 1157, 1669, 2181, 2693, 3205, 3717, 4229, 4741, 5253, 5765, 6277],
    # Tab.36/42 - Zone control mode CP32X (R/W, base 649, +512/zone)
    "CP32X": [649, 1161, 1673, 2185, 2697, 3209, 3721, 4233, 4745, 5257, 5769, 6281],
    # Tab.37 - Zone fixed flow setpoint CP01X (R/W, base 648, +512/zone)
    "CP01X": [648, 1160, 1672, 2184, 2696, 3208, 3720, 4232, 4744, 5256, 5768, 6280],
    # Tab.43 - Zone room temp setpoint manual CP20X (R/W, base 664, +512/zone)
    "CP20X": [664, 1176, 1688, 2200, 2712, 3224, 3736, 4248, 4760, 5272, 5784, 6296],
    # Tab.39 - Heating curve gradient CP23X (R/W, base 674, +512/zone)
    "CP23X": [674, 1186, 1698, 2210, 2722, 3234, 3746, 4258, 4770, 5282, 5794, 6306],
    # Tab.40 - Heating curve footpoint CP21X (R/W, base 675, +512/zone)
    # NOTE: PDF has typos for Z5 (2722) and Z8 (4258); corrected to 2723/4259.
    "CP21X": [675, 1187, 1699, 2211, 2723, 3235, 3747, 4259, 4771, 5283, 5795, 6307],
}

# ===== Static Register Map (non-zone registers) =====

_IWR_STATIC_REGISTER_MAP: Final = {
    # --- Device Information GTW-08 (from German spec 7740782-01) ---
    "manufacturer_code": {
        "address": 1,
        "type": REG_HOLDING,
        "count": 10,
        "data_type": "string",
        "scale": 1,
    },
    "gateway_device_type": {
        "address": 11,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    # --- Zone Detection (Tab.24) ---
    "zone_count": {
        "address": 189,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    # --- Zone Count Subtypes (from German spec 7740782-01) ---
    "zones_disabled": {
        "address": 190,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "zones_ch": {
        "address": 191,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "zones_ch_cooling": {
        "address": 192,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "zones_dhw": {
        "address": 193,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "zones_process_heat": {
        "address": 194,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "zones_swimming_pool": {
        "address": 195,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "zones_others": {
        "address": 196,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "buffer_tank_active": {
        "address": 197,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_role": {
        "address": 198,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    # --- Temperature and Power Control (Tab.18) ---
    "control_power": {
        "address": 256,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "control_temperature": {
        "address": 257,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": IWR_SCALE_TEMP,
    },
    "control_algorithm_type": {
        "address": 258,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "control_heat_demand_type": {
        "address": 259,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "control_cooling_temperature": {
        "address": 260,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    # --- Main Appliance Information (Tab.12) ---
    "system_power": {
        "address": 272,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    # --- Received Temperatures from CU (from German spec 7740782-01) ---
    "cu_flow_temperature": {
        "address": 273,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "cu_return_temperature": {
        "address": 274,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "error_list": {
        "address": 277,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "appliance_error_priority": {
        "address": 278,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "outside_temperature": {
        "address": 384,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "seasonal_mode": {
        "address": 385,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    # --- Appliance Parameters (from German spec 7740782-01) ---
    "summer_winter_threshold": {
        "address": 386,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": IWR_SCALE_TEMP,
    },
    "neutral_band": {
        "address": 387,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": IWR_SCALE_TEMP,
    },
    "frost_protection_threshold": {
        "address": 388,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "force_summer_mode": {
        "address": 389,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "flow_temperature": {
        "address": 400,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "return_temperature": {
        "address": 401,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "exhaust_gas_temperature": {
        "address": 402,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "hp_flow_temperature": {
        "address": 403,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "hp_return_temperature": {
        "address": 404,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    # --- Internal Setpoints (from German spec 7740782-01) ---
    "internal_dhw_setpoint": {
        "address": 405,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": IWR_SCALE_TEMP,
    },
    "ch_setpoint": {
        "address": 406,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": IWR_SCALE_TEMP,
    },
    "cooling_setpoint": {
        "address": 407,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": IWR_SCALE_TEMP,
    },
    "dhw_flow_setpoint": {
        "address": 408,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": IWR_SCALE_TEMP,
    },
    "water_pressure": {
        "address": 409,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": IWR_SCALE_PRESSURE,
    },
    "flow_rate": {
        "address": 410,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": IWR_SCALE_TEMP,  # 0.01 l/min
    },
    "main_status": {
        "address": 411,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "sub_status": {
        "address": 412,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "relative_power": {
        "address": 413,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "power_setpoint": {
        "address": 414,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": IWR_SCALE_PUMP,  # 0.1%
    },
    "ionization_current": {
        "address": 415,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": IWR_SCALE_PRESSURE,  # 0.1 µA
    },
    # MainControlMonitoring counters (Tab.11)
    "main_control_burner_starts": {
        "address": 288,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "main_control_burning_hours": {
        "address": 290,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "main_control_hours_after_service": {
        "address": 292,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 2,
    },
    "main_control_successful_compressor_starts_after_service": {
        "address": 293,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "main_control_backup1_starts": {
        "address": 295,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "main_control_backup1_hours": {
        "address": 297,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "main_control_backup2_starts": {
        "address": 299,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "main_control_backup2_hours": {
        "address": 301,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "main_control_active_hours": {
        "address": 303,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "total_starts": {
        "address": 419,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "total_operating_hours": {
        "address": 421,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "backup1_starts": {
        "address": 423,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "backup1_operating_hours": {
        "address": 425,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "backup2_starts": {
        "address": 427,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "backup2_operating_hours": {
        "address": 429,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "mains_power_hours": {
        "address": 431,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "energy_consumed_ch": {
        "address": 433,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "energy_consumed_dhw": {
        "address": 435,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "energy_consumed_cooling": {
        "address": 437,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "total_energy_consumed": {
        "address": 439,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "energy_consumed_backup": {
        "address": 441,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "total_thermal_delivered": {
        "address": 443,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "thermal_delivered_ch": {
        "address": 445,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "thermal_delivered_dhw": {
        "address": 447,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "thermal_delivered_cooling": {
        "address": 449,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "energy_delivered_backup": {
        "address": 451,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "pump_speed": {
        "address": 459,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": IWR_SCALE_PUMP,
    },
    "actual_power": {
        "address": 460,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": IWR_SCALE_POWER,
    },
    # HM031 - Instantaneous COP calculated by Hybrid application (Tab. Boiler)
    "hybrid_cop": {
        "address": 462,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": IWR_SCALE_COP,
    },
    # HM032 - COP threshold calculated by Hybrid application (Tab. Boiler)
    "hybrid_cop_threshold": {
        "address": 463,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": IWR_SCALE_COP,
    },
    "cop": {
        "address": 9230,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": IWR_SCALE_COP,
    },
    "cop_threshold": {
        "address": 9231,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": IWR_SCALE_COP,
    },
    # --- Cascade Flow/Return Temperature (Tab.23) ---
    "cascade_flow_temperature": {
        "address": 7101,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "cascade_return_temperature": {
        "address": 7163,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    # --- Bitfield registers (Tab.13-15) ---
    # Register 275 bits (Tab.13 - Heat demand bitfield)
    "demand_direct_zones": {
        "address": 275,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 0,
    },
    "demand_mixing_circuits": {
        "address": 275,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 1,
    },
    "demand_valves_open_safety": {
        "address": 275,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 2,
    },
    "demand_manual_heat": {
        "address": 275,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 3,
    },
    "demand_cooling_allowed": {
        "address": 275,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 4,
    },
    "demand_dhw_allowed": {
        "address": 275,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 5,
    },
    "demand_heat_engine_active": {
        "address": 275,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 6,
    },
    # Register 276 bits (Tab.13 - Special status bitfield)
    "special_status_shutdown": {
        "address": 276,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 0,
    },
    "special_status_heating": {
        "address": 276,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 1,
    },
    "special_status_cooling": {
        "address": 276,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 2,
    },
    "special_status_screed_drying": {
        "address": 276,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 3,
    },
    "special_status_electric": {
        "address": 276,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 4,
    },
    "special_status_frost_protection": {
        "address": 276,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 5,
    },
    "special_status_summer_winter": {
        "address": 276,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 6,
    },
    "special_status_summer_neutral_band": {
        "address": 276,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 7,
    },
    # Register 279 bits (Tab.14 - Output status 1)
    "status_flame_on": {
        "address": 279,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 0,
    },
    "status_heat_pump_on": {
        "address": 279,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 1,
    },
    "status_backup1_on": {
        "address": 279,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 2,
    },
    "status_backup2_on": {
        "address": 279,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 3,
    },
    "status_dhw_backup_on": {
        "address": 279,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 4,
    },
    "status_service_required": {
        "address": 279,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 5,
    },
    "status_power_down_needed": {
        "address": 279,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 6,
    },
    "status_water_pressure_low": {
        "address": 279,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 7,
    },
    "status_bitfields_number_1": {
        "address": 340,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint8",
        "scale": 1,
    },
    "status_bitfields_number_2": {
        "address": 341,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint8",
        "scale": 1,
    },
    "status_bitfields_number_3": {
        "address": 342,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint8",
        "scale": 1,
    },
    "appliance_time": {
        "address": 350,
        "type": REG_HOLDING,
        "count": 3,
        "data_type": "appliance_time",
        "scale": 1,
    },
    # Register 280 bits (Tab.15 - Output status 2)
    "output_pump": {
        "address": 280,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 0,
    },
    "output_3way_valve_open": {
        "address": 280,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 1,
    },
    "output_3way_valve": {
        "address": 280,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 2,
    },
    "output_3way_valve_closed": {
        "address": 280,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 3,
    },
    "output_dhw_active": {
        "address": 280,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 4,
    },
    "output_ch_active": {
        "address": 280,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 5,
    },
    "output_cooling_active": {
        "address": 280,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "bool",
        "bit": 6,
    },
    # --- DHW ECO/COMFORT mode (DP051, Excel parameterlist) ---
    "dhw_eco_comfort_mode": {
        "address": 479,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
        "writable": True,
        "min": 0,
        "max": 1,
    },
    "low_noise_mode_state": {
        "address": 480,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    # --- Appliance Enable/Disable (from German spec 7740782-01) ---
    "ch_enabled": {
        "address": 500,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "dhw_enabled": {
        "address": 501,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cooling_enabled": {
        "address": 502,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cooling_forced": {
        "address": 503,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    # --- Service registers (Tab.50) ---
    "service_required": {
        "address": 512,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "service_notification": {
        "address": 513,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "hours_producing_since_service": {
        "address": 514,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 2,  # resolution: 2 hours
    },
    "hours_since_service": {
        "address": 515,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 2,  # resolution: 2 hours
    },
    "starts_since_service": {
        "address": 516,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    # --- Error registers (Tab.51-53) ---
    "current_generic_error_code": {
        "address": 530,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "error_present": {
        "address": 531,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "devices_connected": {
        "address": 128,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    # Per-board error codes (boards 1-4, most common setup)
    "board1_error_code": {
        "address": 532,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "board1_error_severity": {
        "address": 533,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "board2_error_code": {
        "address": 534,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "board2_error_severity": {
        "address": 535,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "board5_error_code": {
        "address": 540,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "board5_error_severity": {
        "address": 541,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "board6_error_code": {
        "address": 542,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "board6_error_severity": {
        "address": 543,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "board7_error_code": {
        "address": 544,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "board7_error_severity": {
        "address": 545,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "board8_error_code": {
        "address": 546,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "board8_error_severity": {
        "address": 547,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "board9_error_code": {
        "address": 548,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "board9_error_severity": {
        "address": 549,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "board10_error_code": {
        "address": 550,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "board10_error_severity": {
        "address": 551,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "buffer_tank_temperature_bottom": {
        "address": 7600,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "buffer_tank_temperature_top": {
        "address": 7601,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "buffer_tank_pump_state": {
        "address": 7602,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "buffer_tank_mode": {
        "address": 7603,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "board3_error_code": {
        "address": 536,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "board3_error_severity": {
        "address": 537,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "board4_error_code": {
        "address": 538,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "board4_error_severity": {
        "address": 539,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    # --- Appliance Measurements (Tab.15 / GTW-08 spec) ---
    "boiler_alarm_code": {
        "address": 390,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": 1,
    },
    "internal_heat_demand_power": {
        "address": 416,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 0.01,
    },
    "internal_heat_demand_temperature_setpoint": {
        "address": 417,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 0.01,
    },
    "internal_heat_demand_type": {
        "address": 418,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "condenser_pump_speed": {
        "address": 453,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 0.001,
    },
    "condenser_pump_hours": {
        "address": 454,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "outdoor_unit_operation_mode": {
        "address": 457,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "odu_current": {
        "address": 456,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 0.1,
    },
    "system_flow_temperature_setpoint": {
        "address": 458,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 0.01,
    },
    # --- Appliance Control (Tab.15 / GTW-08 spec) ---
    "hybrid_mode_selected": {
        "address": 464,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "hybrid_electricity_cost_high_tariff": {
        "address": 465,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
        "sentinel_values": [0x00FF],
    },
    "hybrid_electricity_cost_low_tariff": {
        "address": 466,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
        "sentinel_values": [0x00FF],
    },
    "fossil_energy_cost": {
        "address": 467,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
        "sentinel_values": [0x00FF],
    },
    "electrical_co2_emission_heating_mode": {
        "address": 468,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "electrical_co2_emission_dhw_mode": {
        "address": 469,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "gas_or_oil_co2_emission": {
        "address": 470,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
        "sentinel_values": [0x00FF],
    },
    "boiler_efficiency": {
        "address": 471,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 0.01,
        "sentinel_values": [0x00FF],
    },
    "cop_threshold_primary_energy": {
        "address": 472,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 0.01,
    },
    "blocking_input_1_contact": {
        "address": 473,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "blocking_input_2_contact": {
        "address": 474,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "blocking_input_2_setting": {
        "address": 475,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "function_blocking_input": {
        "address": 476,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "dhw_min_heating_time": {
        "address": 477,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "dhw_max_production_time": {
        "address": 478,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    # --- Appliance Measurements (Tab.15 / GTW-08 spec) ---
    "heat_pump_defrost": {
        "address": 481,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    # --- Appliance Control (Tab.15 / GTW-08 spec) ---
    "backup_type": {
        "address": 482,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    # --- Appliance Measurements (Tab.15 / GTW-08 spec) ---
    "actual_relative_power_produced": {
        "address": 483,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 0.01,
    },
    # --- Appliance Control (Tab.15 / GTW-08 spec) ---
    "hybrid_electricity_cost_high_tariff_accurate": {
        "address": 484,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint16",
        "scale": 0.01,
    },
    "hybrid_electricity_cost_low_tariff_accurate": {
        "address": 485,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint16",
        "scale": 0.01,
    },
    "fossil_energy_cost_accurate": {
        "address": 486,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint16",
        "scale": 0.01,
    },
    "outside_temperature_level_backup_blocked": {
        "address": 487,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "int16",
        "scale": 0.01,
    },
    "next_generator_start_delay": {
        "address": 488,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint16",
        "scale": 1,
    },
    "minimum_outside_temperature_heat_pump_stopped": {
        "address": 489,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "int16",
        "scale": 0.01,
    },
    "heat_pump_silent_mode": {
        "address": 490,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "low_noise_start_time": {
        "address": 491,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
        "writable": True,
    },
    "low_noise_stop_time": {
        "address": 492,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
        "writable": True,
    },
    # --- Appliance Measurements (Tab.15 / GTW-08 spec) ---
    "total_pump_starts": {
        "address": 493,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    # --- Cascade (Tab.110 / GTW-08 spec) ---
    "cascade_producer_active_number": {
        "address": 7100,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_number_of_producers": {
        "address": 7102,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_number_of_stages_available": {
        "address": 7103,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_number_of_stages_required": {
        "address": 7104,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_power_request_power": {
        "address": 7105,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_power_request_temperature_setpoint": {
        "address": 7106,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "cascade_power_request_heat_demand_type": {
        "address": 7107,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_system_power_setpoint_power": {
        "address": 7108,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_system_power_setpoint_temperature_setpoint": {
        "address": 7109,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "cascade_system_power_setpoint_heat_demand_type": {
        "address": 7110,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_1_power_output": {
        "address": 7111,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_1_flow_temperature": {
        "address": 7112,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "cascade_appliance_1_status": {
        "address": 7113,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_1_special_request": {
        "address": 7114,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_3_power_output": {
        "address": 7115,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_3_flow_temperature": {
        "address": 7116,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "cascade_appliance_3_status": {
        "address": 7117,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_3_special_request": {
        "address": 7118,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_4_power_output": {
        "address": 7119,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_4_flow_temperature": {
        "address": 7120,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "cascade_appliance_4_status": {
        "address": 7121,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_4_special_request": {
        "address": 7122,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_5_power_output": {
        "address": 7123,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_5_flow_temperature": {
        "address": 7124,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "cascade_appliance_5_status": {
        "address": 7125,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_5_special_request": {
        "address": 7126,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_6_power_output": {
        "address": 7127,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_6_flow_temperature": {
        "address": 7128,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "cascade_appliance_6_status": {
        "address": 7129,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_6_special_request": {
        "address": 7130,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_7_power_output": {
        "address": 7131,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_7_flow_temperature": {
        "address": 7132,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "cascade_appliance_7_status": {
        "address": 7133,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_7_special_request": {
        "address": 7134,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_8_power_output": {
        "address": 7135,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_8_flow_temperature": {
        "address": 7136,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "cascade_appliance_8_status": {
        "address": 7137,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_8_special_request": {
        "address": 7138,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_9_power_output": {
        "address": 7139,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_9_flow_temperature": {
        "address": 7140,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "cascade_appliance_9_status": {
        "address": 7141,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_9_special_request": {
        "address": 7142,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_appliance_10_power_output": {
        "address": 7143,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint8",
        "scale": 1,
    },
    "cascade_appliance_10_flow_temperature": {
        "address": 7144,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "cascade_appliance_10_status": {
        "address": 7145,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint8",
        "scale": 1,
    },
    "cascade_appliance_10_special_request": {
        "address": 7146,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint8",
        "scale": 1,
    },
    "cascade_requested_power_heat_demand": {
        "address": 7151,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 0.1,
    },
    "cascade_requested_power_percentage": {
        "address": 7155,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": 0.1,
    },
    "cascade_time_to_start_next_stage": {
        "address": 7156,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_primary_pump_relay_active": {
        "address": 7157,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "enum8",
        "scale": 1,
    },
    "cascade_secondary_pump_relay_active": {
        "address": 7158,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "enum8",
        "scale": 1,
    },
    "cascade_system_state": {
        "address": 7159,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "enum8",
        "scale": 1,
    },
    "cascade_operating_hours_heating": {
        "address": 7160,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "cascade_operating_hours_dhw": {
        "address": 7162,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "cascade_llh_return_temperature": {
        "address": 7164,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "cascade_primary_llh_smart_pump_status": {
        "address": 7165,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint8",
        "scale": 1,
    },
    "cascade_primary_pump_control_output": {
        "address": 7166,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 0.1,
    },
    "cascade_secondary_pump_control_output": {
        "address": 7167,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 0.1,
    },
    "cascade_llh_flow_temperature": {
        "address": 7168,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "cascade_appliances_needed_for_heat_demand": {
        "address": 7207,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint8",
        "scale": 1,
    },
    "cascade_temporary_permutation_order": {
        "address": 7208,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint8",
        "scale": 1,
    },
    "cascade_s_bus_producers_status": {
        "address": 7209,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_s_bus_producers_generic_error_code": {
        "address": 7210,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint8",
        "scale": 1,
    },
    "cascade_em068_error_priority_brand_matrix": {
        "address": 7211,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "cascade_appliance_flow_temperature": {
        "address": 7213,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "cascade_appliance_return_temperature": {
        "address": 7214,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "cascade_appliance_heat_exchanger_temperature": {
        "address": 7215,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "cascade_appliance_flue_gas_temperature": {
        "address": 7216,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": 0.1,
    },
    "cascade_appliance_service_notification": {
        "address": 7217,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "enum8",
        "scale": 1,
    },
    "cascade_appliance_water_pressure": {
        "address": 7218,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint8",
        "scale": 0.1,
    },
    "cascade_appliance_second_return_temperature": {
        "address": 7219,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },
    "cascade_appliance_current_pump_speed": {
        "address": 7220,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 0.001,
    },
    "cascade_appliance_actual_relative_power": {
        "address": 7221,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 0.0001,
    },
    "cascade_appliance_total_burner_hours": {
        "address": 7222,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "cascade_appliance_dhw_burner_hours": {
        "address": 7224,
        "type": REG_HOLDING,
        "count": 2,
        "data_type": "uint32",
        "scale": 1,
    },
    "cascade_producer_order_node_id": {
        "address": 7226,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint8",
        "scale": 1,
    },
    "cascade_appliance_device_type": {
        "address": 7227,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_outside_temperature_connected": {
        "address": 7153,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "uint16",
        "scale": 1,
    },
    "cascade_outside_temperature_used": {
        "address": 7154,
        "type": REG_HOLDING,
        "count": 1,
        "data_type": "int16",
        "scale": IWR_SCALE_TEMP,
    },

}

_IWR_STATIC_WRITABLE_UPDATES: Final[dict[str, dict[str, Any]]] = {
    "control_power": {
        "writable": True,
        "min": 0,
        "max": 100,
        "step": 1,
        "poll_profile": "normal",
    },
    "control_temperature": {
        "writable": True,
        "min": 0.0,
        "max": 100.0,
        "step": 0.5,
        "poll_profile": "normal",
    },
    "control_algorithm_type": {
        "writable": True,
        "min": 0,
        "max": 3,
        "poll_profile": "normal",
    },
    "control_heat_demand_type": {
        "writable": True,
        "min": 0,
        "max": 8,
        "poll_profile": "normal",
    },
    "control_cooling_temperature": {
        "writable": True,
        "min": 0.0,
        "max": 50.0,
        "step": 0.5,
        "poll_profile": "normal",
    },
    "summer_winter_threshold": {
        "writable": True,
        "min": -20.0,
        "max": 40.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "neutral_band": {
        "writable": True,
        "min": 0.0,
        "max": 20.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "frost_protection_threshold": {
        "writable": True,
        "min": -30.0,
        "max": 20.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "force_summer_mode": {
        "writable": True,
        "min": 0,
        "max": 1,
        "poll_profile": "slow",
    },
    "hybrid_mode_selected": {
        "writable": True,
        "min": 0,
        "max": 3,
        "poll_profile": "slow",
    },
    "hybrid_electricity_cost_high_tariff": {
        "writable": True,
        "min": 0,
        "max": 255,
        "step": 1,
        "poll_profile": "slow",
    },
    "hybrid_electricity_cost_low_tariff": {
        "writable": True,
        "min": 0,
        "max": 255,
        "step": 1,
        "poll_profile": "slow",
    },
    "fossil_energy_cost": {
        "writable": True,
        "min": 0,
        "max": 255,
        "step": 1,
        "poll_profile": "slow",
    },
    "electrical_co2_emission_heating_mode": {
        "writable": True,
        "min": 0,
        "max": 65535,
        "step": 1,
        "poll_profile": "slow",
    },
    "electrical_co2_emission_dhw_mode": {
        "writable": True,
        "min": 0,
        "max": 65535,
        "step": 1,
        "poll_profile": "slow",
    },
    "gas_or_oil_co2_emission": {
        "writable": True,
        "min": 0,
        "max": 65535,
        "step": 1,
        "poll_profile": "slow",
    },
    "boiler_efficiency": {
        "writable": True,
        "min": 0,
        "max": 100,
        "step": 1,
        "poll_profile": "slow",
    },
    "cop_threshold_primary_energy": {
        "writable": True,
        "min": 0,
        "max": 100,
        "step": 0.1,
        "poll_profile": "slow",
    },
    "blocking_input_1_contact": {
        "writable": True,
        "min": 0,
        "max": 1,
        "poll_profile": "slow",
    },
    "blocking_input_2_contact": {
        "writable": True,
        "min": 0,
        "max": 1,
        "poll_profile": "slow",
    },
    "blocking_input_2_setting": {
        "writable": True,
        "min": 0,
        "max": 12,
        "poll_profile": "slow",
    },
    "function_blocking_input": {
        "writable": True,
        "min": 0,
        "max": 12,
        "poll_profile": "slow",
    },
    "dhw_min_heating_time": {
        "writable": True,
        "min": 0,
        "max": 24,
        "step": 1,
        "poll_profile": "slow",
    },
    "dhw_max_production_time": {
        "writable": True,
        "min": 0,
        "max": 24,
        "step": 1,
        "poll_profile": "slow",
    },
    "dhw_eco_comfort_mode": {
        "writable": True,
        "min": 0,
        "max": 1,
        "poll_profile": "normal",
    },
    "backup_type": {
        "writable": True,
        "min": 0,
        "max": 3,
        "poll_profile": "slow",
    },
    "hybrid_electricity_cost_high_tariff_accurate": {
        "writable": True,
        "min": 0,
        "max": 65535,
        "step": 1,
        "poll_profile": "slow",
    },
    "hybrid_electricity_cost_low_tariff_accurate": {
        "writable": True,
        "min": 0,
        "max": 65535,
        "step": 1,
        "poll_profile": "slow",
    },
    "fossil_energy_cost_accurate": {
        "writable": True,
        "min": 0,
        "max": 65535,
        "step": 1,
        "poll_profile": "slow",
    },
    "outside_temperature_level_backup_blocked": {
        "writable": True,
        "min": -30.0,
        "max": 40.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "next_generator_start_delay": {
        "writable": True,
        "min": 0,
        "max": 1440,
        "step": 1,
        "poll_profile": "slow",
    },
    "minimum_outside_temperature_heat_pump_stopped": {
        "writable": True,
        "min": -30.0,
        "max": 40.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "heat_pump_silent_mode": {
        "writable": True,
        "min": 0,
        "max": 5,
        "poll_profile": "normal",
    },
    "low_noise_start_time": {
        "writable": True,
        "min": 0,
        "max": 143,
        "poll_profile": "slow",
    },
    "low_noise_stop_time": {
        "writable": True,
        "min": 0,
        "max": 143,
        "poll_profile": "slow",
    },
    "ch_enabled": {
        "writable": True,
        "min": 0,
        "max": 1,
        "poll_profile": "normal",
    },
    "dhw_enabled": {
        "writable": True,
        "min": 0,
        "max": 1,
        "poll_profile": "normal",
    },
    "cooling_enabled": {
        "writable": True,
        "min": 0,
        "max": 2,
        "poll_profile": "normal",
    },
    "cooling_forced": {
        "writable": True,
        "min": 0,
        "max": 1,
        "poll_profile": "normal",
    },
}

for _register_key, _updates in _IWR_STATIC_WRITABLE_UPDATES.items():
    _IWR_STATIC_REGISTER_MAP[_register_key].update(_updates)

# ===== Static Sensor Definitions =====

_IWR_STATIC_SENSORS: Final = {
    # --- Device Information GTW-08 (from German spec 7740782-01) ---
    "manufacturer_code": {
        "register": "manufacturer_code",
        "translation_key": "manufacturer_code",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:identifier",
    },
    "cascade_producer_active_number": {
        "register": "cascade_producer_active_number",
        "translation_key": "cascade_producer_active_number",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:counter",
    },
    "cascade_number_of_producers": {
        "register": "cascade_number_of_producers",
        "translation_key": "cascade_number_of_producers",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:counter",
    },
    "cascade_number_of_stages_available": {
        "register": "cascade_number_of_stages_available",
        "translation_key": "cascade_number_of_stages_available",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:stairs",
    },
    "cascade_number_of_stages_required": {
        "register": "cascade_number_of_stages_required",
        "translation_key": "cascade_number_of_stages_required",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:stairs-up",
    },
    "cascade_power_request_power": {
        "register": "cascade_power_request_power",
        "translation_key": "cascade_power_request_power",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:gauge",
    },
    "cascade_power_request_temperature_setpoint": {
        "register": "cascade_power_request_temperature_setpoint",
        "translation_key": "cascade_power_request_temperature_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:thermometer",
    },
    "cascade_power_request_heat_demand_type": {
        "register": "cascade_power_request_heat_demand_type",
        "translation_key": "cascade_power_request_heat_demand_type",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:fire-circle",
        "enum_map": "iwr_heat_demand_type",
    },
    "cascade_system_power_setpoint_power": {
        "register": "cascade_system_power_setpoint_power",
        "translation_key": "cascade_system_power_setpoint_power",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:gauge",
    },
    "cascade_system_power_setpoint_temperature_setpoint": {
        "register": "cascade_system_power_setpoint_temperature_setpoint",
        "translation_key": "cascade_system_power_setpoint_temperature_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:thermometer",
    },
    "cascade_system_power_setpoint_heat_demand_type": {
        "register": "cascade_system_power_setpoint_heat_demand_type",
        "translation_key": "cascade_system_power_setpoint_heat_demand_type",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:fire-circle",
        "enum_map": "iwr_heat_demand_type",
    },
    "cascade_appliance_1_power_output": {
        "register": "cascade_appliance_1_power_output",
        "translation_key": "cascade_appliance_1_power_output",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:gauge",
    },
    "cascade_appliance_1_flow_temperature": {
        "register": "cascade_appliance_1_flow_temperature",
        "translation_key": "cascade_appliance_1_flow_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:thermometer",
    },
    "cascade_appliance_1_status": {
        "register": "cascade_appliance_1_status",
        "translation_key": "cascade_appliance_1_status",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:list-status",
    },
    "cascade_appliance_1_special_request": {
        "register": "cascade_appliance_1_special_request",
        "translation_key": "cascade_appliance_1_special_request",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:message-alert-outline",
    },
    "cascade_appliance_3_power_output": {
        "register": "cascade_appliance_3_power_output",
        "translation_key": "cascade_appliance_3_power_output",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:gauge",
    },
    "cascade_appliance_3_flow_temperature": {
        "register": "cascade_appliance_3_flow_temperature",
        "translation_key": "cascade_appliance_3_flow_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:thermometer",
    },
    "cascade_appliance_3_status": {
        "register": "cascade_appliance_3_status",
        "translation_key": "cascade_appliance_3_status",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:list-status",
    },
    "cascade_appliance_3_special_request": {
        "register": "cascade_appliance_3_special_request",
        "translation_key": "cascade_appliance_3_special_request",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:message-alert-outline",
    },
    "cascade_appliance_4_power_output": {
        "register": "cascade_appliance_4_power_output",
        "translation_key": "cascade_appliance_4_power_output",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:gauge",
    },
    "cascade_appliance_4_flow_temperature": {
        "register": "cascade_appliance_4_flow_temperature",
        "translation_key": "cascade_appliance_4_flow_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:thermometer",
    },
    "cascade_appliance_4_status": {
        "register": "cascade_appliance_4_status",
        "translation_key": "cascade_appliance_4_status",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:list-status",
    },
    "cascade_appliance_4_special_request": {
        "register": "cascade_appliance_4_special_request",
        "translation_key": "cascade_appliance_4_special_request",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:message-alert-outline",
    },
    "cascade_appliance_5_power_output": {
        "register": "cascade_appliance_5_power_output",
        "translation_key": "cascade_appliance_5_power_output",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:gauge",
    },
    "cascade_appliance_5_flow_temperature": {
        "register": "cascade_appliance_5_flow_temperature",
        "translation_key": "cascade_appliance_5_flow_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:thermometer",
    },
    "cascade_appliance_5_status": {
        "register": "cascade_appliance_5_status",
        "translation_key": "cascade_appliance_5_status",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:list-status",
    },
    "cascade_appliance_5_special_request": {
        "register": "cascade_appliance_5_special_request",
        "translation_key": "cascade_appliance_5_special_request",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:message-alert-outline",
    },
    "cascade_appliance_6_power_output": {
        "register": "cascade_appliance_6_power_output",
        "translation_key": "cascade_appliance_6_power_output",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:gauge",
    },
    "cascade_appliance_6_flow_temperature": {
        "register": "cascade_appliance_6_flow_temperature",
        "translation_key": "cascade_appliance_6_flow_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:thermometer",
    },
    "cascade_appliance_6_status": {
        "register": "cascade_appliance_6_status",
        "translation_key": "cascade_appliance_6_status",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:list-status",
    },
    "cascade_appliance_6_special_request": {
        "register": "cascade_appliance_6_special_request",
        "translation_key": "cascade_appliance_6_special_request",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:message-alert-outline",
    },
    "cascade_appliance_7_power_output": {
        "register": "cascade_appliance_7_power_output",
        "translation_key": "cascade_appliance_7_power_output",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:gauge",
    },
    "cascade_appliance_7_flow_temperature": {
        "register": "cascade_appliance_7_flow_temperature",
        "translation_key": "cascade_appliance_7_flow_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:thermometer",
    },
    "cascade_appliance_7_status": {
        "register": "cascade_appliance_7_status",
        "translation_key": "cascade_appliance_7_status",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:list-status",
    },
    "cascade_appliance_7_special_request": {
        "register": "cascade_appliance_7_special_request",
        "translation_key": "cascade_appliance_7_special_request",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:message-alert-outline",
    },
    "cascade_appliance_8_power_output": {
        "register": "cascade_appliance_8_power_output",
        "translation_key": "cascade_appliance_8_power_output",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:gauge",
    },
    "cascade_appliance_8_flow_temperature": {
        "register": "cascade_appliance_8_flow_temperature",
        "translation_key": "cascade_appliance_8_flow_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:thermometer",
    },
    "cascade_appliance_8_status": {
        "register": "cascade_appliance_8_status",
        "translation_key": "cascade_appliance_8_status",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:list-status",
    },
    "cascade_appliance_8_special_request": {
        "register": "cascade_appliance_8_special_request",
        "translation_key": "cascade_appliance_8_special_request",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:message-alert-outline",
    },
    "cascade_appliance_9_power_output": {
        "register": "cascade_appliance_9_power_output",
        "translation_key": "cascade_appliance_9_power_output",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:gauge",
    },
    "cascade_appliance_9_flow_temperature": {
        "register": "cascade_appliance_9_flow_temperature",
        "translation_key": "cascade_appliance_9_flow_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:thermometer",
    },
    "cascade_appliance_9_status": {
        "register": "cascade_appliance_9_status",
        "translation_key": "cascade_appliance_9_status",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:list-status",
    },
    "cascade_appliance_9_special_request": {
        "register": "cascade_appliance_9_special_request",
        "translation_key": "cascade_appliance_9_special_request",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:message-alert-outline",
    },
    "cascade_appliance_10_power_output": {
        "register": "cascade_appliance_10_power_output",
        "translation_key": "cascade_appliance_10_power_output",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:gauge",
    },
    "cascade_appliance_10_flow_temperature": {
        "register": "cascade_appliance_10_flow_temperature",
        "translation_key": "cascade_appliance_10_flow_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:thermometer",
    },
    "cascade_appliance_10_status": {
        "register": "cascade_appliance_10_status",
        "translation_key": "cascade_appliance_10_status",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:list-status",
    },
    "cascade_appliance_10_special_request": {
        "register": "cascade_appliance_10_special_request",
        "translation_key": "cascade_appliance_10_special_request",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:message-alert-outline",
    },
    "cascade_requested_power_heat_demand": {
        "register": "cascade_requested_power_heat_demand",
        "translation_key": "cascade_requested_power_heat_demand",
        "device_class": "power",
        "unit": "kW",
        "state_class": "measurement",
        "icon": "mdi:flash",
    },
    "cascade_requested_power_percentage": {
        "register": "cascade_requested_power_percentage",
        "translation_key": "cascade_requested_power_percentage",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:gauge",
    },
    "cascade_time_to_start_next_stage": {
        "register": "cascade_time_to_start_next_stage",
        "translation_key": "cascade_time_to_start_next_stage",
        "device_class": "duration",
        "unit": "min",
        "state_class": "measurement",
        "icon": "mdi:timer-sand",
    },
    "cascade_primary_pump_relay_active": {
        "register": "cascade_primary_pump_relay_active",
        "translation_key": "cascade_primary_pump_relay_active",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:pump",
        "enum_map": "iwr_no_yes",
    },
    "cascade_secondary_pump_relay_active": {
        "register": "cascade_secondary_pump_relay_active",
        "translation_key": "cascade_secondary_pump_relay_active",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:pump",
        "enum_map": "iwr_no_yes",
    },
    "cascade_system_state": {
        "register": "cascade_system_state",
        "translation_key": "cascade_system_state",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:information-outline",
        "enum_map": "iwr_cascade_system_state",
    },
    "cascade_operating_hours_heating": {
        "register": "cascade_operating_hours_heating",
        "translation_key": "cascade_operating_hours_heating",
        "device_class": "duration",
        "unit": "h",
        "state_class": "total_increasing",
        "icon": "mdi:clock-outline",
    },
    "cascade_operating_hours_dhw": {
        "register": "cascade_operating_hours_dhw",
        "translation_key": "cascade_operating_hours_dhw",
        "device_class": "duration",
        "unit": "h",
        "state_class": "total_increasing",
        "icon": "mdi:clock-outline",
    },
    "cascade_llh_return_temperature": {
        "register": "cascade_llh_return_temperature",
        "translation_key": "cascade_llh_return_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
    },
    "cascade_primary_llh_smart_pump_status": {
        "register": "cascade_primary_llh_smart_pump_status",
        "translation_key": "cascade_primary_llh_smart_pump_status",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:pump",
    },
    "cascade_primary_pump_control_output": {
        "register": "cascade_primary_pump_control_output",
        "translation_key": "cascade_primary_pump_control_output",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:pump",
    },
    "cascade_secondary_pump_control_output": {
        "register": "cascade_secondary_pump_control_output",
        "translation_key": "cascade_secondary_pump_control_output",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:pump",
    },
    "cascade_llh_flow_temperature": {
        "register": "cascade_llh_flow_temperature",
        "translation_key": "cascade_llh_flow_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
    },
    "cascade_appliances_needed_for_heat_demand": {
        "register": "cascade_appliances_needed_for_heat_demand",
        "translation_key": "cascade_appliances_needed_for_heat_demand",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:format-list-numbered",
    },
    "cascade_temporary_permutation_order": {
        "register": "cascade_temporary_permutation_order",
        "translation_key": "cascade_temporary_permutation_order",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:swap-horizontal",
    },
    "cascade_s_bus_producers_status": {
        "register": "cascade_s_bus_producers_status",
        "translation_key": "cascade_s_bus_producers_status",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:list-status",
        "enum_map": "iwr_cascade_system_state",
    },
    "cascade_s_bus_producers_generic_error_code": {
        "register": "cascade_s_bus_producers_generic_error_code",
        "translation_key": "cascade_s_bus_producers_generic_error_code",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:alert-circle-outline",
    },
    "cascade_outside_temperature_connected": {
        "register": "cascade_outside_temperature_connected",
        "translation_key": "cascade_outside_temperature_connected",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:thermometer-check",
        "enum_map": "iwr_no_yes",
    },
    "cascade_outside_temperature_used": {
        "register": "cascade_outside_temperature_used",
        "translation_key": "cascade_outside_temperature_used",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:thermometer",
    },
    "cascade_em068_error_priority_brand_matrix": {
        "register": "cascade_em068_error_priority_brand_matrix",
        "translation_key": "cascade_em068_error_priority_brand_matrix",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:table-large",
    },
    "cascade_appliance_flow_temperature": {
        "register": "cascade_appliance_flow_temperature",
        "translation_key": "cascade_appliance_flow_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:thermometer-chevron-up",
    },
    "cascade_appliance_return_temperature": {
        "register": "cascade_appliance_return_temperature",
        "translation_key": "cascade_appliance_return_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:thermometer-chevron-down",
    },
    "cascade_appliance_heat_exchanger_temperature": {
        "register": "cascade_appliance_heat_exchanger_temperature",
        "translation_key": "cascade_appliance_heat_exchanger_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:radiator",
    },
    "cascade_appliance_flue_gas_temperature": {
        "register": "cascade_appliance_flue_gas_temperature",
        "translation_key": "cascade_appliance_flue_gas_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:smoke",
    },
    "cascade_appliance_service_notification": {
        "register": "cascade_appliance_service_notification",
        "translation_key": "cascade_appliance_service_notification",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:wrench",
        "enum_map": "iwr_service_notification",
    },
    "cascade_appliance_water_pressure": {
        "register": "cascade_appliance_water_pressure",
        "translation_key": "cascade_appliance_water_pressure",
        "device_class": "pressure",
        "unit": "bar",
        "state_class": "measurement",
    },
    "cascade_appliance_second_return_temperature": {
        "register": "cascade_appliance_second_return_temperature",
        "translation_key": "cascade_appliance_second_return_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:thermometer-chevron-double-down",
    },
    "cascade_appliance_current_pump_speed": {
        "register": "cascade_appliance_current_pump_speed",
        "translation_key": "cascade_appliance_current_pump_speed",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:pump",
    },
    "cascade_appliance_actual_relative_power": {
        "register": "cascade_appliance_actual_relative_power",
        "translation_key": "cascade_appliance_actual_relative_power",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:gauge",
    },
    "cascade_appliance_total_burner_hours": {
        "register": "cascade_appliance_total_burner_hours",
        "translation_key": "cascade_appliance_total_burner_hours",
        "device_class": "duration",
        "unit": "h",
        "state_class": "total_increasing",
        "icon": "mdi:clock-outline",
    },
    "cascade_appliance_dhw_burner_hours": {
        "register": "cascade_appliance_dhw_burner_hours",
        "translation_key": "cascade_appliance_dhw_burner_hours",
        "device_class": "duration",
        "unit": "h",
        "state_class": "total_increasing",
        "icon": "mdi:clock-outline",
    },
    "cascade_producer_order_node_id": {
        "register": "cascade_producer_order_node_id",
        "translation_key": "cascade_producer_order_node_id",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:format-list-numbered",
    },
    "cascade_appliance_device_type": {
        "register": "cascade_appliance_device_type",
        "translation_key": "cascade_appliance_device_type",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:chip",
        "value_format": "device_type",
        "device_categories": IWR_DEVICE_CATEGORY,
    },
    "gateway_device_type": {
        "register": "gateway_device_type",
        "translation_key": "gateway_device_type",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:chip",
        "value_format": "device_type",
        "device_categories": IWR_DEVICE_CATEGORY,
    },
    # --- Board Discovery Metadata (System Discovery) ---
    "board1_device_type": {
        "register": "board1_device_type",
        "translation_key": "board1_device_type",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:chip",
        "value_format": "device_type",
        "device_categories": IWR_DEVICE_CATEGORY,
    },
    "board1_software_version": {
        "register": "board1_software_version",
        "translation_key": "board1_software_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board1_config_table_version": {
        "register": "board1_config_table_version",
        "translation_key": "board1_config_table_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board1_hardware_version": {
        "register": "board1_hardware_version",
        "translation_key": "board1_hardware_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board1_article_number": {
        "register": "board1_article_number",
        "translation_key": "board1_article_number",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:barcode",
    },
    "board2_device_type": {
        "register": "board2_device_type",
        "translation_key": "board2_device_type",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:chip",
        "value_format": "device_type",
        "device_categories": IWR_DEVICE_CATEGORY,
    },
    "board2_software_version": {
        "register": "board2_software_version",
        "translation_key": "board2_software_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board2_config_table_version": {
        "register": "board2_config_table_version",
        "translation_key": "board2_config_table_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board2_hardware_version": {
        "register": "board2_hardware_version",
        "translation_key": "board2_hardware_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board2_article_number": {
        "register": "board2_article_number",
        "translation_key": "board2_article_number",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:barcode",
    },
    "board3_device_type": {
        "register": "board3_device_type",
        "translation_key": "board3_device_type",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:chip",
        "value_format": "device_type",
        "device_categories": IWR_DEVICE_CATEGORY,
    },
    "board3_software_version": {
        "register": "board3_software_version",
        "translation_key": "board3_software_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board3_config_table_version": {
        "register": "board3_config_table_version",
        "translation_key": "board3_config_table_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board3_hardware_version": {
        "register": "board3_hardware_version",
        "translation_key": "board3_hardware_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board3_article_number": {
        "register": "board3_article_number",
        "translation_key": "board3_article_number",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:barcode",
    },
    "board4_device_type": {
        "register": "board4_device_type",
        "translation_key": "board4_device_type",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:chip",
        "value_format": "device_type",
        "device_categories": IWR_DEVICE_CATEGORY,
    },
    "board4_software_version": {
        "register": "board4_software_version",
        "translation_key": "board4_software_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board4_config_table_version": {
        "register": "board4_config_table_version",
        "translation_key": "board4_config_table_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board4_hardware_version": {
        "register": "board4_hardware_version",
        "translation_key": "board4_hardware_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board4_article_number": {
        "register": "board4_article_number",
        "translation_key": "board4_article_number",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:barcode",
    },
    "board5_device_type": {
        "register": "board5_device_type",
        "translation_key": "board5_device_type",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:chip",
        "value_format": "device_type",
        "device_categories": IWR_DEVICE_CATEGORY,
    },
    "board5_software_version": {
        "register": "board5_software_version",
        "translation_key": "board5_software_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board5_config_table_version": {
        "register": "board5_config_table_version",
        "translation_key": "board5_config_table_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board5_hardware_version": {
        "register": "board5_hardware_version",
        "translation_key": "board5_hardware_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board5_article_number": {
        "register": "board5_article_number",
        "translation_key": "board5_article_number",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:barcode",
    },
    "board6_device_type": {
        "register": "board6_device_type",
        "translation_key": "board6_device_type",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:chip",
        "value_format": "device_type",
        "device_categories": IWR_DEVICE_CATEGORY,
    },
    "board6_software_version": {
        "register": "board6_software_version",
        "translation_key": "board6_software_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board6_config_table_version": {
        "register": "board6_config_table_version",
        "translation_key": "board6_config_table_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board6_hardware_version": {
        "register": "board6_hardware_version",
        "translation_key": "board6_hardware_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board6_article_number": {
        "register": "board6_article_number",
        "translation_key": "board6_article_number",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:barcode",
    },
    "board7_device_type": {
        "register": "board7_device_type",
        "translation_key": "board7_device_type",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:chip",
        "value_format": "device_type",
        "device_categories": IWR_DEVICE_CATEGORY,
    },
    "board7_software_version": {
        "register": "board7_software_version",
        "translation_key": "board7_software_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board7_config_table_version": {
        "register": "board7_config_table_version",
        "translation_key": "board7_config_table_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board7_hardware_version": {
        "register": "board7_hardware_version",
        "translation_key": "board7_hardware_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board7_article_number": {
        "register": "board7_article_number",
        "translation_key": "board7_article_number",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:barcode",
    },
    "board8_device_type": {
        "register": "board8_device_type",
        "translation_key": "board8_device_type",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:chip",
        "value_format": "device_type",
        "device_categories": IWR_DEVICE_CATEGORY,
    },
    "board8_software_version": {
        "register": "board8_software_version",
        "translation_key": "board8_software_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board8_config_table_version": {
        "register": "board8_config_table_version",
        "translation_key": "board8_config_table_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board8_hardware_version": {
        "register": "board8_hardware_version",
        "translation_key": "board8_hardware_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board8_article_number": {
        "register": "board8_article_number",
        "translation_key": "board8_article_number",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:barcode",
    },
    "board9_device_type": {
        "register": "board9_device_type",
        "translation_key": "board9_device_type",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:chip",
        "value_format": "device_type",
        "device_categories": IWR_DEVICE_CATEGORY,
    },
    "board9_software_version": {
        "register": "board9_software_version",
        "translation_key": "board9_software_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board9_config_table_version": {
        "register": "board9_config_table_version",
        "translation_key": "board9_config_table_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board9_hardware_version": {
        "register": "board9_hardware_version",
        "translation_key": "board9_hardware_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board9_article_number": {
        "register": "board9_article_number",
        "translation_key": "board9_article_number",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:barcode",
    },
    "board10_device_type": {
        "register": "board10_device_type",
        "translation_key": "board10_device_type",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:chip",
        "value_format": "device_type",
        "device_categories": IWR_DEVICE_CATEGORY,
    },
    "board10_software_version": {
        "register": "board10_software_version",
        "translation_key": "board10_software_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board10_config_table_version": {
        "register": "board10_config_table_version",
        "translation_key": "board10_config_table_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board10_hardware_version": {
        "register": "board10_hardware_version",
        "translation_key": "board10_hardware_version",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:memory",
    },
    "board10_article_number": {
        "register": "board10_article_number",
        "translation_key": "board10_article_number",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:barcode",
    },
    "appliance_time_sensor": {
        "register": "appliance_time",
        "translation_key": "appliance_time",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:clock-outline",
        "sub_device": SUBDEV_BOILER,
    },
    "low_noise_mode_state_sensor": {
        "register": "low_noise_mode_state",
        "translation_key": "low_noise_mode_state",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:volume-off",
        "enum_map": "iwr_low_noise_mode_state",
        "sub_device": SUBDEV_BOILER,
    },
    # --- Zone Detection (Tab.24) ---
    "zone_count": {
        "register": "zone_count",
        "translation_key": "zone_count",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:counter",
    },
    # --- Zone Count Subtypes (from German spec 7740782-01) ---
    "zones_disabled": {
        "register": "zones_disabled",
        "translation_key": "zones_disabled",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:counter",
    },
    "zones_ch": {
        "register": "zones_ch",
        "translation_key": "zones_ch",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:counter",
    },
    "zones_ch_cooling": {
        "register": "zones_ch_cooling",
        "translation_key": "zones_ch_cooling",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:counter",
    },
    "zones_dhw": {
        "register": "zones_dhw",
        "translation_key": "zones_dhw",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:counter",
    },
    "zones_process_heat": {
        "register": "zones_process_heat",
        "translation_key": "zones_process_heat",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:counter",
    },
    "zones_swimming_pool": {
        "register": "zones_swimming_pool",
        "translation_key": "zones_swimming_pool",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:counter",
    },
    "zones_others": {
        "register": "zones_others",
        "translation_key": "zones_others",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:counter",
    },
    "buffer_tank_active": {
        "register": "buffer_tank_active",
        "translation_key": "buffer_tank_active",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:storage-tank-outline",
        "enum_map": "iwr_no_yes",
    },
    "cascade_role": {
        "register": "cascade_role",
        "translation_key": "cascade_role",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:source-branch",
        "enum_map": "iwr_cascade_role",
    },
    "control_cooling_temperature": {
        "register": "control_cooling_temperature",
        "translation_key": "control_cooling_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:snowflake-thermometer",
        "sub_device": SUBDEV_BOILER,
    },
    # --- Main Appliance Sensors ---
    "system_power": {
        "register": "system_power",
        "translation_key": "system_power",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:gauge",
        "sub_device": SUBDEV_BOILER,
    },
    # --- Received Temperatures from CU (from German spec 7740782-01) ---
    "cu_flow_temperature": {
        "register": "cu_flow_temperature",
        "translation_key": "cu_flow_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "sub_device": SUBDEV_BOILER,
    },
    "cu_return_temperature": {
        "register": "cu_return_temperature",
        "translation_key": "cu_return_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "sub_device": SUBDEV_BOILER,
    },
    "outside_temperature": {
        "register": "outside_temperature",
        "translation_key": "outside_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "sub_device": SUBDEV_BOILER,
    },
    "seasonal_mode": {
        "register": "seasonal_mode",
        "translation_key": "seasonal_mode",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:weather-partly-cloudy",
        "enum_map": "iwr_seasonal_mode",
        "sub_device": SUBDEV_BOILER,
    },
    # --- Appliance Parameters (from German spec 7740782-01) ---
    "summer_winter_threshold": {
        "register": "summer_winter_threshold",
        "translation_key": "summer_winter_threshold",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:thermometer-lines",
        "sub_device": SUBDEV_BOILER,
    },
    "neutral_band": {
        "register": "neutral_band",
        "translation_key": "neutral_band",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:thermometer-lines",
        "sub_device": SUBDEV_BOILER,
    },
    "frost_protection_threshold": {
        "register": "frost_protection_threshold",
        "translation_key": "frost_protection_threshold",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:snowflake-thermometer",
        "sub_device": SUBDEV_BOILER,
    },
    "force_summer_mode": {
        "register": "force_summer_mode",
        "translation_key": "force_summer_mode",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:weather-sunny",
        "enum_map": "iwr_on_off",
        "sub_device": SUBDEV_BOILER,
    },
    "flow_temperature": {
        "register": "flow_temperature",
        "translation_key": "flow_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "sub_device": SUBDEV_BOILER,
    },
    "return_temperature": {
        "register": "return_temperature",
        "translation_key": "return_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "sub_device": SUBDEV_BOILER,
    },
    "exhaust_gas_temperature": {
        "register": "exhaust_gas_temperature",
        "translation_key": "exhaust_gas_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "sub_device": SUBDEV_BOILER,
    },
    "hp_flow_temperature": {
        "register": "hp_flow_temperature",
        "translation_key": "hp_flow_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "sub_device": SUBDEV_BOILER,
    },
    "hp_return_temperature": {
        "register": "hp_return_temperature",
        "translation_key": "hp_return_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "sub_device": SUBDEV_BOILER,
    },
    # --- Internal Setpoints (from German spec 7740782-01) ---
    "internal_dhw_setpoint": {
        "register": "internal_dhw_setpoint",
        "translation_key": "internal_dhw_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:water-thermometer",
        "sub_device": SUBDEV_BOILER,
    },
    "ch_setpoint": {
        "register": "ch_setpoint",
        "translation_key": "ch_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:thermostat",
        "sub_device": SUBDEV_BOILER,
    },
    "cooling_setpoint": {
        "register": "cooling_setpoint",
        "translation_key": "cooling_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:snowflake-thermometer",
        "sub_device": SUBDEV_BOILER,
    },
    "dhw_flow_setpoint": {
        "register": "dhw_flow_setpoint",
        "translation_key": "dhw_flow_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "sub_device": SUBDEV_BOILER,
    },
    "water_pressure": {
        "register": "water_pressure",
        "translation_key": "water_pressure",
        "device_class": "pressure",
        "unit": "bar",
        "state_class": "measurement",
        "sub_device": SUBDEV_BOILER,
    },
    "flow_rate": {
        "register": "flow_rate",
        "translation_key": "flow_rate",
        "device_class": None,
        "unit": "l/min",
        "state_class": "measurement",
        "icon": "mdi:water-pump",
        "sub_device": SUBDEV_BOILER,
    },
    # --- Boiler / appliance monitoring additions (Tab. Boiler) ---
    "boiler_alarm_code": {
        "register": "boiler_alarm_code",
        "translation_key": "boiler_alarm_code",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "sub_device": SUBDEV_BOILER,
    },
    "internal_heat_demand_power": {
        "register": "internal_heat_demand_power",
        "translation_key": "internal_heat_demand_power",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:fire",
        "sub_device": SUBDEV_BOILER,
    },
    "internal_heat_demand_temperature_setpoint": {
        "register": "internal_heat_demand_temperature_setpoint",
        "translation_key": "internal_heat_demand_temperature_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:thermostat",
        "sub_device": SUBDEV_BOILER,
    },
    "internal_heat_demand_type": {
        "register": "internal_heat_demand_type",
        "translation_key": "internal_heat_demand_type",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:fire",
        "enum_map": "iwr_internal_heat_demand_type",
        "sub_device": SUBDEV_BOILER,
    },
    "condenser_pump_speed": {
        "register": "condenser_pump_speed",
        "translation_key": "condenser_pump_speed",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:pump",
        "sub_device": SUBDEV_BOILER,
    },
    "condenser_pump_hours": {
        "register": "condenser_pump_hours",
        "translation_key": "condenser_pump_hours",
        "device_class": "duration",
        "unit": "h",
        "state_class": "total_increasing",
        "icon": "mdi:clock-outline",
        "sub_device": SUBDEV_BOILER,
    },
    "odu_current": {
        "register": "odu_current",
        "translation_key": "odu_current",
        "device_class": "current",
        "unit": "A",
        "state_class": "measurement",
        "icon": "mdi:current-ac-ac",
        "sub_device": SUBDEV_BOILER,
    },
    "outdoor_unit_operation_mode": {
        "register": "outdoor_unit_operation_mode",
        "translation_key": "outdoor_unit_operation_mode",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:hvac",
        "enum_map": "iwr_outdoor_unit_operation_mode",
        "sub_device": SUBDEV_BOILER,
    },
    "system_flow_temperature_setpoint": {
        "register": "system_flow_temperature_setpoint",
        "translation_key": "system_flow_temperature_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:thermometer",
        "sub_device": SUBDEV_BOILER,
    },
    "main_status": {
        "register": "main_status",
        "translation_key": "main_status",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:information-outline",
        "enum_map": "iwr_main_status",
        "sub_device": SUBDEV_BOILER,
    },
    "sub_status": {
        "register": "sub_status",
        "translation_key": "sub_status",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:information-outline",
        "enum_map": "iwr_sub_status",
        "sub_device": SUBDEV_BOILER,
    },
    "relative_power": {
        "register": "relative_power",
        "translation_key": "relative_power",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:gauge",
        "sub_device": SUBDEV_BOILER,
    },
    "power_setpoint": {
        "register": "power_setpoint",
        "translation_key": "power_setpoint",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:gauge",
        "sub_device": SUBDEV_BOILER,
    },
    "ionization_current": {
        "register": "ionization_current",
        "translation_key": "ionization_current",
        "device_class": None,
        "unit": "µA",
        "state_class": "measurement",
        "icon": "mdi:flash",
        "sub_device": SUBDEV_BOILER,
    },
    "pump_speed": {
        "register": "pump_speed",
        "translation_key": "pump_speed",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:pump",
        "sub_device": SUBDEV_BOILER,
    },
    "actual_power": {
        "register": "actual_power",
        "translation_key": "actual_power",
        "device_class": "power",
        "unit": "kW",
        "state_class": "measurement",
        "sub_device": SUBDEV_BOILER,
    },
    "cop": {
        "register": "cop",
        "translation_key": "cop",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:chart-line",
        "sub_device": SUBDEV_BOILER,
    },
    "cop_threshold": {
        "register": "cop_threshold",
        "translation_key": "cop_threshold",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:chart-line",
        "sub_device": SUBDEV_BOILER,
    },
    "hybrid_cop": {
        "register": "hybrid_cop",
        "translation_key": "hybrid_cop",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:chart-line",
        "sub_device": SUBDEV_BOILER,
    },
    "hybrid_cop_threshold": {
        "register": "hybrid_cop_threshold",
        "translation_key": "hybrid_cop_threshold",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:chart-line",
        "sub_device": SUBDEV_BOILER,
    },
    # --- Cascade Flow/Return Temperature (Tab.23) ---
    "cascade_flow_temperature": {
        "register": "cascade_flow_temperature",
        "translation_key": "cascade_flow_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "sub_device": SUBDEV_BOILER,
    },
    "cascade_return_temperature": {
        "register": "cascade_return_temperature",
        "translation_key": "cascade_return_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "sub_device": SUBDEV_BOILER,
    },
    # --- Counters & Energy ---
    "total_starts": {
        "register": "total_starts",
        "translation_key": "total_starts",
        "device_class": None,
        "unit": None,
        "state_class": "total_increasing",
        "icon": "mdi:counter",
        "sub_device": SUBDEV_BOILER,
    },
    "total_operating_hours": {
        "register": "total_operating_hours",
        "translation_key": "total_operating_hours",
        "device_class": "duration",
        "unit": "h",
        "state_class": "total_increasing",
        "icon": "mdi:clock-outline",
        "sub_device": SUBDEV_BOILER,
    },
    "backup1_starts": {
        "register": "backup1_starts",
        "translation_key": "backup1_starts",
        "device_class": None,
        "unit": None,
        "state_class": "total_increasing",
        "icon": "mdi:counter",
        "sub_device": SUBDEV_BOILER,
    },
    "backup1_operating_hours": {
        "register": "backup1_operating_hours",
        "translation_key": "backup1_operating_hours",
        "device_class": "duration",
        "unit": "h",
        "state_class": "total_increasing",
        "icon": "mdi:clock-outline",
        "sub_device": SUBDEV_BOILER,
    },
    "backup2_starts": {
        "register": "backup2_starts",
        "translation_key": "backup2_starts",
        "device_class": None,
        "unit": None,
        "state_class": "total_increasing",
        "icon": "mdi:counter",
        "sub_device": SUBDEV_BOILER,
    },
    "backup2_operating_hours": {
        "register": "backup2_operating_hours",
        "translation_key": "backup2_operating_hours",
        "device_class": "duration",
        "unit": "h",
        "state_class": "total_increasing",
        "icon": "mdi:clock-outline",
        "sub_device": SUBDEV_BOILER,
    },
    "mains_power_hours": {
        "register": "mains_power_hours",
        "translation_key": "mains_power_hours",
        "device_class": "duration",
        "unit": "h",
        "state_class": "total_increasing",
        "icon": "mdi:clock-outline",
        "sub_device": SUBDEV_BOILER,
    },
    # --- Main Controller Monitoring counters (Tab.11) ---
    "main_control_burner_starts": {
        "register": "main_control_burner_starts",
        "translation_key": "main_control_burner_starts",
        "device_class": None,
        "unit": None,
        "state_class": "total_increasing",
        "icon": "mdi:counter",
        "sub_device": SUBDEV_BOILER,
    },
    "main_control_burning_hours": {
        "register": "main_control_burning_hours",
        "translation_key": "main_control_burning_hours",
        "device_class": "duration",
        "unit": "h",
        "state_class": "total_increasing",
        "icon": "mdi:clock-outline",
        "sub_device": SUBDEV_BOILER,
    },
    "main_control_hours_after_service": {
        "register": "main_control_hours_after_service",
        "translation_key": "main_control_hours_after_service",
        "device_class": "duration",
        "unit": "h",
        "state_class": "measurement",
        "icon": "mdi:clock-alert-outline",
        "sub_device": SUBDEV_BOILER,
    },
    "main_control_successful_compressor_starts_after_service": {
        "register": "main_control_successful_compressor_starts_after_service",
        "translation_key": "main_control_successful_compressor_starts_after_service",
        "device_class": None,
        "unit": None,
        "state_class": "total_increasing",
        "icon": "mdi:counter",
        "sub_device": SUBDEV_BOILER,
    },
    "main_control_backup1_starts": {
        "register": "main_control_backup1_starts",
        "translation_key": "main_control_backup1_starts",
        "device_class": None,
        "unit": None,
        "state_class": "total_increasing",
        "icon": "mdi:counter",
        "sub_device": SUBDEV_BOILER,
    },
    "main_control_backup1_hours": {
        "register": "main_control_backup1_hours",
        "translation_key": "main_control_backup1_hours",
        "device_class": "duration",
        "unit": "h",
        "state_class": "total_increasing",
        "icon": "mdi:clock-outline",
        "sub_device": SUBDEV_BOILER,
    },
    "main_control_backup2_starts": {
        "register": "main_control_backup2_starts",
        "translation_key": "main_control_backup2_starts",
        "device_class": None,
        "unit": None,
        "state_class": "total_increasing",
        "icon": "mdi:counter",
        "sub_device": SUBDEV_BOILER,
    },
    "main_control_backup2_hours": {
        "register": "main_control_backup2_hours",
        "translation_key": "main_control_backup2_hours",
        "device_class": "duration",
        "unit": "h",
        "state_class": "total_increasing",
        "icon": "mdi:clock-outline",
        "sub_device": SUBDEV_BOILER,
    },
    "main_control_active_hours": {
        "register": "main_control_active_hours",
        "translation_key": "main_control_active_hours",
        "device_class": "duration",
        "unit": "h",
        "state_class": "total_increasing",
        "icon": "mdi:clock-outline",
        "sub_device": SUBDEV_BOILER,
    },
    "energy_consumed_ch": {
        "register": "energy_consumed_ch",
        "translation_key": "energy_consumed_ch",
        "device_class": "energy",
        "unit": "kWh",
        "state_class": "total_increasing",
        "sub_device": SUBDEV_BOILER,
    },
    "energy_consumed_dhw": {
        "register": "energy_consumed_dhw",
        "translation_key": "energy_consumed_dhw",
        "device_class": "energy",
        "unit": "kWh",
        "state_class": "total_increasing",
        "sub_device": SUBDEV_BOILER,
    },
    "energy_consumed_cooling": {
        "register": "energy_consumed_cooling",
        "translation_key": "energy_consumed_cooling",
        "device_class": "energy",
        "unit": "kWh",
        "state_class": "total_increasing",
        "sub_device": SUBDEV_BOILER,
    },
    "total_energy_consumed": {
        "register": "total_energy_consumed",
        "translation_key": "total_energy_consumed",
        "device_class": "energy",
        "unit": "kWh",
        "state_class": "total_increasing",
        "sub_device": SUBDEV_BOILER,
    },
    "energy_consumed_backup": {
        "register": "energy_consumed_backup",
        "translation_key": "energy_consumed_backup",
        "device_class": "energy",
        "unit": "kWh",
        "state_class": "total_increasing",
        "sub_device": SUBDEV_BOILER,
    },
    "total_thermal_delivered": {
        "register": "total_thermal_delivered",
        "translation_key": "total_thermal_delivered",
        "device_class": "energy",
        "unit": "kWh",
        "state_class": "total_increasing",
        "sub_device": SUBDEV_BOILER,
    },
    "thermal_delivered_ch": {
        "register": "thermal_delivered_ch",
        "translation_key": "thermal_delivered_ch",
        "device_class": "energy",
        "unit": "kWh",
        "state_class": "total_increasing",
        "sub_device": SUBDEV_BOILER,
    },
    "thermal_delivered_dhw": {
        "register": "thermal_delivered_dhw",
        "translation_key": "thermal_delivered_dhw",
        "device_class": "energy",
        "unit": "kWh",
        "state_class": "total_increasing",
        "sub_device": SUBDEV_BOILER,
    },
    "thermal_delivered_cooling": {
        "register": "thermal_delivered_cooling",
        "translation_key": "thermal_delivered_cooling",
        "device_class": "energy",
        "unit": "kWh",
        "state_class": "total_increasing",
        "sub_device": SUBDEV_BOILER,
    },
    "energy_delivered_backup": {
        "register": "energy_delivered_backup",
        "translation_key": "energy_delivered_backup",
        "device_class": "energy",
        "unit": "kWh",
        "state_class": "total_increasing",
        "sub_device": SUBDEV_BOILER,
    },
    "total_pump_starts": {
        "register": "total_pump_starts",
        "translation_key": "total_pump_starts",
        "device_class": None,
        "unit": None,
        "state_class": "total_increasing",
        "icon": "mdi:counter",
        "sub_device": SUBDEV_BOILER,
    },
    "heat_pump_defrost": {
        "register": "heat_pump_defrost",
        "translation_key": "heat_pump_defrost",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:snowflake-alert",
        "enum_map": "iwr_no_yes",
        "sub_device": SUBDEV_BOILER,
    },
    "actual_relative_power_produced": {
        "register": "actual_relative_power_produced",
        "translation_key": "actual_relative_power_produced",
        "device_class": None,
        "unit": "%",
        "state_class": "measurement",
        "icon": "mdi:gauge",
        "sub_device": SUBDEV_BOILER,
    },
    # --- Appliance Enable/Disable (from German spec 7740782-01) ---
    "ch_enabled": {
        "register": "ch_enabled",
        "translation_key": "ch_enabled",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:radiator",
        "enum_map": "iwr_on_off",
        "sub_device": SUBDEV_BOILER,
    },
    "dhw_enabled": {
        "register": "dhw_enabled",
        "translation_key": "dhw_enabled",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:water-boiler",
        "enum_map": "iwr_on_off",
        "sub_device": SUBDEV_BOILER,
    },
    "cooling_enabled": {
        "register": "cooling_enabled",
        "translation_key": "cooling_enabled",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:snowflake",
        "enum_map": "iwr_cooling_enabled",
        "sub_device": SUBDEV_BOILER,
    },
    "cooling_forced": {
        "register": "cooling_forced",
        "translation_key": "cooling_forced",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:snowflake-alert",
        "enum_map": "iwr_on_off",
        "sub_device": SUBDEV_BOILER,
    },
    # --- Service sensors ---
    "service_notification": {
        "register": "service_notification",
        "translation_key": "service_notification",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:wrench",
        "enum_map": "iwr_service_notification",
        "sub_device": SUBDEV_SERVICE,
    },
    "hours_producing_since_service": {
        "register": "hours_producing_since_service",
        "translation_key": "hours_producing_since_service",
        "device_class": "duration",
        "unit": "h",
        "state_class": "total_increasing",
        "icon": "mdi:clock-alert-outline",
        "sub_device": SUBDEV_SERVICE,
    },
    "hours_since_service": {
        "register": "hours_since_service",
        "translation_key": "hours_since_service",
        "device_class": "duration",
        "unit": "h",
        "state_class": "total_increasing",
        "icon": "mdi:clock-alert-outline",
        "sub_device": SUBDEV_SERVICE,
    },
    "starts_since_service": {
        "register": "starts_since_service",
        "translation_key": "starts_since_service",
        "device_class": None,
        "unit": None,
        "state_class": "total_increasing",
        "icon": "mdi:counter",
        "sub_device": SUBDEV_SERVICE,
    },
    # --- Error sensors ---
    "devices_connected": {
        "register": "devices_connected",
        "translation_key": "devices_connected",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:developer-board",
        "sub_device": SUBDEV_SERVICE,
    },
    "appliance_error_priority": {
        "register": "appliance_error_priority",
        "translation_key": "appliance_error_priority",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "enum_map": "iwr_error_severity",
        "sub_device": SUBDEV_SERVICE,
    },
    "current_generic_error_code": {
        "register": "current_generic_error_code",
        "translation_key": "current_generic_error_code",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "sub_device": SUBDEV_SERVICE,
    },
    "board1_error_code": {
        "register": "board1_error_code",
        "translation_key": "board1_error_code",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "sub_device": SUBDEV_SERVICE,
    },
    "board1_error_severity": {
        "register": "board1_error_severity",
        "translation_key": "board1_error_severity",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "enum_map": "iwr_error_severity",
        "sub_device": SUBDEV_SERVICE,
    },
    "board2_error_code": {
        "register": "board2_error_code",
        "translation_key": "board2_error_code",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "sub_device": SUBDEV_SERVICE,
    },
    "board2_error_severity": {
        "register": "board2_error_severity",
        "translation_key": "board2_error_severity",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "enum_map": "iwr_error_severity",
        "sub_device": SUBDEV_SERVICE,
    },
    "board3_error_code": {
        "register": "board3_error_code",
        "translation_key": "board3_error_code",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "sub_device": SUBDEV_SERVICE,
    },
    "board3_error_severity": {
        "register": "board3_error_severity",
        "translation_key": "board3_error_severity",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "enum_map": "iwr_error_severity",
        "sub_device": SUBDEV_SERVICE,
    },
    "board4_error_code": {
        "register": "board4_error_code",
        "translation_key": "board4_error_code",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "sub_device": SUBDEV_SERVICE,
    },
    "board4_error_severity": {
        "register": "board4_error_severity",
        "translation_key": "board4_error_severity",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "enum_map": "iwr_error_severity",
        "sub_device": SUBDEV_SERVICE,
    },
    "board5_error_code": {
        "register": "board5_error_code",
        "translation_key": "board5_error_code",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "sub_device": SUBDEV_SERVICE,
    },
    "board5_error_severity": {
        "register": "board5_error_severity",
        "translation_key": "board5_error_severity",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "enum_map": "iwr_error_severity",
        "sub_device": SUBDEV_SERVICE,
    },
    "board6_error_code": {
        "register": "board6_error_code",
        "translation_key": "board6_error_code",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "sub_device": SUBDEV_SERVICE,
    },
    "board6_error_severity": {
        "register": "board6_error_severity",
        "translation_key": "board6_error_severity",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "enum_map": "iwr_error_severity",
        "sub_device": SUBDEV_SERVICE,
    },
    "board7_error_code": {
        "register": "board7_error_code",
        "translation_key": "board7_error_code",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "sub_device": SUBDEV_SERVICE,
    },
    "board7_error_severity": {
        "register": "board7_error_severity",
        "translation_key": "board7_error_severity",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "enum_map": "iwr_error_severity",
        "sub_device": SUBDEV_SERVICE,
    },
    "board8_error_code": {
        "register": "board8_error_code",
        "translation_key": "board8_error_code",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "sub_device": SUBDEV_SERVICE,
    },
    "board8_error_severity": {
        "register": "board8_error_severity",
        "translation_key": "board8_error_severity",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "enum_map": "iwr_error_severity",
        "sub_device": SUBDEV_SERVICE,
    },
    "board9_error_code": {
        "register": "board9_error_code",
        "translation_key": "board9_error_code",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "sub_device": SUBDEV_SERVICE,
    },
    "board9_error_severity": {
        "register": "board9_error_severity",
        "translation_key": "board9_error_severity",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "enum_map": "iwr_error_severity",
        "sub_device": SUBDEV_SERVICE,
    },
    "board10_error_code": {
        "register": "board10_error_code",
        "translation_key": "board10_error_code",
        "device_class": None,
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "sub_device": SUBDEV_SERVICE,
    },
    "board10_error_severity": {
        "register": "board10_error_severity",
        "translation_key": "board10_error_severity",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:alert-circle-outline",
        "enum_map": "iwr_error_severity",
        "sub_device": SUBDEV_SERVICE,
    },
    "buffer_tank_temperature_bottom": {
        "register": "buffer_tank_temperature_bottom",
        "translation_key": "buffer_tank_temperature_bottom",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:thermometer-chevron-down",
        "sub_device": SUBDEV_BUFFER_TANK,
    },
    "buffer_tank_temperature_top": {
        "register": "buffer_tank_temperature_top",
        "translation_key": "buffer_tank_temperature_top",
        "device_class": "temperature",
        "unit": "°C",
        "state_class": "measurement",
        "icon": "mdi:thermometer-chevron-up",
        "sub_device": SUBDEV_BUFFER_TANK,
    },
    "buffer_tank_pump_state": {
        "register": "buffer_tank_pump_state",
        "translation_key": "buffer_tank_pump_state",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:pump",
        "enum_map": "iwr_on_off",
        "sub_device": SUBDEV_BUFFER_TANK,
    },
    "buffer_tank_mode": {
        "register": "buffer_tank_mode",
        "translation_key": "buffer_tank_mode",
        "device_class": "enum",
        "unit": None,
        "state_class": None,
        "icon": "mdi:storage-tank",
        "enum_map": "iwr_buffer_tank_mode",
        "sub_device": SUBDEV_BUFFER_TANK,
    },
}

# ===== Static Binary Sensor Definitions =====

_IWR_STATIC_BINARY_SENSORS: Final = {
    # --- Bitfield 275: Heat demand ---
    "demand_direct_zones": {
        "register": "demand_direct_zones",
        "translation_key": "demand_direct_zones",
        "device_class": None,
        "icon": "mdi:radiator",
        "sub_device": SUBDEV_BOILER,
    },
    "demand_mixing_circuits": {
        "register": "demand_mixing_circuits",
        "translation_key": "demand_mixing_circuits",
        "device_class": None,
        "icon": "mdi:valve",
        "sub_device": SUBDEV_BOILER,
    },
    "demand_valves_open_safety": {
        "register": "demand_valves_open_safety",
        "translation_key": "demand_valves_open_safety",
        "device_class": None,
        "icon": "mdi:valve-open",
        "sub_device": SUBDEV_BOILER,
    },
    "demand_manual_heat": {
        "register": "demand_manual_heat",
        "translation_key": "demand_manual_heat",
        "device_class": None,
        "icon": "mdi:hand-back-right",
        "sub_device": SUBDEV_BOILER,
    },
    "demand_cooling_allowed": {
        "register": "demand_cooling_allowed",
        "translation_key": "demand_cooling_allowed",
        "device_class": None,
        "icon": "mdi:snowflake",
        "sub_device": SUBDEV_BOILER,
    },
    "demand_dhw_allowed": {
        "register": "demand_dhw_allowed",
        "translation_key": "demand_dhw_allowed",
        "device_class": None,
        "icon": "mdi:water-boiler",
        "sub_device": SUBDEV_BOILER,
    },
    "demand_heat_engine_active": {
        "register": "demand_heat_engine_active",
        "translation_key": "demand_heat_engine_active",
        "device_class": "running",
        "sub_device": SUBDEV_BOILER,
    },
    # --- Bitfield 276: Special status ---
    "special_status_shutdown": {
        "register": "special_status_shutdown",
        "translation_key": "shutdown",
        "device_class": None,
        "icon": "mdi:power",
        "sub_device": SUBDEV_BOILER,
    },
    "special_status_heating": {
        "register": "special_status_heating",
        "translation_key": "heating_mode",
        "device_class": "heat",
        "sub_device": SUBDEV_BOILER,
    },
    "special_status_cooling": {
        "register": "special_status_cooling",
        "translation_key": "cooling_active",
        "device_class": "cold",
        "sub_device": SUBDEV_BOILER,
    },
    "special_status_screed_drying": {
        "register": "special_status_screed_drying",
        "translation_key": "screed_drying",
        "device_class": None,
        "icon": "mdi:floor-plan",
        "sub_device": SUBDEV_BOILER,
    },
    "special_status_electric": {
        "register": "special_status_electric",
        "translation_key": "electric_on",
        "device_class": "power",
        "sub_device": SUBDEV_BOILER,
    },
    "special_status_frost_protection": {
        "register": "special_status_frost_protection",
        "translation_key": "frost_protection",
        "device_class": "cold",
        "sub_device": SUBDEV_BOILER,
    },
    "special_status_summer_winter": {
        "register": "special_status_summer_winter",
        "translation_key": "summer_winter",
        "device_class": None,
        "icon": "mdi:weather-partly-cloudy",
        "sub_device": SUBDEV_BOILER,
    },
    "special_status_summer_neutral_band": {
        "register": "special_status_summer_neutral_band",
        "translation_key": "summer_neutral",
        "device_class": None,
        "icon": "mdi:weather-partly-cloudy",
        "sub_device": SUBDEV_BOILER,
    },
    # --- Bitfield 279: Output status 1 ---
    "status_flame_on": {
        "register": "status_flame_on",
        "translation_key": "status_flame_on",
        "device_class": None,
        "icon": "mdi:fire",
        "sub_device": SUBDEV_BOILER,
    },
    "status_heat_pump_on": {
        "register": "status_heat_pump_on",
        "translation_key": "status_heat_pump_on",
        "device_class": "running",
        "sub_device": SUBDEV_BOILER,
    },
    "status_backup1_on": {
        "register": "status_backup1_on",
        "translation_key": "status_backup1_on",
        "device_class": "running",
        "sub_device": SUBDEV_BOILER,
    },
    "status_backup2_on": {
        "register": "status_backup2_on",
        "translation_key": "status_backup2_on",
        "device_class": "running",
        "sub_device": SUBDEV_BOILER,
    },
    "status_dhw_backup_on": {
        "register": "status_dhw_backup_on",
        "translation_key": "status_dhw_backup_on",
        "device_class": "running",
        "sub_device": SUBDEV_BOILER,
    },
    "status_service_required": {
        "register": "status_service_required",
        "translation_key": "status_service_required",
        "device_class": "problem",
        "sub_device": SUBDEV_SERVICE,
    },
    "status_power_down_needed": {
        "register": "status_power_down_needed",
        "translation_key": "status_power_down_needed",
        "device_class": "problem",
        "sub_device": SUBDEV_SERVICE,
    },
    "status_water_pressure_low": {
        "register": "status_water_pressure_low",
        "translation_key": "status_water_pressure_low",
        "device_class": "problem",
        "sub_device": SUBDEV_SERVICE,
    },
    "status_bitfields_number_1": {
        "register": "status_bitfields_number_1",
        "translation_key": "status_bitfields_number_1",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:counter",
        "sub_device": SUBDEV_SERVICE,
    },
    "status_bitfields_number_2": {
        "register": "status_bitfields_number_2",
        "translation_key": "status_bitfields_number_2",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:counter",
        "sub_device": SUBDEV_SERVICE,
    },
    "status_bitfields_number_3": {
        "register": "status_bitfields_number_3",
        "translation_key": "status_bitfields_number_3",
        "device_class": None,
        "unit": None,
        "state_class": "measurement",
        "icon": "mdi:counter",
        "sub_device": SUBDEV_SERVICE,
    },
    # --- Bitfield 280: Output status 2 ---
    "output_pump": {
        "register": "output_pump",
        "translation_key": "output_pump",
        "device_class": "running",
        "sub_device": SUBDEV_BOILER,
    },
    "output_3way_valve_open": {
        "register": "output_3way_valve_open",
        "translation_key": "output_3way_valve_open",
        "device_class": None,
        "icon": "mdi:valve-open",
        "sub_device": SUBDEV_BOILER,
    },
    "output_3way_valve": {
        "register": "output_3way_valve",
        "translation_key": "output_3way_valve",
        "device_class": None,
        "icon": "mdi:valve",
        "sub_device": SUBDEV_BOILER,
    },
    "output_3way_valve_closed": {
        "register": "output_3way_valve_closed",
        "translation_key": "output_3way_valve_closed",
        "device_class": None,
        "icon": "mdi:valve-closed",
        "sub_device": SUBDEV_BOILER,
    },
    "output_dhw_active": {
        "register": "output_dhw_active",
        "translation_key": "output_dhw_active",
        "device_class": "running",
        "sub_device": SUBDEV_BOILER,
    },
    "output_ch_active": {
        "register": "output_ch_active",
        "translation_key": "output_ch_active",
        "device_class": "running",
        "sub_device": SUBDEV_BOILER,
    },
    "output_cooling_active": {
        "register": "output_cooling_active",
        "translation_key": "output_cooling_active",
        "device_class": "running",
        "sub_device": SUBDEV_BOILER,
    },
    # --- Service / Error binary sensors ---
    "service_required": {
        "register": "service_required",
        "translation_key": "service_required",
        "device_class": "problem",
        "sub_device": SUBDEV_SERVICE,
    },
    "error_present": {
        "register": "error_present",
        "translation_key": "error_present",
        "device_class": "problem",
        "sub_device": SUBDEV_SERVICE,
    },
}


# ===== Dynamic Zone Generation =====


def _zone_addr(base: int, zone_idx: int) -> int:
    """Compute zone register address. base is zone-1 address, zone_idx is 0-based."""
    return base + ZONE_ADDR_OFFSET * zone_idx


_ZONE_WRITABLE_REGISTER_UPDATES: Final[dict[str, dict[str, Any]]] = {
    "control_mode": {"writable": True, "min": 0, "max": 2, "poll_profile": "normal"},
    "comfort_setpoint_1": {
        "writable": True,
        "min": 5.0,
        "max": 30.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "comfort_setpoint_2": {
        "writable": True,
        "min": 5.0,
        "max": 30.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "comfort_setpoint_3": {
        "writable": True,
        "min": 5.0,
        "max": 30.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "comfort_setpoint_4": {
        "writable": True,
        "min": 5.0,
        "max": 30.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "comfort_setpoint_5": {
        "writable": True,
        "min": 5.0,
        "max": 30.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "night_setback": {
        "writable": True,
        "min": 5.0,
        "max": 30.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "cooling_room_setpoint_1": {
        "writable": True,
        "min": 10.0,
        "max": 35.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "cooling_room_setpoint_2": {
        "writable": True,
        "min": 10.0,
        "max": 35.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "cooling_room_setpoint_3": {
        "writable": True,
        "min": 10.0,
        "max": 35.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "cooling_room_setpoint_4": {
        "writable": True,
        "min": 10.0,
        "max": 35.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "cooling_room_setpoint_5": {
        "writable": True,
        "min": 10.0,
        "max": 35.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "cooling_night_setback": {
        "writable": True,
        "min": 10.0,
        "max": 35.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "holiday_setpoint": {
        "writable": True,
        "min": 5.0,
        "max": 30.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "temporary_setpoint": {
        "writable": True,
        "min": 5.0,
        "max": 30.0,
        "step": 0.5,
        "poll_profile": "normal",
    },
    "room_setpoint_manual": {
        "writable": True,
        "min": 5.0,
        "max": 30.0,
        "step": 0.5,
        "poll_profile": "normal",
    },
    "dhw_comfort_setpoint": {
        "writable": True,
        "min": 10.0,
        "max": 80.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "dhw_reduced_setpoint": {
        "writable": True,
        "min": 10.0,
        "max": 80.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "dhw_holiday_setpoint": {
        "writable": True,
        "min": 10.0,
        "max": 80.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "dhw_antilegionella_setpoint": {
        "writable": True,
        "min": 10.0,
        "max": 80.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "swimming_pool_setpoint": {
        "writable": True,
        "min": 5.0,
        "max": 40.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "process_heat_setpoint": {
        "writable": True,
        "min": 0.0,
        "max": 90.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "heating_control_strategy": {
        "writable": True,
        "min": 0,
        "max": 3,
        "poll_profile": "slow",
    },
    "max_flow_setpoint": {
        "writable": True,
        "min": 0.0,
        "max": 90.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "cooling_mixing_setpoint": {
        "writable": True,
        "min": 0.0,
        "max": 35.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "heating_curve_footpoint_night": {
        "writable": True,
        "min": 5.0,
        "max": 30.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "max_preheat_time": {
        "writable": True,
        "min": 0,
        "max": 600,
        "step": 1,
        "poll_profile": "slow",
    },
    "mixing_valve_shift": {
        "writable": True,
        "min": -20.0,
        "max": 20.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "mixing_valve_bandwidth": {
        "writable": True,
        "min": 0.0,
        "max": 40.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "dhw_hysteresis": {
        "writable": True,
        "min": 0.5,
        "max": 20.0,
        "step": 0.1,
        "poll_profile": "slow",
    },
    "dhw_calorifier_offset": {
        "writable": True,
        "min": 0.0,
        "max": 30.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "dhw_calorifier_raise": {
        "writable": True,
        "min": 0.0,
        "max": 30.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "process_heat_hysteresis": {
        "writable": True,
        "min": 0.5,
        "max": 20.0,
        "step": 0.1,
        "poll_profile": "slow",
    },
    "process_heat_offset": {
        "writable": True,
        "min": 0.0,
        "max": 30.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "process_heat_calorifier_raise": {
        "writable": True,
        "min": 0.0,
        "max": 30.0,
        "step": 0.5,
        "poll_profile": "slow",
    },
    "dhw_calorifier_hysteresis": {
        "writable": True,
        "min": 0.5,
        "max": 20.0,
        "step": 0.1,
        "poll_profile": "slow",
    },
    "pump_post_run": {
        "writable": True,
        "min": 0,
        "max": 600,
        "step": 1,
        "poll_profile": "slow",
    },
    "time_program_selected": {
        "writable": True,
        "min": 0,
        "max": 2,
        "poll_profile": "slow",
    },
    "room_temp_measured": {
        "writable": True,
        "min": -30.0,
        "max": 50.0,
        "step": 0.1,
        "poll_profile": "normal",
    },
}


def _build_zone_registers(zones: list[int]) -> dict[str, Any]:
    """Generate register map entries for the given zone numbers (1-based)."""
    registers: dict[str, Any] = {}
    for zn in zones:
        z = zn - 1  # 0-based index for address lookup
        prefix = f"zone{zn}"

        # CM040 - Zone flow temperature (INT16, 0.01°C)
        registers[f"{prefix}_flow_temp"] = {
            "address": ZONE_ADDRESSES["CM040"][z],
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "int16",
            "scale": IWR_SCALE_TEMP,
        }
        # CM070 - Zone flow temperature setpoint (UINT16, 0.01°C)
        registers[f"{prefix}_flow_setpoint"] = {
            "address": ZONE_ADDRESSES["CM070"][z],
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_TEMP,
        }
        # CM190 - Room temperature setpoint (INT16, 0.1°C)
        registers[f"{prefix}_room_setpoint"] = {
            "address": ZONE_ADDRESSES["CM190"][z],
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "int16",
            "scale": IWR_SCALE_ROOM_TEMP,
        }
        # CM130 - Current zone activity (ENUM8)
        registers[f"{prefix}_activity"] = {
            "address": ZONE_ADDRESSES["CM130"][z],
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": 1,
        }
        # CM120 - Zone operating mode (ENUM8)
        registers[f"{prefix}_operating_mode"] = {
            "address": ZONE_ADDRESSES["CM120"][z],
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": 1,
        }
        # CM050 - Zone pump status (UINT8, 0/1)
        registers[f"{prefix}_pump"] = {
            "address": ZONE_ADDRESSES["CM050"][z],
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "bool",
        }
        # CM010 - Zone flow measurement active (UINT8, 0/1)
        registers[f"{prefix}_flow_measurement"] = {
            "address": ZONE_ADDRESSES["CM010"][z],
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "bool",
        }
        # CC001 - Pump operating hours (UINT32)
        registers[f"{prefix}_pump_hours"] = {
            "address": ZONE_ADDRESSES["CC001"][z],
            "type": REG_HOLDING,
            "count": 2,
            "data_type": "uint32",
            "scale": 1,
        }
        # CC010 - Pump starts (UINT32)
        registers[f"{prefix}_pump_starts"] = {
            "address": ZONE_ADDRESSES["CC010"][z],
            "type": REG_HOLDING,
            "count": 2,
            "data_type": "uint32",
            "scale": 1,
        }
        # CP02X - Zone function type (ENUM8, Tab.25/26)
        registers[f"{prefix}_function"] = {
            "address": ZONE_ADDRESSES["CP02X"][z],
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": 1,
        }
        # DEV - Zone device type (UINT16 as 0xZZYY, Tab.25/26)
        registers[f"{prefix}_device_type"] = {
            "address": ZONE_ADDRESSES["DEV"][z],
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": 1,
        }
        # CP32X - Zone control mode (ENUM8, Tab.36/42, R/W)
        registers[f"{prefix}_control_mode"] = {
            "address": ZONE_ADDRESSES["CP32X"][z],
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": 1,
            "writable": True,
            "min": 0,
            "max": 2,
        }
        # CP01X - Zone fixed flow setpoint (UINT16, 0.01°C, Tab.37)
        registers[f"{prefix}_fixed_flow_setpoint"] = {
            "address": ZONE_ADDRESSES["CP01X"][z],
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_TEMP,
        }
        # CP20X - Zone room temp setpoint manual (UINT16, 0.1°C, Tab.43, R/W)
        registers[f"{prefix}_room_setpoint_manual"] = {
            "address": ZONE_ADDRESSES["CP20X"][z],
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_ROOM_TEMP,
            "writable": True,
            "min": 5.0,
            "max": 30.0,
            "step": 0.5,
        }
        # CP23X - Heating curve gradient (UINT8, resolution 0.1, Tab.39)
        registers[f"{prefix}_heating_curve_gradient"] = {
            "address": ZONE_ADDRESSES["CP23X"][z],
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": 0.1,
            **({"sentinel_values": [0x00FF]} if zn == 2 else {}),
        }
        # CP21X - Heating curve footpoint (UINT16, 0.1°C, Tab.40)
        registers[f"{prefix}_heating_curve_footpoint"] = {
            "address": ZONE_ADDRESSES["CP21X"][z],
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_ROOM_TEMP,
        }

        # ===== New zone registers from German spec 7740782-01 =====

        # 640 - Zone type (ENUM8)
        registers[f"{prefix}_zone_type"] = {
            "address": _zone_addr(640, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": 1,
        }
        # 650-654 - Room comfort setpoints 1-5 (UINT16, 0.1°C)
        for sp in range(1, 6):
            registers[f"{prefix}_comfort_setpoint_{sp}"] = {
                "address": _zone_addr(649 + sp, z),
                "type": REG_HOLDING,
                "count": 1,
                "data_type": "uint16",
                "scale": IWR_SCALE_ROOM_TEMP,
            }
        # 655 - Night setback setpoint (UINT16, 0.1°C)
        registers[f"{prefix}_night_setback"] = {
            "address": _zone_addr(655, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_ROOM_TEMP,
        }
        # 656-660 - Room cooling setpoints 1-5 (UINT16, 0.1°C)
        for sp in range(1, 6):
            registers[f"{prefix}_cooling_room_setpoint_{sp}"] = {
                "address": _zone_addr(655 + sp, z),
                "type": REG_HOLDING,
                "count": 1,
                "data_type": "uint16",
                "scale": IWR_SCALE_ROOM_TEMP,
            }
        # 661 - Cooling night setback (UINT16, 0.1°C)
        registers[f"{prefix}_cooling_night_setback"] = {
            "address": _zone_addr(661, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_ROOM_TEMP,
        }
        # 662 - Holiday room setpoint (UINT16, 0.1°C)
        registers[f"{prefix}_holiday_setpoint"] = {
            "address": _zone_addr(662, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_ROOM_TEMP,
        }
        # 663 - Temporary room setpoint (UINT16, 0.1°C)
        registers[f"{prefix}_temporary_setpoint"] = {
            "address": _zone_addr(663, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_ROOM_TEMP,
        }
        # 665 - DHW comfort setpoint (UINT16, 0.01°C, R/W)
        registers[f"{prefix}_dhw_comfort_setpoint"] = {
            "address": _zone_addr(665, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_TEMP,
            "writable": True,
            "min": 10.0,
            "max": 80.0,
            "step": 0.5,
        }
        # 666 - DHW reduced setpoint (UINT16, 0.01°C, R/W)
        registers[f"{prefix}_dhw_reduced_setpoint"] = {
            "address": _zone_addr(666, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_TEMP,
            "writable": True,
            "min": 10.0,
            "max": 80.0,
            "step": 0.5,
        }
        # 667 - DHW holiday setpoint (UINT16, 0.01°C, R/W)
        registers[f"{prefix}_dhw_holiday_setpoint"] = {
            "address": _zone_addr(667, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_TEMP,
            "writable": True,
            "min": 10.0,
            "max": 80.0,
            "step": 0.5,
        }
        # 668 - DHW anti-legionella setpoint (UINT16, 0.01°C, R/W)
        registers[f"{prefix}_dhw_antilegionella_setpoint"] = {
            "address": _zone_addr(668, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_TEMP,
            "writable": True,
            "min": 10.0,
            "max": 80.0,
            "step": 0.5,
        }
        # 669 - Swimming pool setpoint (UINT16, 0.01°C)
        registers[f"{prefix}_swimming_pool_setpoint"] = {
            "address": _zone_addr(669, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_TEMP,
        }
        # 670 - Process heat setpoint (UINT16, 0.01°C)
        registers[f"{prefix}_process_heat_setpoint"] = {
            "address": _zone_addr(670, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_TEMP,
        }
        # 671 - Heating control strategy (ENUM8)
        registers[f"{prefix}_heating_control_strategy"] = {
            "address": _zone_addr(671, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": 1,
        }
        # 672 - Max flow temperature setpoint (UINT16, 0.01°C)
        registers[f"{prefix}_max_flow_setpoint"] = {
            "address": _zone_addr(672, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_TEMP,
        }
        # 673 - Cooling mixing circuit flow setpoint (UINT16, 0.01°C)
        registers[f"{prefix}_cooling_mixing_setpoint"] = {
            "address": _zone_addr(673, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_TEMP,
        }
        # 676 - Heating curve footpoint night (UINT16, 0.1°C)
        registers[f"{prefix}_heating_curve_footpoint_night"] = {
            "address": _zone_addr(676, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_ROOM_TEMP,
        }
        # 677 - Max preheat time (UINT16, minutes)
        registers[f"{prefix}_max_preheat_time"] = {
            "address": _zone_addr(677, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": 1,
        }
        # 678 - Mixing valve shift (UINT16, 0.01°C)
        registers[f"{prefix}_mixing_valve_shift"] = {
            "address": _zone_addr(678, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_TEMP,
        }
        # 679 - Mixing valve bandwidth (UINT16, 0.01°C)
        registers[f"{prefix}_mixing_valve_bandwidth"] = {
            "address": _zone_addr(679, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_TEMP,
        }
        # 680 - DHW hysteresis (UINT16, 0.01°C)
        registers[f"{prefix}_dhw_hysteresis"] = {
            "address": _zone_addr(680, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_TEMP,
        }
        # 681 - DHW calorifier offset (UINT16, 0.01°C)
        registers[f"{prefix}_dhw_calorifier_offset"] = {
            "address": _zone_addr(681, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_TEMP,
        }
        # 682 - DHW calorifier setpoint raise (UINT16, 0.01°C)
        registers[f"{prefix}_dhw_calorifier_raise"] = {
            "address": _zone_addr(682, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_TEMP,
        }
        # 683 - Process heat hysteresis (UINT16, 0.01°C)
        registers[f"{prefix}_process_heat_hysteresis"] = {
            "address": _zone_addr(683, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_TEMP,
        }
        # 684 - Process heat offset (UINT16, 0.01°C)
        registers[f"{prefix}_process_heat_offset"] = {
            "address": _zone_addr(684, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_TEMP,
        }
        # 685 - Process heat calorifier setpoint raise (UINT16, 0.01°C)
        registers[f"{prefix}_process_heat_calorifier_raise"] = {
            "address": _zone_addr(685, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_TEMP,
        }
        # 686 - DHW calorifier hysteresis (UINT16, 0.01°C, R/W)
        registers[f"{prefix}_dhw_calorifier_hysteresis"] = {
            "address": _zone_addr(686, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": IWR_SCALE_TEMP,
            "writable": True,
            "min": 0.5,
            "max": 20.0,
            "step": 0.1,
        }
        # 687 - Pump post-run delay (UINT8, minutes)
        registers[f"{prefix}_pump_post_run"] = {
            "address": _zone_addr(687, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": 1,
        }
        # 688 - Time program selected (ENUM8)
        registers[f"{prefix}_time_program_selected"] = {
            "address": _zone_addr(688, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": 1,
        }

        # ===== Zone measurements (from German spec 7740782-01) =====

        # 1103 - Zone outdoor temperature (INT16, 0.01°C)
        registers[f"{prefix}_outside_temp"] = {
            "address": _zone_addr(1103, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "int16",
            "scale": IWR_SCALE_TEMP,
        }
        # 1104 - Zone room temperature (INT16, 0.1°C)
        registers[f"{prefix}_room_temp"] = {
            "address": _zone_addr(1104, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "int16",
            "scale": IWR_SCALE_ROOM_TEMP,
        }
        # 1105 - Zone room temperature measured (INT16, 0.01°C, R/W)
        # Writing allows injecting an external room sensor value into the controller.
        registers[f"{prefix}_room_temp_measured"] = {
            "address": _zone_addr(1105, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "int16",
            "scale": IWR_SCALE_TEMP,
            "writable": True,
            "min": -30.0,
            "max": 50.0,
            "step": 0.1,
        }
        # 1106 - Zone heat demand on/off (ENUM8, 0=off/1=on)
        registers[f"{prefix}_heat_demand"] = {
            "address": _zone_addr(1106, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "bool",
        }
        # 1109 - Zone current heating mode (ENUM8)
        registers[f"{prefix}_heating_mode"] = {
            "address": _zone_addr(1109, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": 1,
        }
        # 1112 - Mixing valve opening (ENUM8, 0=no/1=yes)
        registers[f"{prefix}_mixing_valve_opening"] = {
            "address": _zone_addr(1112, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "bool",
        }
        # 1113 - Swimming pool secondary pump (ENUM8, 0=off/1=on)
        registers[f"{prefix}_swimming_pool_pump"] = {
            "address": _zone_addr(1113, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "bool",
        }
        # 1114 - Electrical backup output (ENUM8, 0=off/1=on)
        registers[f"{prefix}_electrical_backup_output"] = {
            "address": _zone_addr(1114, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "bool",
        }
        # 1119 - DHW tank temperature bottom sensor (INT16, 0.01°C)
        registers[f"{prefix}_dhw_tank_temp_bottom"] = {
            "address": _zone_addr(1119, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "int16",
            "scale": IWR_SCALE_TEMP,
        }
        # 1120 - DHW tank temperature top sensor (INT16, 0.01°C)
        registers[f"{prefix}_dhw_tank_temp_top"] = {
            "address": _zone_addr(1120, z),
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "int16",
            "scale": IWR_SCALE_TEMP,
        }

        for suffix, updates in _ZONE_WRITABLE_REGISTER_UPDATES.items():
            registers[f"{prefix}_{suffix}"].update(updates)

    return registers


def _build_zone_sensors(zones: list[int]) -> dict[str, Any]:
    """Generate sensor definitions for the given zone numbers (1-based)."""
    sensors: dict[str, Any] = {}
    for zn in zones:
        prefix = f"zone{zn}"

        sensors[f"{prefix}_flow_temp"] = {
            "register": f"{prefix}_flow_temp",
            "translation_key": "zone_flow_temp",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "zone_number": zn,
        }
        sensors[f"{prefix}_flow_setpoint"] = {
            "register": f"{prefix}_flow_setpoint",
            "translation_key": "zone_flow_setpoint",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "zone_number": zn,
        }
        sensors[f"{prefix}_room_setpoint"] = {
            "register": f"{prefix}_room_setpoint",
            "translation_key": "zone_room_setpoint",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "zone_number": zn,
        }
        sensors[f"{prefix}_activity"] = {
            "register": f"{prefix}_activity",
            "translation_key": "zone_activity",
            "device_class": "enum",
            "unit": None,
            "state_class": None,
            "icon": "mdi:thermostat",
            "enum_map": "iwr_zone_activity",
            "zone_number": zn,
        }
        sensors[f"{prefix}_operating_mode"] = {
            "register": f"{prefix}_operating_mode",
            "translation_key": "zone_operating_mode",
            "device_class": "enum",
            "unit": None,
            "state_class": None,
            "icon": "mdi:cog",
            "enum_map": "iwr_zone_operating_mode",
            "zone_number": zn,
        }
        sensors[f"{prefix}_pump_hours"] = {
            "register": f"{prefix}_pump_hours",
            "translation_key": "zone_pump_hours",
            "device_class": "duration",
            "unit": "h",
            "state_class": "total_increasing",
            "icon": "mdi:clock-outline",
            "zone_number": zn,
        }
        sensors[f"{prefix}_pump_starts"] = {
            "register": f"{prefix}_pump_starts",
            "translation_key": "zone_pump_starts",
            "device_class": None,
            "unit": None,
            "state_class": "total_increasing",
            "icon": "mdi:counter",
            "zone_number": zn,
        }
        sensors[f"{prefix}_function"] = {
            "register": f"{prefix}_function",
            "translation_key": "zone_function",
            "device_class": "enum",
            "unit": None,
            "state_class": None,
            "icon": "mdi:information-outline",
            "enum_map": "iwr_zone_function",
            "zone_number": zn,
        }
        sensors[f"{prefix}_device_type"] = {
            "register": f"{prefix}_device_type",
            "translation_key": "zone_device_type",
            "device_class": None,
            "unit": None,
            "state_class": None,
            "icon": "mdi:developer-board",
            "zone_number": zn,
            "value_format": "device_type",
            "device_categories": IWR_DEVICE_CATEGORY,
        }
        sensors[f"{prefix}_control_mode"] = {
            "register": f"{prefix}_control_mode",
            "translation_key": "zone_control_mode",
            "device_class": "enum",
            "unit": None,
            "state_class": None,
            "icon": "mdi:cog",
            "enum_map": "iwr_zone_control_mode",
            "zone_number": zn,
        }
        sensors[f"{prefix}_fixed_flow_setpoint"] = {
            "register": f"{prefix}_fixed_flow_setpoint",
            "translation_key": "zone_fixed_flow_setpoint",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "zone_number": zn,
        }
        sensors[f"{prefix}_room_setpoint_manual"] = {
            "register": f"{prefix}_room_setpoint_manual",
            "translation_key": "zone_room_setpoint_manual",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "zone_number": zn,
        }
        sensors[f"{prefix}_heating_curve_gradient"] = {
            "register": f"{prefix}_heating_curve_gradient",
            "translation_key": "zone_heating_curve_gradient",
            "device_class": None,
            "unit": None,
            "state_class": "measurement",
            "icon": "mdi:chart-line",
            "zone_number": zn,
        }
        sensors[f"{prefix}_heating_curve_footpoint"] = {
            "register": f"{prefix}_heating_curve_footpoint",
            "translation_key": "zone_heating_curve_footpoint",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:chart-line",
            "zone_number": zn,
        }

        # ===== New zone sensors from German spec 7740782-01 =====

        sensors[f"{prefix}_zone_type"] = {
            "register": f"{prefix}_zone_type",
            "translation_key": "zone_type",
            "device_class": "enum",
            "unit": None,
            "state_class": None,
            "icon": "mdi:information-outline",
            "enum_map": "iwr_zone_type",
            "zone_number": zn,
        }
        for sp in range(1, 6):
            sensors[f"{prefix}_comfort_setpoint_{sp}"] = {
                "register": f"{prefix}_comfort_setpoint_{sp}",
                "translation_key": f"zone_comfort_setpoint_{sp}",
                "device_class": "temperature",
                "unit": "°C",
                "state_class": "measurement",
                "icon": "mdi:home-thermometer",
                "zone_number": zn,
            }
        sensors[f"{prefix}_night_setback"] = {
            "register": f"{prefix}_night_setback",
            "translation_key": "zone_night_setback",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:weather-night",
            "zone_number": zn,
        }
        for sp in range(1, 6):
            sensors[f"{prefix}_cooling_room_setpoint_{sp}"] = {
                "register": f"{prefix}_cooling_room_setpoint_{sp}",
                "translation_key": f"zone_cooling_room_setpoint_{sp}",
                "device_class": "temperature",
                "unit": "°C",
                "state_class": "measurement",
                "icon": "mdi:snowflake-thermometer",
                "zone_number": zn,
            }
        sensors[f"{prefix}_cooling_night_setback"] = {
            "register": f"{prefix}_cooling_night_setback",
            "translation_key": "zone_cooling_night_setback",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:snowflake-thermometer",
            "zone_number": zn,
        }
        sensors[f"{prefix}_holiday_setpoint"] = {
            "register": f"{prefix}_holiday_setpoint",
            "translation_key": "zone_holiday_setpoint",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:beach",
            "zone_number": zn,
        }
        sensors[f"{prefix}_temporary_setpoint"] = {
            "register": f"{prefix}_temporary_setpoint",
            "translation_key": "zone_temporary_setpoint",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:clock-fast",
            "zone_number": zn,
        }
        sensors[f"{prefix}_dhw_comfort_setpoint"] = {
            "register": f"{prefix}_dhw_comfort_setpoint",
            "translation_key": "zone_dhw_comfort_setpoint",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:water-thermometer",
            "zone_number": zn,
        }
        sensors[f"{prefix}_dhw_reduced_setpoint"] = {
            "register": f"{prefix}_dhw_reduced_setpoint",
            "translation_key": "zone_dhw_reduced_setpoint",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:water-thermometer",
            "zone_number": zn,
        }
        sensors[f"{prefix}_dhw_holiday_setpoint"] = {
            "register": f"{prefix}_dhw_holiday_setpoint",
            "translation_key": "zone_dhw_holiday_setpoint",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:water-thermometer",
            "zone_number": zn,
        }
        sensors[f"{prefix}_dhw_antilegionella_setpoint"] = {
            "register": f"{prefix}_dhw_antilegionella_setpoint",
            "translation_key": "zone_dhw_antilegionella_setpoint",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:bacteria-outline",
            "zone_number": zn,
        }
        sensors[f"{prefix}_swimming_pool_setpoint"] = {
            "register": f"{prefix}_swimming_pool_setpoint",
            "translation_key": "zone_swimming_pool_setpoint",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:pool-thermometer",
            "zone_number": zn,
        }
        sensors[f"{prefix}_process_heat_setpoint"] = {
            "register": f"{prefix}_process_heat_setpoint",
            "translation_key": "zone_process_heat_setpoint",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:fire",
            "zone_number": zn,
        }
        sensors[f"{prefix}_heating_control_strategy"] = {
            "register": f"{prefix}_heating_control_strategy",
            "translation_key": "zone_heating_control_strategy",
            "device_class": "enum",
            "unit": None,
            "state_class": None,
            "icon": "mdi:strategy",
            "enum_map": "iwr_heating_control_strategy",
            "zone_number": zn,
        }
        sensors[f"{prefix}_max_flow_setpoint"] = {
            "register": f"{prefix}_max_flow_setpoint",
            "translation_key": "zone_max_flow_setpoint",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:thermometer-chevron-up",
            "zone_number": zn,
        }
        sensors[f"{prefix}_cooling_mixing_setpoint"] = {
            "register": f"{prefix}_cooling_mixing_setpoint",
            "translation_key": "zone_cooling_mixing_setpoint",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:snowflake-thermometer",
            "zone_number": zn,
        }
        sensors[f"{prefix}_heating_curve_footpoint_night"] = {
            "register": f"{prefix}_heating_curve_footpoint_night",
            "translation_key": "zone_heating_curve_footpoint_night",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:chart-line",
            "zone_number": zn,
        }
        sensors[f"{prefix}_max_preheat_time"] = {
            "register": f"{prefix}_max_preheat_time",
            "translation_key": "zone_max_preheat_time",
            "device_class": None,
            "unit": "min",
            "state_class": "measurement",
            "icon": "mdi:clock-start",
            "zone_number": zn,
        }
        sensors[f"{prefix}_mixing_valve_shift"] = {
            "register": f"{prefix}_mixing_valve_shift",
            "translation_key": "zone_mixing_valve_shift",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:valve",
            "zone_number": zn,
        }
        sensors[f"{prefix}_mixing_valve_bandwidth"] = {
            "register": f"{prefix}_mixing_valve_bandwidth",
            "translation_key": "zone_mixing_valve_bandwidth",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:valve",
            "zone_number": zn,
        }
        sensors[f"{prefix}_dhw_hysteresis"] = {
            "register": f"{prefix}_dhw_hysteresis",
            "translation_key": "zone_dhw_hysteresis",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:water-thermometer",
            "zone_number": zn,
        }
        sensors[f"{prefix}_dhw_calorifier_offset"] = {
            "register": f"{prefix}_dhw_calorifier_offset",
            "translation_key": "zone_dhw_calorifier_offset",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:water-thermometer",
            "zone_number": zn,
        }
        sensors[f"{prefix}_dhw_calorifier_raise"] = {
            "register": f"{prefix}_dhw_calorifier_raise",
            "translation_key": "zone_dhw_calorifier_raise",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:water-thermometer",
            "zone_number": zn,
        }
        sensors[f"{prefix}_process_heat_hysteresis"] = {
            "register": f"{prefix}_process_heat_hysteresis",
            "translation_key": "zone_process_heat_hysteresis",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:fire",
            "zone_number": zn,
        }
        sensors[f"{prefix}_process_heat_offset"] = {
            "register": f"{prefix}_process_heat_offset",
            "translation_key": "zone_process_heat_offset",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:fire",
            "zone_number": zn,
        }
        sensors[f"{prefix}_process_heat_calorifier_raise"] = {
            "register": f"{prefix}_process_heat_calorifier_raise",
            "translation_key": "zone_process_heat_calorifier_raise",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:fire",
            "zone_number": zn,
        }
        sensors[f"{prefix}_dhw_calorifier_hysteresis"] = {
            "register": f"{prefix}_dhw_calorifier_hysteresis",
            "translation_key": "zone_dhw_calorifier_hysteresis",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:water-thermometer",
            "zone_number": zn,
        }
        sensors[f"{prefix}_pump_post_run"] = {
            "register": f"{prefix}_pump_post_run",
            "translation_key": "zone_pump_post_run",
            "device_class": None,
            "unit": "min",
            "state_class": "measurement",
            "icon": "mdi:pump",
            "zone_number": zn,
        }
        sensors[f"{prefix}_time_program_selected"] = {
            "register": f"{prefix}_time_program_selected",
            "translation_key": "zone_time_program_selected",
            "device_class": "enum",
            "unit": None,
            "state_class": None,
            "icon": "mdi:clock-outline",
            "enum_map": "iwr_time_program_selected",
            "zone_number": zn,
        }

        # ===== Zone measurements (from German spec 7740782-01) =====

        sensors[f"{prefix}_outside_temp"] = {
            "register": f"{prefix}_outside_temp",
            "translation_key": "zone_outside_temp",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "zone_number": zn,
        }
        sensors[f"{prefix}_room_temp"] = {
            "register": f"{prefix}_room_temp",
            "translation_key": "zone_room_temp",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:home-thermometer",
            "zone_number": zn,
        }
        sensors[f"{prefix}_room_temp_measured"] = {
            "register": f"{prefix}_room_temp_measured",
            "translation_key": "zone_room_temp_measured",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:home-thermometer",
            "zone_number": zn,
        }
        sensors[f"{prefix}_heating_mode"] = {
            "register": f"{prefix}_heating_mode",
            "translation_key": "zone_heating_mode",
            "device_class": "enum",
            "unit": None,
            "state_class": None,
            "icon": "mdi:thermostat",
            "enum_map": "iwr_zone_heating_mode",
            "zone_number": zn,
        }
        sensors[f"{prefix}_dhw_tank_temp_bottom"] = {
            "register": f"{prefix}_dhw_tank_temp_bottom",
            "translation_key": "zone_dhw_tank_temp_bottom",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:water-thermometer",
            "zone_number": zn,
        }
        sensors[f"{prefix}_dhw_tank_temp_top"] = {
            "register": f"{prefix}_dhw_tank_temp_top",
            "translation_key": "zone_dhw_tank_temp_top",
            "device_class": "temperature",
            "unit": "°C",
            "state_class": "measurement",
            "icon": "mdi:water-thermometer",
            "zone_number": zn,
        }

    return sensors


def _build_zone_binary_sensors(zones: list[int]) -> dict[str, Any]:
    """Generate binary sensor definitions for the given zone numbers (1-based)."""
    binary_sensors: dict[str, Any] = {}
    for zn in zones:
        prefix = f"zone{zn}"

        binary_sensors[f"{prefix}_pump"] = {
            "register": f"{prefix}_pump",
            "translation_key": "zone_pump",
            "device_class": "running",
            "zone_number": zn,
        }
        binary_sensors[f"{prefix}_flow_measurement"] = {
            "register": f"{prefix}_flow_measurement",
            "translation_key": "zone_flow_measurement",
            "device_class": None,
            "icon": "mdi:thermometer-check",
            "zone_number": zn,
        }

        # ===== Zone binary measurements (from German spec 7740782-01) =====

        binary_sensors[f"{prefix}_heat_demand"] = {
            "register": f"{prefix}_heat_demand",
            "translation_key": "zone_heat_demand",
            "device_class": "heat",
            "zone_number": zn,
        }
        binary_sensors[f"{prefix}_mixing_valve_opening"] = {
            "register": f"{prefix}_mixing_valve_opening",
            "translation_key": "zone_mixing_valve_opening",
            "device_class": None,
            "icon": "mdi:valve-open",
            "zone_number": zn,
        }
        binary_sensors[f"{prefix}_swimming_pool_pump"] = {
            "register": f"{prefix}_swimming_pool_pump",
            "translation_key": "zone_swimming_pool_pump",
            "device_class": "running",
            "icon": "mdi:pool",
            "zone_number": zn,
        }
        binary_sensors[f"{prefix}_electrical_backup_output"] = {
            "register": f"{prefix}_electrical_backup_output",
            "translation_key": "zone_electrical_backup_output",
            "device_class": "running",
            "icon": "mdi:lightning-bolt",
            "zone_number": zn,
        }

    return binary_sensors


# ===== Board Info Builders (System Discovery, addresses 129-188) =====

_BOARD_COUNT: Final = 10  # GTW-08 supports up to 10 electronic boards


def _build_board_registers() -> dict[str, Any]:
    """Generate register definitions for board info (boards 1..10).

    Each board occupies 6 registers starting at 129 + 6*(n-1):
      DeviceType (uint16), SoftwareVersion (uint16),
      ConfigTableVersion (uint16), HardwareVersion (uint16),
      ArticleNumber (uint32 = 2 registers).
    """
    registers: dict[str, Any] = {}
    for n in range(1, _BOARD_COUNT + 1):
        base = 129 + 6 * (n - 1)
        prefix = f"board{n}"

        registers[f"{prefix}_device_type"] = {
            "address": base,
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": 1,
        }
        registers[f"{prefix}_software_version"] = {
            "address": base + 1,
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": 1,
        }
        registers[f"{prefix}_config_table_version"] = {
            "address": base + 2,
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": 1,
        }
        registers[f"{prefix}_hardware_version"] = {
            "address": base + 3,
            "type": REG_HOLDING,
            "count": 1,
            "data_type": "uint16",
            "scale": 1,
        }
        registers[f"{prefix}_article_number"] = {
            "address": base + 4,
            "type": REG_HOLDING,
            "count": 2,
            "data_type": "uint32",
            "scale": 1,
        }

    return registers


def _build_board_sensors() -> dict[str, Any]:
    """Generate sensor definitions for board info (boards 1..10)."""
    sensors: dict[str, Any] = {}
    for n in range(1, _BOARD_COUNT + 1):
        prefix = f"board{n}"

        sensors[f"{prefix}_device_type"] = {
            "register": f"{prefix}_device_type",
            "translation_key": "board_device_type",
            "device_class": None,
            "unit": None,
            "state_class": None,
            "icon": "mdi:chip",
            "board_number": n,
        }
        sensors[f"{prefix}_software_version"] = {
            "register": f"{prefix}_software_version",
            "translation_key": "board_software_version",
            "device_class": None,
            "unit": None,
            "state_class": None,
            "icon": "mdi:memory",
            "board_number": n,
        }
        sensors[f"{prefix}_config_table_version"] = {
            "register": f"{prefix}_config_table_version",
            "translation_key": "board_config_table_version",
            "device_class": None,
            "unit": None,
            "state_class": None,
            "icon": "mdi:memory",
            "board_number": n,
        }
        sensors[f"{prefix}_hardware_version"] = {
            "register": f"{prefix}_hardware_version",
            "translation_key": "board_hardware_version",
            "device_class": None,
            "unit": None,
            "state_class": None,
            "icon": "mdi:memory",
            "board_number": n,
        }
        sensors[f"{prefix}_article_number"] = {
            "register": f"{prefix}_article_number",
            "translation_key": "board_article_number",
            "device_class": None,
            "unit": None,
            "state_class": None,
            "icon": "mdi:barcode",
            "board_number": n,
        }

    return sensors


# ===== Writable Entity Builders =====


_ZONE_NUMBER_DEFINITIONS: Final[dict[str, dict[str, Any]]] = {
    "comfort_setpoint_1": {
        "translation_key": "zone_comfort_setpoint_1",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "comfort_setpoint_2": {
        "translation_key": "zone_comfort_setpoint_2",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "comfort_setpoint_3": {
        "translation_key": "zone_comfort_setpoint_3",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "comfort_setpoint_4": {
        "translation_key": "zone_comfort_setpoint_4",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "comfort_setpoint_5": {
        "translation_key": "zone_comfort_setpoint_5",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "night_setback": {
        "translation_key": "zone_night_setback",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "cooling_room_setpoint_1": {
        "translation_key": "zone_cooling_room_setpoint_1",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "cooling_room_setpoint_2": {
        "translation_key": "zone_cooling_room_setpoint_2",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "cooling_room_setpoint_3": {
        "translation_key": "zone_cooling_room_setpoint_3",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "cooling_room_setpoint_4": {
        "translation_key": "zone_cooling_room_setpoint_4",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "cooling_room_setpoint_5": {
        "translation_key": "zone_cooling_room_setpoint_5",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "cooling_night_setback": {
        "translation_key": "zone_cooling_night_setback",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "holiday_setpoint": {
        "translation_key": "zone_holiday_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "temporary_setpoint": {
        "translation_key": "zone_temporary_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "room_setpoint_manual": {
        "translation_key": "zone_room_setpoint_manual",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "slider",
    },
    "dhw_comfort_setpoint": {
        "translation_key": "zone_dhw_comfort_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "dhw_reduced_setpoint": {
        "translation_key": "zone_dhw_reduced_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "dhw_holiday_setpoint": {
        "translation_key": "zone_dhw_holiday_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "dhw_antilegionella_setpoint": {
        "translation_key": "zone_dhw_antilegionella_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "swimming_pool_setpoint": {
        "translation_key": "zone_swimming_pool_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "process_heat_setpoint": {
        "translation_key": "zone_process_heat_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "max_flow_setpoint": {
        "translation_key": "zone_max_flow_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "cooling_mixing_setpoint": {
        "translation_key": "zone_cooling_mixing_setpoint",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "heating_curve_footpoint_night": {
        "translation_key": "zone_heating_curve_footpoint_night",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "max_preheat_time": {
        "translation_key": "zone_max_preheat_time",
        "device_class": None,
        "unit": "min",
        "mode": "box",
    },
    "mixing_valve_shift": {
        "translation_key": "zone_mixing_valve_shift",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "mixing_valve_bandwidth": {
        "translation_key": "zone_mixing_valve_bandwidth",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "dhw_hysteresis": {
        "translation_key": "zone_dhw_hysteresis",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "dhw_calorifier_offset": {
        "translation_key": "zone_dhw_calorifier_offset",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "dhw_calorifier_raise": {
        "translation_key": "zone_dhw_calorifier_raise",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "process_heat_hysteresis": {
        "translation_key": "zone_process_heat_hysteresis",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "process_heat_offset": {
        "translation_key": "zone_process_heat_offset",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "process_heat_calorifier_raise": {
        "translation_key": "zone_process_heat_calorifier_raise",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "dhw_calorifier_hysteresis": {
        "translation_key": "zone_dhw_calorifier_hysteresis",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
    "pump_post_run": {
        "translation_key": "zone_pump_post_run",
        "device_class": None,
        "unit": "min",
        "mode": "box",
    },
    "room_temp_measured": {
        "translation_key": "zone_room_temp_measured",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
    },
}


def _build_zone_numbers(zones: list[int]) -> dict[str, Any]:
    """Generate number entity definitions for writable numeric zone registers."""
    numbers: dict[str, Any] = {}
    for zn in zones:
        prefix = f"zone{zn}"
        for suffix, definition in _ZONE_NUMBER_DEFINITIONS.items():
            numbers[f"{prefix}_{suffix}"] = {
                "register": f"{prefix}_{suffix}",
                "zone_number": zn,
                **definition,
            }

    return numbers


# Static (non-zone) number entities for the IWR device.
_IWR_STATIC_NUMBERS: Final[dict[str, Any]] = {
    # Boiler / hybrid settings and operating limits.
    "hybrid_electricity_cost_high_tariff": {
        "register": "hybrid_electricity_cost_high_tariff",
        "translation_key": "hybrid_electricity_cost_high_tariff",
        "device_class": None,
        "unit": None,
        "mode": "box",
        "sub_device": SUBDEV_HYBRID,
    },
    "hybrid_electricity_cost_low_tariff": {
        "register": "hybrid_electricity_cost_low_tariff",
        "translation_key": "hybrid_electricity_cost_low_tariff",
        "device_class": None,
        "unit": None,
        "mode": "box",
        "sub_device": SUBDEV_HYBRID,
    },
    "fossil_energy_cost": {
        "register": "fossil_energy_cost",
        "translation_key": "fossil_energy_cost",
        "device_class": None,
        "unit": None,
        "mode": "box",
        "sub_device": SUBDEV_HYBRID,
    },
    "electrical_co2_emission_heating_mode": {
        "register": "electrical_co2_emission_heating_mode",
        "translation_key": "electrical_co2_emission_heating_mode",
        "device_class": None,
        "unit": None,
        "mode": "box",
        "sub_device": SUBDEV_HYBRID,
    },
    "electrical_co2_emission_dhw_mode": {
        "register": "electrical_co2_emission_dhw_mode",
        "translation_key": "electrical_co2_emission_dhw_mode",
        "device_class": None,
        "unit": None,
        "mode": "box",
        "sub_device": SUBDEV_HYBRID,
    },
    "gas_or_oil_co2_emission": {
        "register": "gas_or_oil_co2_emission",
        "translation_key": "gas_or_oil_co2_emission",
        "device_class": None,
        "unit": None,
        "mode": "box",
        "sub_device": SUBDEV_HYBRID,
    },
    "boiler_efficiency": {
        "register": "boiler_efficiency",
        "translation_key": "boiler_efficiency",
        "device_class": None,
        "unit": "%",
        "mode": "box",
        "sub_device": SUBDEV_BOILER,
    },
    "cop_threshold_primary_energy": {
        "register": "cop_threshold_primary_energy",
        "translation_key": "cop_threshold_primary_energy",
        "device_class": None,
        "unit": None,
        "mode": "box",
        "sub_device": SUBDEV_HYBRID,
    },
    "dhw_min_heating_time": {
        "register": "dhw_min_heating_time",
        "translation_key": "dhw_min_heating_time",
        "device_class": None,
        "unit": "h",
        "mode": "box",
        "sub_device": SUBDEV_BOILER,
    },
    "dhw_max_production_time": {
        "register": "dhw_max_production_time",
        "translation_key": "dhw_max_production_time",
        "device_class": None,
        "unit": "h",
        "mode": "box",
        "sub_device": SUBDEV_BOILER,
    },
    "hybrid_electricity_cost_high_tariff_accurate": {
        "register": "hybrid_electricity_cost_high_tariff_accurate",
        "translation_key": "hybrid_electricity_cost_high_tariff_accurate",
        "device_class": None,
        "unit": None,
        "mode": "box",
        "sub_device": SUBDEV_HYBRID,
    },
    "hybrid_electricity_cost_low_tariff_accurate": {
        "register": "hybrid_electricity_cost_low_tariff_accurate",
        "translation_key": "hybrid_electricity_cost_low_tariff_accurate",
        "device_class": None,
        "unit": None,
        "mode": "box",
        "sub_device": SUBDEV_HYBRID,
    },
    "fossil_energy_cost_accurate": {
        "register": "fossil_energy_cost_accurate",
        "translation_key": "fossil_energy_cost_accurate",
        "device_class": None,
        "unit": None,
        "mode": "box",
        "sub_device": SUBDEV_HYBRID,
    },
    "outside_temperature_level_backup_blocked": {
        "register": "outside_temperature_level_backup_blocked",
        "translation_key": "outside_temperature_level_backup_blocked",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
        "sub_device": SUBDEV_BOILER,
    },
    "next_generator_start_delay": {
        "register": "next_generator_start_delay",
        "translation_key": "next_generator_start_delay",
        "device_class": None,
        "unit": "min",
        "mode": "box",
        "sub_device": SUBDEV_BOILER,
    },
    "minimum_outside_temperature_heat_pump_stopped": {
        "register": "minimum_outside_temperature_heat_pump_stopped",
        "translation_key": "minimum_outside_temperature_heat_pump_stopped",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
        "sub_device": SUBDEV_BOILER,
    },
    "control_cooling_temperature": {
        "register": "control_cooling_temperature",
        "translation_key": "control_cooling_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
        "sub_device": SUBDEV_BOILER,
    },
    "summer_winter_threshold": {
        "register": "summer_winter_threshold",
        "translation_key": "summer_winter_threshold",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
        "sub_device": SUBDEV_BOILER,
    },
    "neutral_band": {
        "register": "neutral_band",
        "translation_key": "neutral_band",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
        "sub_device": SUBDEV_BOILER,
    },
    "frost_protection_threshold": {
        "register": "frost_protection_threshold",
        "translation_key": "frost_protection_threshold",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
        "sub_device": SUBDEV_BOILER,
    },
    # --- Remote Power / Temperature Control (Tab.18, registers 256-257, R/W) ---
    "control_power": {
        "register": "control_power",
        "translation_key": "control_power",
        "device_class": None,
        "unit": "%",
        "mode": "box",
        "icon": "mdi:gauge",
        "sub_device": SUBDEV_BOILER,
    },
    "control_temperature": {
        "register": "control_temperature",
        "translation_key": "control_temperature",
        "device_class": "temperature",
        "unit": "°C",
        "mode": "box",
        "sub_device": SUBDEV_BOILER,
    },
}


_IWR_STATIC_TIMES: Final[dict[str, Any]] = {
    "low_noise_start_time": {
        "register": "low_noise_start_time",
        "translation_key": "low_noise_start_time",
        "slot_minutes": 10,
        "icon": "mdi:clock-start",
        "sub_device": SUBDEV_BOILER,
    },
    "low_noise_stop_time": {
        "register": "low_noise_stop_time",
        "translation_key": "low_noise_stop_time",
        "slot_minutes": 10,
        "icon": "mdi:clock-stop",
        "sub_device": SUBDEV_BOILER,
    },
}


# Static (non-zone) select entities for the IWR device.
_IWR_STATIC_SELECTS: Final[dict[str, Any]] = {
    # DP051 - DHW ECO or COMFORT setting (register 479, R/W)
    # Only relevant for hybrid systems that have a backup boiler.
    "dhw_eco_comfort_mode": {
        "register": "dhw_eco_comfort_mode",
        "translation_key": "dhw_eco_comfort_mode",
        "enum_map": "iwr_dhw_eco_comfort",
        "icon": "mdi:water-boiler",
        "sub_device": SUBDEV_HYBRID,
    },
    "hybrid_mode_selected": {
        "register": "hybrid_mode_selected",
        "translation_key": "hybrid_mode_selected",
        "enum_map": "iwr_hybrid_mode_selected",
        "icon": "mdi:flash",
        "sub_device": SUBDEV_HYBRID,
    },
    "blocking_input_1_contact": {
        "register": "blocking_input_1_contact",
        "translation_key": "blocking_input_1_contact",
        "enum_map": "iwr_logic_contact",
        "icon": "mdi:toggle-switch",
        "sub_device": SUBDEV_BOILER,
    },
    "blocking_input_2_contact": {
        "register": "blocking_input_2_contact",
        "translation_key": "blocking_input_2_contact",
        "enum_map": "iwr_logic_contact",
        "icon": "mdi:toggle-switch",
        "sub_device": SUBDEV_BOILER,
    },
    "blocking_input_2_setting": {
        "register": "blocking_input_2_setting",
        "translation_key": "blocking_input_2_setting",
        "enum_map": "iwr_blocking_input_setting",
        "icon": "mdi:progress-alert",
        "sub_device": SUBDEV_BOILER,
    },
    "function_blocking_input": {
        "register": "function_blocking_input",
        "translation_key": "function_blocking_input",
        "enum_map": "iwr_blocking_input_setting",
        "icon": "mdi:progress-alert",
        "sub_device": SUBDEV_BOILER,
    },
    "backup_type": {
        "register": "backup_type",
        "translation_key": "backup_type",
        "enum_map": "iwr_backup_type",
        "icon": "mdi:backup-restore",
        "sub_device": SUBDEV_BOILER,
    },
    "heat_pump_silent_mode": {
        "register": "heat_pump_silent_mode",
        "translation_key": "heat_pump_silent_mode",
        "enum_map": "iwr_low_noise_mode_state",
        "icon": "mdi:volume-off",
        "sub_device": SUBDEV_BOILER,
    },
    # --- Remote Control Algorithm & Heat Demand (Tab.18, registers 258-259, R/W) ---
    "control_algorithm_type": {
        "register": "control_algorithm_type",
        "translation_key": "control_algorithm_type",
        "icon": "mdi:cog-outline",
        "enum_map": "iwr_algorithm_type",
        "sub_device": SUBDEV_BOILER,
    },
    "control_heat_demand_type": {
        "register": "control_heat_demand_type",
        "translation_key": "control_heat_demand_type",
        "icon": "mdi:fire-circle",
        "enum_map": "iwr_heat_demand_type",
        "sub_device": SUBDEV_BOILER,
    },
    "force_summer_mode": {
        "register": "force_summer_mode",
        "translation_key": "force_summer_mode",
        "icon": "mdi:weather-sunny",
        "enum_map": "iwr_on_off",
        "sub_device": SUBDEV_BOILER,
    },
    "ch_enabled": {
        "register": "ch_enabled",
        "translation_key": "ch_enabled",
        "icon": "mdi:radiator",
        "enum_map": "iwr_on_off",
        "sub_device": SUBDEV_BOILER,
    },
    "dhw_enabled": {
        "register": "dhw_enabled",
        "translation_key": "dhw_enabled",
        "icon": "mdi:water-boiler",
        "enum_map": "iwr_on_off",
        "sub_device": SUBDEV_BOILER,
    },
    "cooling_enabled": {
        "register": "cooling_enabled",
        "translation_key": "cooling_enabled",
        "icon": "mdi:snowflake",
        "enum_map": "iwr_cooling_enabled",
        "sub_device": SUBDEV_BOILER,
    },
    "cooling_forced": {
        "register": "cooling_forced",
        "translation_key": "cooling_forced",
        "icon": "mdi:snowflake-alert",
        "enum_map": "iwr_on_off",
        "sub_device": SUBDEV_BOILER,
    },
}


def _build_zone_selects(zones: list[int]) -> dict[str, Any]:
    """Generate select entity definitions for writable enum zone registers."""
    selects: dict[str, Any] = {}
    for zn in zones:
        prefix = f"zone{zn}"

        # CP32X - Zone control mode (R/W)
        selects[f"{prefix}_control_mode"] = {
            "register": f"{prefix}_control_mode",
            "translation_key": "zone_control_mode",
            "enum_map": "iwr_zone_control_mode",
            "icon": "mdi:cog",
            "zone_number": zn,
        }
        selects[f"{prefix}_heating_control_strategy"] = {
            "register": f"{prefix}_heating_control_strategy",
            "translation_key": "zone_heating_control_strategy",
            "enum_map": "iwr_heating_control_strategy",
            "icon": "mdi:home-thermometer-outline",
            "zone_number": zn,
        }
        selects[f"{prefix}_time_program_selected"] = {
            "register": f"{prefix}_time_program_selected",
            "translation_key": "zone_time_program_selected",
            "enum_map": "iwr_time_program_selected",
            "icon": "mdi:clock-outline",
            "zone_number": zn,
        }

    return selects


def _build_zone_climates(zones: list[int]) -> dict[str, Any]:
    """Generate climate entity definitions for zone thermostat control."""
    climates: dict[str, Any] = {}
    for zn in zones:
        prefix = f"zone{zn}"
        climates[f"{prefix}_climate"] = {
            "temperature_register": f"{prefix}_room_temp_measured",
            "setpoint_register": f"{prefix}_room_setpoint_manual",
            "control_mode_register": f"{prefix}_control_mode",
            "heating_mode_register": f"{prefix}_heating_mode",
            "zone_number": zn,
            "translation_key": "zone_climate",
        }
    return climates


# Registers that have been promoted to number/select entities and should
# no longer appear as read-only sensors.
_WRITABLE_ZONE_SENSOR_KEYS: Final[set[str]] = {
    "control_mode",
    "comfort_setpoint_1",
    "comfort_setpoint_2",
    "comfort_setpoint_3",
    "comfort_setpoint_4",
    "comfort_setpoint_5",
    "night_setback",
    "cooling_room_setpoint_1",
    "cooling_room_setpoint_2",
    "cooling_room_setpoint_3",
    "cooling_room_setpoint_4",
    "cooling_room_setpoint_5",
    "cooling_night_setback",
    "holiday_setpoint",
    "temporary_setpoint",
    "dhw_comfort_setpoint",
    "dhw_reduced_setpoint",
    "dhw_holiday_setpoint",
    "dhw_antilegionella_setpoint",
    "swimming_pool_setpoint",
    "process_heat_setpoint",
    "heating_control_strategy",
    "max_flow_setpoint",
    "cooling_mixing_setpoint",
    "heating_curve_footpoint_night",
    "max_preheat_time",
    "mixing_valve_shift",
    "mixing_valve_bandwidth",
    "dhw_hysteresis",
    "dhw_calorifier_offset",
    "dhw_calorifier_raise",
    "process_heat_hysteresis",
    "process_heat_offset",
    "process_heat_calorifier_raise",
    "dhw_calorifier_hysteresis",
    "pump_post_run",
    "time_program_selected",
    "room_setpoint_manual",
    "room_temp_measured",
}

_WRITABLE_STATIC_SENSOR_KEYS: Final[set[str]] = {
    "ch_enabled",
    "control_cooling_temperature",
    "cooling_enabled",
    "cooling_forced",
    "dhw_enabled",
    "force_summer_mode",
    "frost_protection_threshold",
    "neutral_band",
    "summer_winter_threshold",
}

_ZONE_ROLE_HEATING: Final = "heating"
_ZONE_ROLE_DHW: Final = "dhw"
_ZONE_ROLE_INACTIVE: Final = "inactive"

_ZONE_INACTIVE_KEEP_SUFFIXES: Final[set[str]] = {"zone_type", "function", "device_type"}
_ZONE_DHW_ONLY_SUFFIXES: Final[set[str]] = {
    "dhw_comfort_setpoint",
    "dhw_reduced_setpoint",
    "dhw_holiday_setpoint",
    "dhw_antilegionella_setpoint",
    "dhw_hysteresis",
    "dhw_calorifier_offset",
    "dhw_calorifier_raise",
    "dhw_calorifier_hysteresis",
    "dhw_tank_temp_bottom",
    "dhw_tank_temp_top",
}
_ZONE_HEATING_ONLY_SUFFIXES: Final[set[str]] = {
    "room_setpoint_manual",
    "comfort_setpoint_1",
    "comfort_setpoint_2",
    "comfort_setpoint_3",
    "comfort_setpoint_4",
    "comfort_setpoint_5",
    "night_setback",
    "holiday_setpoint",
    "temporary_setpoint",
    "swimming_pool_setpoint",
    "process_heat_setpoint",
    "heating_control_strategy",
    "max_flow_setpoint",
    "heating_curve_footpoint_night",
    "max_preheat_time",
    "mixing_valve_shift",
    "mixing_valve_bandwidth",
    "process_heat_hysteresis",
    "process_heat_offset",
    "process_heat_calorifier_raise",
    "pump_post_run",
    "climate",
}


def _zone_key_parts(entity_key: str) -> tuple[int, str] | None:
    """Split a zone-prefixed entity/register key into zone number and suffix."""
    if not entity_key.startswith("zone"):
        return None
    prefix, separator, suffix = entity_key.partition("_")
    if not separator:
        return None
    try:
        return int(prefix[4:]), suffix
    except ValueError:
        return None


def _zone_role(zone_number: int, zone_details: dict[str, Any] | None) -> str:
    """Return the persisted zone role for a zone number."""
    if not zone_details:
        return _ZONE_ROLE_HEATING
    return zone_details.get(str(zone_number), {}).get("role", _ZONE_ROLE_HEATING)


def _is_zone_key_allowed(
    entity_key: str,
    zone_details: dict[str, Any] | None,
    features: dict[str, bool],
) -> bool:
    """Return True when a zone-scoped register/entity is enabled."""
    parts = _zone_key_parts(entity_key)
    if parts is None:
        return True

    zone_number, suffix = parts
    role = _zone_role(zone_number, zone_details)

    if role == _ZONE_ROLE_INACTIVE:
        return suffix in _ZONE_INACTIVE_KEEP_SUFFIXES

    if not features.get(FEATURE_COOLING, True) and "cooling" in suffix:
        return False

    if role == _ZONE_ROLE_DHW:
        if suffix in _ZONE_HEATING_ONLY_SUFFIXES or "cooling" in suffix:
            return False
    else:
        if suffix in _ZONE_DHW_ONLY_SUFFIXES:
            return False

    return True


def _feature_for_register(entity_key: str, register_config: dict[str, Any]) -> str | None:
    """Map a register definition to an optional feature group."""
    address = int(register_config.get("address", -1))
    sub_device = register_config.get("sub_device")

    if "hybrid" in entity_key:
        return FEATURE_HYBRID
    if entity_key.startswith("cascade_"):
        return FEATURE_CASCADE
    if sub_device == SUBDEV_BUFFER_TANK or 7600 <= address <= 7699:
        return FEATURE_BUFFER_TANK
    if sub_device == SUBDEV_HYBRID or 464 <= address <= 486:
        return FEATURE_HYBRID
    if "cooling" in entity_key:
        return FEATURE_COOLING
    return None


def _filter_iwr_register_map(
    register_map: dict[str, Any],
    features: dict[str, bool],
    zone_details: dict[str, Any] | None,
) -> dict[str, Any]:
    """Filter register definitions according to selected feature groups."""
    filtered: dict[str, Any] = {}
    for entity_key, register_config in register_map.items():
        if not _is_zone_key_allowed(entity_key, zone_details, features):
            continue

        feature = _feature_for_register(entity_key, register_config)
        if feature is not None and not features.get(feature, False):
            continue

        filtered[entity_key] = register_config

    return filtered


def _filter_register_entities(
    entity_map: dict[str, Any],
    register_map: dict[str, Any],
) -> dict[str, Any]:
    """Keep only entities whose backing register still exists."""
    return {
        entity_key: entity_config
        for entity_key, entity_config in entity_map.items()
        if entity_config.get("register") in register_map
    }


def _filter_climate_entities(
    climates: dict[str, Any],
    register_map: dict[str, Any],
) -> dict[str, Any]:
    """Keep only climates whose backing registers still exist."""
    filtered: dict[str, Any] = {}
    for entity_key, entity_config in climates.items():
        required_registers = (
            entity_config["temperature_register"],
            entity_config["setpoint_register"],
            entity_config["control_mode_register"],
            entity_config["heating_mode_register"],
        )
        if all(register_key in register_map for register_key in required_registers):
            filtered[entity_key] = entity_config
    return filtered


# ===== Public API =====


def _build_entity_classification(
    sensors: dict[str, Any],
    binary_sensors: dict[str, Any],
    numbers: dict[str, Any],
    selects: dict[str, Any],
    times: dict[str, Any],
) -> dict[str, tuple[str | None, bool]]:
    """Build a merged classification map for all IWR entities.

    Static entities are looked up by entity key in IWR_STATIC_ENTITY_CLASSIFICATION.
    Zone entities are looked up by translation_key in IWR_ZONE_ENTITY_CLASSIFICATION.
    Board entities all get IWR_BOARD_ENTITY_CLASSIFICATION.
    """
    classification: dict[str, tuple[str | None, bool]] = {}

    all_entities = {**sensors, **binary_sensors, **numbers, **selects, **times}
    for entity_key, config in all_entities.items():
        translation_key = config.get(
            "classification_key", config.get("translation_key", entity_key)
        )

        if entity_key in IWR_STATIC_ENTITY_CLASSIFICATION:
            classification[entity_key] = IWR_STATIC_ENTITY_CLASSIFICATION[entity_key]
        elif translation_key in IWR_ZONE_ENTITY_CLASSIFICATION:
            classification[entity_key] = IWR_ZONE_ENTITY_CLASSIFICATION[translation_key]
        elif translation_key.startswith("board_"):
            classification[entity_key] = IWR_BOARD_ENTITY_CLASSIFICATION
        # else: defaults to (None, True) at lookup time

    return classification


def get_iwr_device_config(
    zones: list[int] | None = None,
    features: dict[str, bool] | None = None,
    zone_details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the complete IWR device config for the given zone numbers (1-based)."""
    if zones is None:
        zones = [1]
    if features is None:
        features = {
            FEATURE_HYBRID: True,
            FEATURE_CASCADE: True,
            FEATURE_COOLING: True,
            FEATURE_BUFFER_TANK: True,
        }
    # Merge static + dynamic registers
    register_map = {
        **_IWR_STATIC_REGISTER_MAP,
        **_build_zone_registers(zones),
        **_build_board_registers(),
    }
    sensors = {
        **_IWR_STATIC_SENSORS,
        **_build_zone_sensors(zones),
        **_build_board_sensors(),
    }
    binary_sensors = {
        **_IWR_STATIC_BINARY_SENSORS,
        **_build_zone_binary_sensors(zones),
    }
    numbers = {**_IWR_STATIC_NUMBERS, **_build_zone_numbers(zones)}
    selects = {**_IWR_STATIC_SELECTS, **_build_zone_selects(zones)}
    times = _IWR_STATIC_TIMES
    climates = _build_zone_climates(zones)

    # Remove sensor entries for registers that now have number/select entities
    for key in list(sensors):
        suffix = key.split("_", 1)[1] if "_" in key else key
        if key in _WRITABLE_STATIC_SENSOR_KEYS or suffix in _WRITABLE_ZONE_SENSOR_KEYS:
            del sensors[key]

    register_map = _filter_iwr_register_map(register_map, features, zone_details)
    sensors = _filter_register_entities(sensors, register_map)
    binary_sensors = _filter_register_entities(binary_sensors, register_map)
    numbers = _filter_register_entities(numbers, register_map)
    selects = _filter_register_entities(selects, register_map)
    times = _filter_register_entities(times, register_map)
    climates = _filter_climate_entities(climates, register_map)

    return {
        "register_map": register_map,
        "sensors": sensors,
        "binary_sensors": binary_sensors,
        "numbers": numbers,
        "selects": selects,
        "times": times,
        "climates": climates,
        "enum_maps": IWR_ENUM_MAPS,
        "entity_classification": _build_entity_classification(
            sensors, binary_sensors, numbers, selects, times
        ),
    }
