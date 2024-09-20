# # Class créer par Rivah
from django.urls import re_path
from base.consumers1 import LangflowConsumer  # Importez vos consumers WebSocket

websocket_urlpatterns = [
     re_path(r"^ws/socket-server/$", LangflowConsumer.as_asgi()),
]
