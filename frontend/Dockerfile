# Utiliser une image de base Node.js
FROM node:14

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier package.json et installer les dépendances
COPY package.json /app
RUN npm install

# Copier le reste des fichiers du frontend dans le conteneur
COPY . /app

# Exécuter le serveur de développement React
CMD ["npm", "start"]
