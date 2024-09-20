# Importation des classes nécessaires depuis le framework Django REST
#Créer par Rivah
from rest_framework import viewsets
from .models import Message
from .serializers import MessageSerializer
from rest_framework.permissions import AllowAny

# Définition de la vue pour le modèle Message
class MessageViewSet(viewsets.ModelViewSet):
    # Définir la requête de base pour cette vue, qui récupère tous les objets Message
    queryset = Message.objects.all()

    # Définir le sérialiseur à utiliser pour transformer les objets Message en JSON
    serializer_class = MessageSerializer

    # Définir les permissions pour cette vue
    # AllowAny permet à tout le monde d'accéder à cette vue, sans authentification
    # Il est possible de modifier cette classe de permissions selon les besoins de votre application
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]
    # permission_classes = [IsAdminUser]