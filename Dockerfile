# Utiliser une image de base pour FastAPI
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# Ajouter les fichiers nécessaires
ADD requirements.txt .

# Installer les dépendances
RUN pip install -r requirements.txt

# Copier le code de l'application dans le conteneur
COPY ./app /app/app

# Exécuter le script d'initialisation de la base de données
CMD ["sh", "-c", "python /app/init_db.py && uvicorn main:app --host 0.0.0.0 --port 5000 --reload"]
