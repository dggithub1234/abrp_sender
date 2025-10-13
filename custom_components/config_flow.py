"""Config flow for ABRP Sender integration."""
from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_SCAN_INTERVAL
from homeassistant.helpers import selector
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .util import get_gps_entities, test_abrp_api_key


class ABRPSenderConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the ABRP Sender config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Initial setup."""
        if user_input is not None:
            valid = await test_abrp_api_key(user_input[CONF_API_KEY])
            if not valid:
                errors = {"base": "invalid_api"}
            else:
                return self.async_create_entry(title="ABRP Sender", data=user_input)
        else:
            errors = {}

        gps_entities = await get_gps_entities(self.hass)
        gps_selector = selector.EntitySelector(
            {"include_entities": gps_entities} if gps_entities else {"domain": "sensor"}
        )

        schema = vol.Schema({
            vol.Required(CONF_API_KEY): str,
            vol.Optional("soc_sensor"): selector.EntitySelector({"domain": "sensor"}),
            vol.Optional("speed_sensor"): selector.EntitySelector({"domain": "sensor"}),
            vol.Optional("latitude_sensor"): gps_selector,
            vol.Optional("longitude_sensor"): gps_selector,
            vol.Optional("power_sensor"): selector.EntitySelector({"domain": "sensor"}),
            vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(int, vol.Range(min=10, max=600))
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
            description_placeholders={"api_key": "Enter your ABRP API key."},
        )


class ABRPSenderOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for existing ABRP Sender config."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Handle options UI."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data = self.config_entry.data
        options = self.config_entry.options
        gps_entities = await get_gps_entities(self.hass)
        gps_selector = selector.EntitySelector(
            {"include_entities": gps_entities} if gps_entities else {"domain": "sensor"}
        )

        schema = vol.Schema({
            vol.Required(CONF_API_KEY, default=data.get(CONF_API_KEY)): str,
            vol.Optional("soc_sensor", default=options.get("soc_sensor", data.get("soc_sensor"))):
                selector.EntitySelector({"domain": "sensor"}),
            vol.Optional("speed_sensor", default=options.get("speed_sensor", data.get("speed_sensor"))):
                selector.EntitySelector({"domain": "sensor"}),
            vol.Optional("latitude_sensor", default=options.get("latitude_sensor", data.get("latitude_sensor"))):
                gps_selector,
            vol.Optional("longitude_sensor", default=options.get("longitude_sensor", data.get("longitude_sensor"))):
                gps_selector,
            vol.Optional("power_sensor", default=options.get("power_sensor", data.get("power_sensor"))):
                selector.EntitySelector({"domain": "sensor"}),
            vol.Optional(CONF_SCAN_INTERVAL, default=options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)):
                vol.All(int, vol.Range(min=10, max=600))
        })

        return self.async_show_form(step_id="init", data_schema=schema)
