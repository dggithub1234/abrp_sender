"""Coordinator for ABRP Sender."""
from __future__ import annotations
import aiohttp
import logging
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_API_KEY, CONF_SCAN_INTERVAL
from homeassistant.helpers.event import async_track_time_interval
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL, ABRP_API_URL

_LOGGER = logging.getLogger(__name__)


class ABRPSenderCoordinator:
    def __init__(self, hass: HomeAssistant, entry):
        self.hass = hass
        self.entry = entry
        self.api_key = entry.options.get(CONF_API_KEY, entry.data.get(CONF_API_KEY))
        self.interval = timedelta(
            seconds=entry.options.get(CONF_SCAN_INTERVAL, entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))
        )
        self._unsub = None

    async def async_setup(self):
        """Start periodic updates."""
        self._unsub = async_track_time_interval(self.hass, self._async_send_data, self.interval)

    async def async_unload(self):
        """Unload periodic task."""
        if self._unsub:
            self._unsub()
            self._unsub = None

    async def _async_send_data(self, now):
        """Send sensor data to ABRP."""
        data = {**self.entry.data, **self.entry.options}
        payload = {"api_key": self.api_key}

        def get_value(entity_id):
            state = self.hass.states.get(entity_id)
            return float(state.state) if state and state.state not in ("unknown", "unavailable") else None

        payload["soc"] = get_value(data.get("soc_sensor"))
        payload["speed"] = get_value(data.get("speed_sensor"))
        payload["power"] = get_value(data.get("power_sensor"))
        payload["lat"] = get_value(data.get("latitude_sensor"))
        payload["lon"] = get_value(data.get("longitude_sensor"))

        payload = {k: v for k, v in payload.items() if v is not None}

        if len(payload) <= 1:
            _LOGGER.debug("No valid data to send yet.")
            return

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(ABRP_API_URL, json=payload) as resp:
                    if resp.status != 200:
                        _LOGGER.warning("ABRP send failed (%s): %s", resp.status, await resp.text())
                    else:
                        _LOGGER.debug("ABRP data sent successfully: %s", payload)
            except Exception as e:
                _LOGGER.error("Error sending data to ABRP: %s", e)
