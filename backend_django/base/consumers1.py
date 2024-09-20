import json
import aiohttp
import warnings
import logging
from typing import Optional
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

# Configuration du logger
logger = logging.getLogger(__name__)

# Importation du module upload_file depuis Langflow si disponible
try:
    from langflow.load import upload_file
except ImportError:
    warnings.warn("Langflow provides a function to help you upload files to the flow. Please install langflow to use it.")
    upload_file = None

class LangflowConsumer(AsyncWebsocketConsumer):
    def __init__(self, base_api_url: str = "http://chat_app_langflow:7860", flow_id: str = "aa2ba4f0-2573-4e52-aba8-117ca1bc019a"):
        """
        Initialisation de la classe LangflowConsumer.
        :param base_api_url: L'URL de base de l'API Langflow
        :param flow_id: L'ID du flow Langflow
        """
        self.base_api_url = base_api_url
        self.flow_id = flow_id
        self.endpoint = ""  # Peut être configuré dans les paramètres du flow
        self.tweaks = {
              "Prompt-B5He1": {},
              "ChatOutput-9Tl1t": {},
              "HuggingFaceModel-pmzcj": {},
              "ChatInput-RdX5F": {}
        }
        self.user = None  # Associer la connexion à un utilisateur spécifique
        self.sent_messages = set()  # Initialisation des messages envoyés
        super().__init__()

    async def connect(self):
        query_string = self.scope['query_string'].decode()
        token = self.get_token_from_query_string(query_string)

        if token and await self.is_valid_token(token):
            # Associer l'utilisateur connecté à la session WebSocket
            self.user = await self.get_user_from_token(token)
            if self.user:
                self.room_name = 'langflow_room'
                self.room_group_name = f'chat_{self.room_name}_{self.user.id}'  # Associer la room à l'utilisateur

                # Joindre l'utilisateur au groupe
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
                await self.accept()
            else:
                await self.close()
        else:
            # Fermer la connexion si le token est invalide
            await self.close()

    async def disconnect(self, close_code):
        # Retirer l'utilisateur du groupe
        if self.user:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({'error': 'Invalid JSON'}))
            return

        message = text_data_json.get('message', '')

        if message and self.user:
            # Vérifiez si le message a déjà été traité
            if message not in self.sent_messages:
                self.sent_messages.add(message)
                response = await self.get_langflow_response(message)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': response
                    }
                )
            else:
                await self.send(text_data=json.dumps({'error': 'Message already processed'}))
        else:
            await self.send(text_data=json.dumps({'error': 'No message or invalid user'}))

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @sync_to_async
    def is_valid_token(self, token):
        """
        Validation du token JWT
        """
        try:
            UntypedToken(token)
            return True
        except (InvalidToken, TokenError):
            return False

    @sync_to_async
    def get_user_from_token(self, token):
        """
        Récupérer l'utilisateur associé à un token JWT valide.
        """
        try:
            UntypedToken(token)
            User = get_user_model()
            user_id = UntypedToken(token).payload['user_id']
            return User.objects.get(id=user_id)
        except (InvalidToken, TokenError, User.DoesNotExist):
            return None

    async def get_langflow_response(self, message):
        """
        Interagit avec l'API Langflow pour obtenir une réponse à partir du message reçu.
        Renvoie la réponse de Langflow.
        """
        api_url = f"{self.base_api_url}/api/v1/run/{self.endpoint or self.flow_id}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "input_value": message,
            "output_type": "chat",
            "input_type": "chat",
            "tweaks": self.tweaks,
            "max_length": 150
        }
        
        # Log pour le message et les détails de la requête
        logger.info(f"Envoi de la requête à l'API Langflow")
        logger.info(f"URL: {api_url}")
        logger.info(f"Payload: {payload}")
        logger.info(f"Headers: {headers}")

        try:
            # Appel API
            response = await self.async_post(api_url, payload, headers)
            
            # Log pour la réponse brute
            logger.info(f"Réponse brute de l'API: {response}")

            # Vérification que la réponse est bien un dictionnaire avec les clés attendues
            if isinstance(response, dict):
                outputs = response.get('outputs', [])
                logger.info(f"Sorties de la réponse: {outputs}")
                
                if outputs:
                    first_output = outputs[0].get('outputs', [])
                    logger.info(f"Première sortie: {first_output}")
                    
                    if first_output:
                        results = first_output[0].get('results', {})
                        logger.info(f"Résultats: {results}")
                        
                        message_obj = results.get('message', {})
                        text = message_obj.get('text', 'Aucun texte trouvé dans la réponse')

                        # Filtrer les répétitions ou réduire la longueur du texte
                        text = text[:300]  # Limiter à 300 caractères (ajustez selon vos besoins)
                        
                        # Log pour le texte extrait
                        logger.info(f"Texte extrait: {text}")
                        
                        return text.strip()  # Retirer les espaces inutiles
                    return "Réponse vide du modèle."
                return "Aucune sortie disponible de l'API."
            return "Format inattendu de la réponse API."
        except aiohttp.ClientError as e:
            logger.error(f"Erreur réseau lors de la récupération de la réponse: {str(e)}")
            return f"Erreur réseau: {str(e)}"
        except ValueError as e:
            logger.error(f"Erreur de traitement JSON: {str(e)}")
            return f"Erreur JSON: {str(e)}"

    async def async_post(self, url: str, data: dict, headers: dict) -> dict:
        """
        Effectue une requête POST asynchrone.
        :param url: L'URL de la requête POST
        :param data: Les données à envoyer dans la requête POST
        :param headers: Les en-têtes de la requête POST
        :return: La réponse JSON de la requête POST
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                if response.status == 200 and response.headers.get('Content-Type') == 'application/json':
                    return await response.json()
                else:
                    logger.error(f"Unexpected content type: {response.headers.get('Content-Type')}")
                    return {"error": f"Unexpected content type: {response.headers.get('Content-Type')}"}

    def get_token_from_query_string(self, query_string):
        """
        Extrait le token JWT de la chaîne de requête.
        """
        if 'token=' in query_string:
            return query_string.split('token=')[1]
        return None
