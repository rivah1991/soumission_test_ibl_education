from channels.testing import WebsocketCommunicator
from django.test import TestCase
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from backend_django.asgi  import application  # Remplace 'myapp' par le nom de ton app
# websocket_urlpatterns

class WebSocketJWTTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='rivah', password='Naivo@1991')

    def generate_token(self):
        token = AccessToken.for_user(self.user)
        return str(token)

    async def test_websocket_connection_with_valid_jwt(self):
        token = self.generate_token()
        communicator = WebsocketCommunicator(application, f"/ws/socket-server/?token={token}")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_websocket_connection_with_invalid_jwt(self):
        invalid_token = "invalidtoken123"
        communicator = WebsocketCommunicator(application, f"/ws/socket-server/?token={invalid_token}")
        connected, subprotocol = await communicator.connect()
        self.assertFalse(connected)

    async def test_websocket_connection_without_jwt(self):
        communicator = WebsocketCommunicator(application, "/ws/socket-server/")
        connected, subprotocol = await communicator.connect()
        self.assertFalse(connected)
