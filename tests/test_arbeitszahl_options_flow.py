"""Exercise the Arbeitszahl OptionsFlow step with small HA-facing fakes."""

import importlib.util
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_flow(monkeypatch):
    package_name = "custom_components.broetje_heating"
    package = types.ModuleType(package_name)
    package.__path__ = [str(ROOT / "custom_components/broetje_heating")]
    monkeypatch.setitem(sys.modules, package_name, package)

    voluptuous = types.ModuleType("voluptuous")

    class Marker:
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs

        def __hash__(self):
            return id(self)

    voluptuous.Schema = lambda value: value
    voluptuous.Required = Marker
    voluptuous.Optional = Marker
    voluptuous.All = lambda *args: args
    voluptuous.Range = lambda **kwargs: kwargs
    voluptuous.Any = lambda *args: args
    monkeypatch.setitem(sys.modules, "voluptuous", voluptuous)

    homeassistant = types.ModuleType("homeassistant")
    homeassistant.__path__ = []
    config_entries = types.ModuleType("homeassistant.config_entries")

    class ConfigFlow:
        def __init_subclass__(cls, **kwargs):
            return super().__init_subclass__()

    class OptionsFlow:
        def async_show_form(self, **kwargs):
            return {"type": "form", **kwargs}

        def async_create_entry(self, data):
            return {"type": "create_entry", "data": data}

    config_entries.ConfigEntry = type("ConfigEntry", (), {})
    config_entries.ConfigFlow = ConfigFlow
    config_entries.ConfigFlowResult = dict
    config_entries.OptionsFlow = OptionsFlow
    monkeypatch.setitem(sys.modules, "homeassistant", homeassistant)
    monkeypatch.setitem(sys.modules, "homeassistant.config_entries", config_entries)

    ha_const = types.ModuleType("homeassistant.const")
    ha_const.CONF_HOST = "host"
    ha_const.CONF_PORT = "port"
    monkeypatch.setitem(sys.modules, "homeassistant.const", ha_const)

    selector = types.ModuleType("homeassistant.helpers.selector")
    for name in (
        "EntityFilterSelectorConfig",
        "EntitySelector",
        "EntitySelectorConfig",
        "NumberSelector",
        "NumberSelectorConfig",
        "SelectSelector",
        "SelectSelectorConfig",
    ):
        setattr(
            selector, name, type(name, (), {"__init__": lambda self, *a, **k: None})
        )
    selector.SelectOptionDict = dict
    selector.NumberSelectorMode = types.SimpleNamespace(BOX="box")
    selector.SelectSelectorMode = types.SimpleNamespace(LIST="list")
    helpers = types.ModuleType("homeassistant.helpers")
    helpers.__path__ = []
    monkeypatch.setitem(sys.modules, "homeassistant.helpers", helpers)
    monkeypatch.setitem(sys.modules, "homeassistant.helpers.selector", selector)

    devices = types.ModuleType(f"{package_name}.devices")
    devices.CONF_DEVICE_TYPE = "device_type"
    devices.DEVICE_MODELS = {}
    devices.DeviceType = types.SimpleNamespace(
        ISR=types.SimpleNamespace(value="isr"), IWR=types.SimpleNamespace(value="iwr")
    )
    monkeypatch.setitem(sys.modules, f"{package_name}.devices", devices)
    iwr_setup = types.ModuleType(f"{package_name}.iwr_setup")
    iwr_setup.SerializedModbusDiscoveryReader = type(
        "SerializedModbusDiscoveryReader", (), {}
    )
    iwr_setup.ZONE_ROLE_HEATING = "heating"
    iwr_setup.detect_iwr_setup = lambda *args, **kwargs: None
    monkeypatch.setitem(sys.modules, f"{package_name}.iwr_setup", iwr_setup)

    path = ROOT / "custom_components/broetje_heating/config_flow.py"
    spec = importlib.util.spec_from_file_location(
        f"{package_name}.config_flow_under_test", path
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    module.__package__ = package_name
    monkeypatch.setitem(sys.modules, spec.name, module)
    spec.loader.exec_module(module)
    return module


def _flow(module, monkeypatch):
    flow = module.BroetjeOptionsFlow()
    flow.config_entry = types.SimpleNamespace(
        options={}, entry_id="entry", data={"device_type": "iwr"}
    )
    updates = []

    class ConfigEntries:
        def async_update_entry(self, entry, *, options):
            entry.options = options
            updates.append(options)

        async def async_reload(self, entry_id):
            return None

    class Hass:
        config_entries = ConfigEntries()

        def async_create_task(self, coro):
            coro.close()

    flow.hass = Hass()
    flow._updates = updates
    return flow


def test_options_flow_rejects_one_sided_baseline_and_saves_pair(monkeypatch) -> None:
    module = _load_flow(monkeypatch)
    flow = _flow(module, monkeypatch)

    rejected = __import__("asyncio").run(
        flow.async_step_arbeitszahl({"arbeitszahl_electrical_baseline_kwh": 123.0})
    )
    assert rejected["type"] == "form"
    assert rejected["errors"] == {"base": "baseline_pair_required"}
    assert flow._updates == []

    saved = __import__("asyncio").run(
        flow.async_step_arbeitszahl(
            {
                "arbeitszahl_electrical_baseline_kwh": 123.0,
                "arbeitszahl_thermal_baseline_kwh": 456.0,
            }
        )
    )
    assert saved["type"] == "create_entry"
    assert saved["data"]["arbeitszahl_electrical_baseline_kwh"] == 123.0
    assert saved["data"]["arbeitszahl_thermal_baseline_kwh"] == 456.0
    assert len(flow._updates) == 1
