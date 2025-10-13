"""Utility functions for ABRP Sender."""
from __future__ import annotations
import logging
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

async def get_gps_entities(hass: HomeAssistant) -> list[str]:
    """Return entities that provide latitude/longitude attributes."""
    entities: list[str] = []
    for state in hass.states.async_all():
        attrs = state.attributes
        if isinstance(attrs.get("latitude"), (float, int)) and isinstance(attrs.get("longitude"), (float, int)):
            entities.append(state.entity_id)
    entities.sort()
    return entities
