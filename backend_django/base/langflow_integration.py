import requests

async def call_your_langflow_agent(message):
    # URL de l'API de Langflow
    langflow_url = 'https://api.langflow.com/process_message'  # Remplacez par l'URL de votre API Langflow
    
    # En-têtes de la requête (ajustez selon les besoins de votre API)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_API_KEY'  # Remplacez par votre clé API si nécessaire
    }
    
    # Corps de la requête
    data = {
        'message': message
    }
    
    # Envoyer la requête POST à l'API Langflow
    response = requests.post(langflow_url, headers=headers, json=data)
    
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Extraire la réponse JSON
        response_data = response.json()
        # Retourner la réponse traitée
        return response_data.get('response', 'No response from Langflow')
    else:
        # En cas d'erreur, retourner un message d'erreur
        return f'Error: {response.status_code} - {response.text}'
