import json
import os
from .const import *

from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components import websocket_api


async def register_websockets(hass: HomeAssistant, config: ConfigEntry):
    websocket_api.async_register_command(hass, ws_info)


def _get_manifest_info():
    try:
        dir_path = os.path.dirname(__file__)
        with open(os.path.join(dir_path, "manifest.json"), "r") as file:
            response = json.load(file)
            LOGGER.info(f"info response: {response}")
    except Exception as e:
        LOGGER.error("Cannot read manifest.json", exc_info=True, stack_info=True)
        response = {}

    return response


@websocket_api.websocket_command({
    'type': 'eltako/info',
    'required': []
})
@websocket_api.async_response
async def ws_info(hass: HomeAssistant, connection, msg):
    
    LOGGER.debug("Call WS eltako/info")

    response = await hass.async_add_executor_job(_get_manifest_info)

    LOGGER.debug(f"version {response['version']}")

    # Send the response back
    connection.send_message(websocket_api.result_message(msg['id'], response))