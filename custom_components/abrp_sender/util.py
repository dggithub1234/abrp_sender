"""Utility functions for ABRP Sender."""
from __future__ import annotations
import aiohttp
import logging
from homeassistant.core import HomeAssistant
from .const import ABRP_API_URL

_LOGGER = logging.getLogger(__name__)


async def get_gps_entities(hass: HomeAssistant) -> list[str]:
    """
    Return entities that provide latitude/longitude attributes.
    Includes device_tracker and other entities with numeric lat/lon.
    """
    entities: list[str] = []
    for state in hass.states.async_all():
        attrs = state.attributes
        if isinstance(attrs.get("latitude"), (float, int)) and isinstance(attrs.get("longitude"), (float, int)):
            entities.append(state.entity_id)
    entities.sort()
    return entities


async def test_abrp_api_key(api_key: str) -> bool:
    """Send a test payload to ABRP to validate API key."""
    payload = {"api_key": api_key, "soc": 50, "lat": 0, "lon": 0}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(ABRP_API_URL, json=payload) as resp:
                text = await resp.text()
                if resp.status == 200:
                    _LOGGER.debug("ABRP API test success: %s", text)
                    return True
                _LOGGER.error("ABRP API test failed (%s): %s", resp.status, text)
                return False
    except Exception as e:
        _LOGGER.error("Error testing ABRP API: %s", e)
        return False
