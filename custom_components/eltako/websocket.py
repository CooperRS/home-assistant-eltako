import json
import logging

from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components import websocket_api


async def register_websockets(hass: HomeAssistant, config: ConfigEntry):
    websocket_api.async_register_command(hass, ws_info)


def _get_manifest_info():

    try:
        with open("manifest.json", "r") as file:
            response = json.load(file)
            logging.getLogger("eltako").info(f"info response: {response}")
    except:
        response = {}

@websocket_api.websocket_command({
    'type': 'eltako/info',
    'required': []
})
@websocket_api.async_response
async def ws_info(hass: HomeAssistant, connection, msg):
    
    response = await hass.async_add_executor_job(_get_manifest_info)

    # Send the response back
    connection.send_message(websocket_api.result_message(msg['id'], response))