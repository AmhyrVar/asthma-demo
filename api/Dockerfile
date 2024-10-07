# Utilise une image Python officielle
FROM python:3.9

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application
COPY . .

# Exposer le port pour l'API
EXPOSE 8000

# Démarrer l'API FastAPI avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
