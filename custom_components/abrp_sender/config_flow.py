"""Config flow for ABRP Sender integration."""
from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_SCAN_INTERVAL
from homeassistant.helpers import selector
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL, CONF_ENABLED
from .util import get_gps_entities, test_abrp_api_key


class ABRPSenderConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the ABRP Sender config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Initial setup."""
        errors = {}
        if user_input is not None:
            valid = await test_abrp_api_key(user_input[CONF_API_KEY])
            if not valid:
                errors["base"] = "invalid_api"
            else:
                return self.async_create_entry(title="ABRP Sender", data=user_input)

        # build location selector using entities that actually have lat/lon attributes
        gps_entities = await get_gps_entities(self.hass)
        if gps_entities:
            location_selector = selector.EntitySelector({"include_entities": gps_entities})
        else:
            # fallback: let user pick device_tracker entities (common)
            location_selector = selector.EntitySelector({"domain": "device_tracker"})

        schema = vol.Schema(
            {
                vol.Required(CONF_API_KEY): str,
                vol.Optional(CONF_ENABLED, default=True): bool,
                vol.Optional("soc_sensor"): selector.EntitySelector({"domain": "sensor"}),
                vol.Optional("speed_sensor"): selector.EntitySelector({"domain": "sensor"}),
                # Single location entity (device_tracker or sensor with lat/lon attributes)
                vol.Optional("location_entity"): location_selector,
                # Optional legacy lat/lon sensor fields (keep as fallback)
                vol.Optional("latitude_sensor"): selector.EntitySelector({"domain": "sensor"}),
                vol.Optional("longitude_sensor"): selector.EntitySelector({"domain": "sensor"}),
                vol.Optional("power_sensor"): selector.EntitySelector({"domain": "sensor"}),
                vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(
                    int, vol.Range(min=10, max=600)
                ),
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
