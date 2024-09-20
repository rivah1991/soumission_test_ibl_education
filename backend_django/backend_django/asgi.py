# import os
# # from django.conf.urls import url
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')

# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# django_asgi_app = get_asgi_application()

# from channels.auth import AuthMiddlewareStack
# # import backend_django.routing
# from backend_django.routing import websocket_urlpatterns
# application = ProtocolTypeRouter(
#     {
#         "http": django_asgi_app,
#         'websocket': AuthMiddlewareStack(
#             websocket_urlpatterns
         
#         )
#     }
# )
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from base.routing import websocket_urlpatterns  # Assurez-vous que ce chemin est correct

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_django.settings')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        ),
    }
)
