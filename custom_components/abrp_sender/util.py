"""Utility functions for ABRP Sender."""
from __future__ import annotations
import aiohttp
import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from .const import ABRP_API_URL

_LOGGER = logging.getLogger(__name__)


async def get_gps_entities(hass: HomeAssistant) -> list[str]:
    """Return entities that likely provide latitude/longitude data."""
    entities = []
    entity_reg = er.async_get(hass)
    for entity in entity_reg.entities.values():
        # device_trackers, or sensors with "latitude" in name
        if entity.domain in ["device_tracker", "sensor"] and (
            "lat" in entity.entity_id or "location" in entity.entity_id
        ):
            entities.append(entity.entity_id)
    return entities


async def test_abrp_api_key(api_key: str) -> bool:
    """Check if ABRP API key is valid by sending a small test payload."""
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
