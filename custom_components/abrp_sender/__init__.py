"""ABRP Sender integration for Home Assistant."""
from __future__ import annotations
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_API_TOKEN, CONF_ENABLED
from .coordinator import ABRPSenderCoordinator
from .config_flow import ABRPSenderOptionsFlowHandler

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = []  # No platforms, everything handled by coordinator


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up ABRP Sender integration (YAML not supported)."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up ABRP Sender from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Create coordinator
    coordinator = ABRPSenderCoordinator(hass, entry)
    await coordinator.async_setup()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    _LOGGER.debug("ABRP Sender integration loaded for entry_id: %s", entry.entry_id)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    coordinator: ABRPSenderCoordinator = hass.data[DOMAIN].pop(entry.entry_id, None)
    if coordinator:
        await coordinator.async_unload()
        _LOGGER.debug("ABRP Sender coordinator unloaded for entry_id: %s", entry.entry_id)
    return True


async def async_get_options_flow(config_entry):
    """Return the options flow handler for the integration."""
    return ABRPSenderOptionsFlowHandler(config_entry)
