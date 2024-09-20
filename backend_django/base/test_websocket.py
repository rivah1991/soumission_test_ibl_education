# test_websocket.py
from channels.testing import WebsocketCommunicator
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from backend_django.asgi import application  # Modifier selon le nom de votre projet
import json
import httpx
from unittest.mock import patch

class LangflowConsumerTestCase(TestCase):
    """
    Teste le LangflowConsumer pour vérifier la connexion WebSocket,
    l'envoi de messages et la réception des réponses de Langflow.
    """

    @patch('base.chat.LangflowConsumer.get_huggingface_response')
    def test_websocket_connection_and_message(self, mock_get_huggingface_response):
        """
        Teste la connexion WebSocket et la réception des messages en simulant
        la réponse de Langflow.
        """
        # Créer un utilisateur pour générer un token JWT
        user = User.objects.create_user(username="testuser", password="testpassword")
        
        # Générer un token JWT valide pour cet utilisateur
        token = str(AccessToken.for_user(user))

        # Simuler la réponse de Langflow
        mock_get_huggingface_response.return_value = "Mocked response from Langflow"

        # Créer un WebsocketCommunicator pour tester la connexion
        communicator = WebsocketCommunicator(
            application, f"/ws/langflow/?token={token}"
        )

        # Connecter
        connected, _ = communicator.connect()
        self.assertTrue(connected)  # Vérifier si la connexion est réussie

        # Envoyer un message
        communicator.send_json_to({
            'message': 'What is the weather today?'
        })

        # Recevoir la réponse
        response = communicator.receive_json_from()
        self.assertIn('message', response)  # Vérifier la présence de la réponse
        self.assertEqual(response['message'], "Mocked response from Langflow")  # Vérifier le contenu de la réponse

        # Déconnecter
        communicator.disconnect()
