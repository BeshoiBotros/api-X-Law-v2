import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from chatapp.routing import chat_websockets
from XLaw.JWTMiddleWare import JWTAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'XLaw.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    'websocket' : JWTAuthMiddleware(URLRouter(chat_websockets))
})
