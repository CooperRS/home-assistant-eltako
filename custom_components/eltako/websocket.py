import json
import os
from .const import *

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components import websocket_api

from .gateway import detect


async def register_websockets(hass: HomeAssistant, config: ConfigEntry):
    websocket_api.async_register_command(hass, ws_info)
    websocket_api.async_register_command(hass, ws_usb_ports)


def _get_manifest_info():
    try:
        dir_path = os.path.dirname(__file__)
        with open(os.path.join(dir_path, "manifest.json"), "r") as file:
            response = json.load(file)
            # LOGGER.info(f"info response: {response}")
    except Exception as e:
        LOGGER.error("Cannot read manifest.json", exc_info=True, stack_info=True)
        response = {}

    return response

def _get_configured_gateways(hass: HomeAssistant):
    result = []
    for k in hass.data[DATA_ELTAKO]:
        if k.startswith('gateway'):
            result.append(hass.data[DATA_ELTAKO][k])
    return result


@websocket_api.websocket_command({
    'type': 'eltako/info',
    'required': []
})
@websocket_api.async_response
async def ws_info(hass: HomeAssistant, connection, msg):
    
    # LOGGER.debug("Call WS eltako/info")

    response = await hass.async_add_executor_job(_get_manifest_info)

    # Send the response back
    connection.send_message(websocket_api.result_message(msg['id'], response))


@websocket_api.websocket_command({
    'type': 'eltako/potential_usb_ports',
    'required': []
})
@websocket_api.async_response
async def ws_usb_ports(hass: HomeAssistant, connection, msg):
    
    response = await hass.async_add_executor_job(detect)

    # Send the response back
    connection.send_message(websocket_api.result_message(msg['id'], response))

@websocket_api.websocket_command({
    'type': 'eltako/configured_gateways',
    'required': []
})
@websocket_api.async_response
async def ws_configured_gateways(hass: HomeAssistant, connection, msg):
    
    response = await _get_configured_gateways(hass)

    # Send the response back
    connection.send_message(websocket_api.result_message(msg['id'], response))