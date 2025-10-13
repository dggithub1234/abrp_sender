"""Coordinator for ABRP Sender."""
from __future__ import annotations
import aiohttp
import logging
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_API_KEY, CONF_SCAN_INTERVAL
from homeassistant.helpers.event import async_track_time_interval
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL, ABRP_API_URL, CONF_ENABLED

_LOGGER = logging.getLogger(__name__)


class ABRPSenderCoordinator:
    """Coordinator class for periodic ABRP updates."""

    def __init__(self, hass: HomeAssistant, entry):
        self.hass = hass
        self.entry = entry
        self.api_key = entry.options.get(CONF_API_KEY, entry.data.get(CONF_API_KEY))
        self.enabled = entry.options.get(CONF_ENABLED, entry.data.get(CONF_ENABLED, True))
        self.interval = timedelta(
            seconds=entry.options.get(
                CONF_SCAN_INTERVAL, entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
            )
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
        self.enabled = data.get(CONF_ENABLED, True)

        if not self.enabled:
            _LOGGER.debug("ABRP Sender disabled — skipping data upload.")
            return

        payload = {"api_key": self.api_key}

        def get_value(entity_id):
            if not entity_id:
                return None
            state = self.hass.states.get(entity_id)
            if not state or state.state in ("unknown", "unavailable"):
                return None
            try:
                return float(state.state)
            except (ValueError, TypeError):
                return None

        # Standard sensors
        payload["soc"] = get_value(data.get("soc_sensor"))
        payload["speed"] = get_value(data.get("speed_sensor"))
        payload["power"] = get_value(data.get("power_sensor"))

        # Location handling
        lat = lon = None
        location_entity = data.get("location_entity")
        if location_entity:
            loc_state = self.hass.states.get(location_entity)
            if loc_state:
                try:
                    lat = float(loc_state.attributes.get("latitude"))
                    lon = float(loc_state.attributes.get("longitude"))
                except (TypeError, ValueError):
                    _LOGGER.debug("Location entity %s has invalid lat/lon", location_entity)

        # Fallback to separate sensors
        if lat is None:
            lat = get_value(data.get("latitude_sensor"))
        if lon is None:
            lon = get_value(data.get("longitude_sensor"))

        if lat is not None and lon is not None:
            payload["lat"] = lat
            payload["lon"] = lon

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
