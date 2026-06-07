"""Shared IWR setup detection helpers for config and runtime setup."""

from __future__ import annotations

import logging
from typing import Any, Final

from .const import (
    FEATURE_BUFFER_TANK,
    FEATURE_CASCADE,
    FEATURE_COOLING,
    FEATURE_HYBRID,
)
from .devices.iwr import ZONE_ADDR_OFFSET, ZONE_FUNCTION_BASE_ADDR, ZONE_TYPE_BASE_ADDR

_LOGGER = logging.getLogger(__name__)

ZONE_ROLE_HEATING: Final = "heating"
ZONE_ROLE_DHW: Final = "dhw"
ZONE_ROLE_INACTIVE: Final = "inactive"

ZONE_TYPE_LABELS: Final[dict[int, str]] = {
    0: "Inactive",
    1: "Heating circuit",
    2: "Heating circuit + cooling",
    3: "Domestic hot water (DHW)",
    4: "Process heat",
    5: "Swimming pool",
    254: "Other",
    255: "Inactive / undefined",
}

ZONE_FUNCTION_LABELS: Final[dict[int, str]] = {
    0: "Disabled",
    1: "Direct circuit",
    2: "Mixing circuit",
    3: "Swimming pool",
    4: "High-temperature circuit",
    5: "Fan convector",
    6: "DHW tank",
    7: "Electrical DHW",
    8: "Time program",
    9: "Process heat",
    10: "Layered DHW",
    11: "Internal DHW tank",
    12: "Commercial DHW tank",
    13: "Occupied",
    254: "Primary DHW",
    255: "Undefined",
}

ZONE_TYPE_INACTIVE: Final[frozenset[int]] = frozenset({0, 255})
ZONE_FUNCTION_DHW: Final[frozenset[int]] = frozenset({6, 7, 10, 11, 12, 254})

_RAW_SENTINELS_16: Final[frozenset[int]] = frozenset({0x00FF, 0xFFFF, 0x8000})
_RAW_SENTINELS_32: Final[frozenset[int]] = frozenset({0xFFFFFFFF, 0x80000000})


async def _read_holding_registers(
    client: Any,
    unit_id: int,
    address: int,
    count: int = 1,
) -> list[int] | None:
    """Read one or more holding registers, returning None on any read failure."""
    try:
        result = await client.read_holding_registers(
            address=address,
            count=count,
            device_id=unit_id,
        )
    except Exception:
        _LOGGER.exception("IWR setup detection failed reading holding register %s", address)
        return None

    if result.isError():
        _LOGGER.debug(
            "IWR setup detection got Modbus error at address %s: %s",
            address,
            result,
        )
        return None

    return list(result.registers)


def _combine_u32(registers: list[int]) -> int | None:
    """Combine two 16-bit Modbus registers into an unsigned 32-bit value."""
    if len(registers) != 2:
        return None
    return ((registers[0] & 0xFFFF) << 16) | (registers[1] & 0xFFFF)


def _is_raw_sentinel(registers: list[int] | None) -> bool:
    """Return True when raw register words represent a no-data sentinel."""
    if not registers:
        return True

    if len(registers) == 1:
        return (registers[0] & 0xFFFF) in _RAW_SENTINELS_16

    if len(registers) == 2:
        raw32 = _combine_u32(registers)
        return raw32 in _RAW_SENTINELS_32

    return False


def _has_meaningful_value(registers: list[int] | None) -> bool:
    """Return True when a probe result looks like actual data."""
    if registers is None or _is_raw_sentinel(registers):
        return False
    return any((word & 0xFFFF) != 0 for word in registers)


def classify_zone_role(zone_type: int, zone_function: int) -> str:
    """Classify a detected zone into heating, DHW, or inactive."""
    if zone_type in ZONE_TYPE_INACTIVE:
        return ZONE_ROLE_INACTIVE
    if zone_type == 3 or zone_function in ZONE_FUNCTION_DHW:
        return ZONE_ROLE_DHW
    return ZONE_ROLE_HEATING


