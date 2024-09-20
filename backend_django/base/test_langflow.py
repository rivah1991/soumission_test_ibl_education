import asyncio
import httpx

async def get_langflow_response(message):
    langflow_url = 'http://127.0.0.1:7860/api/v1/run/224aaba0-b9f7-4e61-a690-dc4ae674d868?stream=false'
    headers = {'Content-Type': 'application/json'}
    data = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
        "tweaks": {
            "ChatInput-Fwj5F": {},
            "Prompt-YCXBm": {},
            "ChatOutput-sqFjS": {},
            "HuggingFaceModel-TBSYl": {},
            "TextInput-LEroE": {},
            "TextOutput-tRGrx": {}
        }
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(langflow_url, headers=headers, json=data)
            response.raise_for_status()  # Assure que la requête a réussi
            response_data = response.json()
            print(f"Réponse complète : {response_data}")  # Affiche la réponse complète

            # Extraire le texte du message
            outputs = response_data.get('outputs', [])
            if outputs:
                # Imprimer les données pour déboguer
                print(f"Outputs trouvés : {outputs}")
                result = outputs[0].get('outputs', [{}])[0].get('results', {}).get('message', {}).get('text', 'Pas de champ texte dans le message')
                print(f"Résultat extrait : {result}")
                return result
            return 'Pas de champ outputs dans la réponse'
        except httpx.HTTPStatusError as e:
            return f'Erreur HTTP : {e.response.status_code} - {e.response.text}'
        except httpx.RequestError as e:
            return f'Erreur de requête : {str(e)}'

# Test
async def main():
    message = "message"  # Vous pouvez ajuster le message si nécessaire
    result = await get_langflow_response(message)
    print(f"Résultat du test : {result}")

if __name__ == "__main__":
    asyncio.run(main())
