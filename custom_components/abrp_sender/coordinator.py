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

        # Standard numeric sensors
        payload["soc"] = get_value(data.get("soc_sensor"))
        payload["speed"] = get_value(data.get("speed_sensor"))
        payload["power"] = get_value(data.get("power_sensor"))

        # Location handling: prefer single location_entity with attributes
        lat = None
        lon = None
        location_entity = data.get("location_entity")
        if location_entity:
            loc_state = self.hass.states.get(location_entity)
            if loc_state:
                lat_attr = loc_state.attributes.get("latitude")
                lon_attr = loc_state.attributes.get("longitude")
                # Accept numbers or numeric strings
                try:
                    if lat_attr is not None:
                        lat = float(lat_attr)
                    if lon_attr is not None:
                        lon = float(lon_attr)
                except (TypeError, ValueError):
                    _LOGGER.debug("Location entity %s has non-numeric lat/lon attrs", location_entity)

        # Fallback to separate sensors if location_entity not provided or invalid
        if lat is None:
            lat = get_value(data.get("latitude_sensor"))
        if lon is None:
            lon = get_value(data.get("longitude_sensor"))

        if lat is not None and lon is not None:
            payload["lat"] = lat
            payload["lon"] = lon

        # Filter empty values
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
