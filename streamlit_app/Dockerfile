# Utilise une image officielle Python
FROM python:3.9

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code de l'application dans le conteneur
COPY . .

# Exposer le port utilisé par Streamlit
EXPOSE 8501

# Démarrer Streamlit
CMD ["streamlit", "run", "questionnaire-act.py", "--server.port=8501", "--server.address=0.0.0.0"]
