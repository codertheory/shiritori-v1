"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/

"""
import os
import sys
from pathlib import Path

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

django_app = get_asgi_application()

# Routing
from shiritori.game.routing import \
    websocket_patterns as game_websocket_patterns  # pylint: disable=wrong-import-position

# This allows easy placement of apps within the interior
# backend directory.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR))

# If DJANGO_SETTINGS_MODULE is unset, default to the local settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

websocket_patterns = [
    *game_websocket_patterns,
]

application = ProtocolTypeRouter({
    "http": django_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_patterns)
    ),
})