async def detect_zones(client: Any, unit_id: int) -> list[dict[str, Any]]:
    """Read zone type/function registers for all 12 zones."""
    results: list[dict[str, Any]] = []
    for index in range(12):
        zone_number = index + 1
        type_addr = ZONE_TYPE_BASE_ADDR + ZONE_ADDR_OFFSET * index
        func_addr = ZONE_FUNCTION_BASE_ADDR + ZONE_ADDR_OFFSET * index

        zone_type = 0
        zone_function = 0

        type_registers = await _read_holding_registers(client, unit_id, type_addr)
        if type_registers:
            zone_type = type_registers[0]

        function_registers = await _read_holding_registers(client, unit_id, func_addr)
        if function_registers:
            zone_function = function_registers[0]

        role = classify_zone_role(zone_type, zone_function)
        active = role != ZONE_ROLE_INACTIVE
        type_label = ZONE_TYPE_LABELS.get(zone_type, f"type {zone_type}")
        func_label = ZONE_FUNCTION_LABELS.get(zone_function, f"func {zone_function}")

        if active:
            label = f"Zone {zone_number} — {type_label}, {func_label}"
        else:
            label = f"Zone {zone_number} — {type_label}"

        results.append(
            {
                "zone": zone_number,
                "zone_type": zone_type,
                "zone_function": zone_function,
                "role": role,
                "active": active,
                "cooling_capable": zone_type == 2 or zone_function == 5,
                "label": label,
            }
        )

    return results


def _zone_details_from_zone_info(zone_info: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Return persistent per-zone details keyed by zone number string."""
    return {
        str(item["zone"]): {
            "zone_type": item["zone_type"],
            "zone_function": item["zone_function"],
            "role": item["role"],
            "active": item["active"],
            "cooling_capable": item["cooling_capable"],
        }
        for item in zone_info
    }


async def detect_iwr_features(client: Any, unit_id: int) -> dict[str, bool]:
    """Detect optional IWR feature groups from representative registers."""
    features = {
        FEATURE_HYBRID: False,
        FEATURE_CASCADE: False,
        FEATURE_COOLING: False,
        FEATURE_BUFFER_TANK: False,
    }

    # Hybrid-related registers and status bits.
    for address in (465, 466, 467, 470, 471, 9204):
        registers = await _read_holding_registers(client, unit_id, address)
        if _has_meaningful_value(registers):
            features[FEATURE_HYBRID] = True
            break

    # Cascade-specific discovery/status registers.
    for address in (7143, 7145, 7146, 7154, 7207, 7208):
        registers = await _read_holding_registers(client, unit_id, address)
        if _has_meaningful_value(registers):
            features[FEATURE_CASCADE] = True
            break

    cooling_registers = await _read_holding_registers(client, unit_id, 502)
    if cooling_registers and cooling_registers[0] in {1, 2}:
        features[FEATURE_COOLING] = True

    buffer_enable = await _read_holding_registers(client, unit_id, 197)
    if buffer_enable and buffer_enable[0] == 1:
        features[FEATURE_BUFFER_TANK] = True
    else:
        for address in (7600, 7601, 7602, 7603):
            registers = await _read_holding_registers(client, unit_id, address)
            if _has_meaningful_value(registers):
                features[FEATURE_BUFFER_TANK] = True
                break

    return features


async def detect_iwr_setup(client: Any, unit_id: int) -> dict[str, Any]:
    """Detect zone layout and optional feature groups for an IWR installation."""
    zone_info = await detect_zones(client, unit_id)
    zone_details = _zone_details_from_zone_info(zone_info)
    active_zones = [item["zone"] for item in zone_info if item["active"]]
    features = await detect_iwr_features(client, unit_id)

    return {
        "zone_info": zone_info,
        "zone_details": zone_details,
        "zones": active_zones,
        "features": features,
    }
