"""Coordinator for ABRP Sender."""
from __future__ import annotations
import aiohttp
import logging
import json
import urllib.parse
import time
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL, ABRP_API_URL, ABRP_API_KEY, CONF_ENABLED, CONF_API_TOKEN

_LOGGER = logging.getLogger(__name__)

class ABRPSenderCoordinator:
    """Coordinator class for periodic ABRP updates."""

    def __init__(self, hass: HomeAssistant, entry):
        self.hass = hass
        self.entry = entry
        self.token = entry.data.get(CONF_API_TOKEN)
        self.enabled = entry.data.get(CONF_ENABLED, True)
        self.interval = timedelta(seconds=entry.data.get("scan_interval", DEFAULT_SCAN_INTERVAL))
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
        """Send sensor data to ABRP using URL-encoded query parameters."""
        if not self.enabled:
            _LOGGER.debug("ABRP Sender disabled — skipping data upload.")
            return

        data = {**self.entry.data, **self.entry.options}

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

        # Location
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

        if lat is None:
            lat = get_value(data.get("latitude_sensor"))
        if lon is None:
            lon = get_value(data.get("longitude_sensor"))

        # Build telemetry
        tlm = {
            "utc": float(time.time()),
            "soc": get_value(data.get("soc_sensor")),
            "speed": get_value(data.get("speed_sensor")),
            "power": get_value(data.get("power_sensor")),
            "odometer": get_value(data.get("odometer_sensor")) or 0,
            "lat": lat,
            "lon": lon,
            "is_parked": False,  # optional, could be derived from movement sensor
        }

        # Remove None values
        tlm = {k: v for k, v in tlm.items() if v is not None}

        tlm_json = json.dumps(tlm)
        tlm_encoded = urllib.parse.quote(tlm_json)

        url = f"{ABRP_API_URL}?api_key={ABRP_API_KEY}&token={self.token}&tlm={tlm_encoded}"
        headers = {"Content-Type": "charset=utf-8; application/x-www-form-urlencoded"}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=headers) as resp:
                    resp_text = await resp.text()
                    if resp.status != 200:
                        _LOGGER.warning("ABRP send failed (%s): %s", resp.status, resp_text)
                    else:
                        _LOGGER.debug("ABRP data sent successfully: %s", resp_text)
            except Exception as e:
                _LOGGER.error("Error sending data to ABRP: %s", e)
