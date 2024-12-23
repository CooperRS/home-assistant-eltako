from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry


def register_websockets(hass: HomeAssistant, config: ConfigEntry):
    hass.components.websocket_api.async_register_command(handle_ws_info)


@websocket_api.websocket_command({
    'type': 'info',
    'required': []
})
@websocket_api.async_response
async def handle_ws_info(hass: HomeAssistant, connection, msg):
    
    response = {
        'info': 'info-message'
    }

    # Send the response back
    connection.send_message(websocket_api.result_message(msg['id'], response))