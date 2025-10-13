"""Config flow for ABRP Sender integration."""
from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_SCAN_INTERVAL
from homeassistant.helpers import selector
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL


class ABRPSenderConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ABRP Sender."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial setup step."""
        if user_input is not None:
            return self.async_create_entry(title="ABRP Sender", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_API_KEY): str,
            vol.Optional("soc_sensor"): selector.EntitySelector({"domain": "sensor"}),
            vol.Optional("speed_sensor"): selector.EntitySelector({"domain": "sensor"}),
            vol.Optional("latitude_sensor"): selector.EntitySelector({"domain": "sensor"}),
            vol.Optional("longitude_sensor"): selector.EntitySelector({"domain": "sensor"}),
            vol.Optional("power_sensor"): selector.EntitySelector({"domain": "sensor"}),
            vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(int, vol.Range(min=10, max=600))
        })

        return self.async_show_form(step_id="user", data_schema=schema)


class ABRPSenderOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for an existing entry."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data = self.config_entry.data
        options = self.config_entry.options

        schema = vol.Schema({
            vol.Required(CONF_API_KEY, default=data.get(CONF_API_KEY)): str,
            vol.Optional("soc_sensor", default=options.get("soc_sensor", data.get("soc_sensor"))):
                selector.EntitySelector({"domain": "sensor"}),
            vol.Optional("speed_sensor", default=options.get("speed_sensor", data.get("speed_sensor"))):
                selector.EntitySelector({"domain": "sensor"}),
            vol.Optional("latitude_sensor", default=options.get("latitude_sensor", data.get("latitude_sensor"))):
                selector.EntitySelector({"domain": "sensor"}),
            vol.Optional("longitude_sensor", default=options.get("longitude_sensor", data.get("longitude_sensor"))):
                selector.EntitySelector({"domain": "sensor"}),
            vol.Optional("power_sensor", default=options.get("power_sensor", data.get("power_sensor"))):
                selector.EntitySelector({"domain": "sensor"}),
            vol.Optional(CONF_SCAN_INTERVAL, default=options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)):
                vol.All(int, vol.Range(min=10, max=600))
        })

        return self.async_show_form(step_id="init", data_schema=schema)


# Register options flow
async def async_get_options_flow(config_entry):
    return ABRPSenderOptionsFlowHandler(config_entry)
