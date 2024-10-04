# Utiliser une image de base pour FastAPI (Python 3.10)
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le contenu de l'application dans le conteneur
COPY . /app

# Exécuter le script d'initialisation de la base de données et lancer l'API
CMD ["sh", "-c", "python /app/init_db.py && uvicorn main:app --host 0.0.0.0 --port 5000 --reload"]
