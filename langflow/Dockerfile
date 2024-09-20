# Utiliser l'image Python officielle comme base
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier de dépendances
COPY requirements.txt ./ 

# Mettre à jour pip, setuptools et wheel
RUN pip install --upgrade pip setuptools wheel

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source de l'application
COPY . .

# Exposer le port utilisé par Langflow
EXPOSE 7860

# Définir la commande d'exécution pour Langflow
CMD ["langflow", "run", "--host", "0.0.0.0", "--port", "7860"]