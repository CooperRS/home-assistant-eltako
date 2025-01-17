from aiohttp import web
from homeassistant.components.http import HomeAssistantView

class InfoPageView(HomeAssistantView):
    """Serve a custom page."""

    url = "/eltako"
    name = "eltako"
    requires_auth = True

    async def get(self, request):
        """Handle GET requests."""
        # Example: Serve a simple HTML page embedding the external URL
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>My External Page</title>
            <style>
                body, html { margin: 0; padding: 0; height: 100%; }
                iframe { width: 100%; height: 100%; border: none; }
            </style>
        </head>
        <body>
            <iframe src="http://localhost:5173"></iframe>
        </body>
        </html>
        """
        return web.Response(body=html_content, content_type="text/html")