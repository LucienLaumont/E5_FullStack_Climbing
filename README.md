
# 🧗‍♂️ Climbing Dashboard Application

## 📖 Description

Ce projet est une application FullStack 🖥️ construite autour du thème de l'escalade. Voici les principaux composants :
- **API** : Développée avec **FastAPI** 🚀, pour gérer les grimpeurs à partir de données provenant de Kaggle.
- **Base de données** : Utilisation de **PostgreSQL** 🐘 pour stocker et gérer les données.
- **Frontend** : Une interface utilisateur dynamique créée avec **React** ⚛️.
- **Docker** : L'ensemble du projet est dockerisé 🐳 pour simplifier le déploiement.

## 🏗️ Structure du projet

```
CLIMBING
├── app/                  # Backend (API)
├── frontend/             # Frontend (React)
├── docker-compose.yml    # Configuration Docker
├── .env                  # Variables d'environnement
└── README.md             # Documentation
```

## 🔧 Fonctionnalités principales

### Backend (API)
- Création, lecture et gestion des grimpeurs avec **FastAPI** 🚀.
- Authentification par token 🔑.
- Gestion des erreurs claires, comme le fameux `404 Not Found`.
- Validation des données grâce à **Pydantic**.

### Frontend (React)
- Page de présentation 📖
- Dashboard sur les grimpeurs 🏔️

### Base de données (PostgreSQL)
- Stockage des grimpeurs et des autres entités liées à l'escalade.

## 🛠️ Configuration et Lancement

### Prérequis
- **Docker** et **Docker Compose** installés sur votre machine.

### Étapes
1. **Cloner le projet** :
   ```bash
   git clone <URL_DU_DEPOT>
   cd CLIMBING
   ```

2. **Lancer l'application** :
   ```bash
   docker-compose up --build
   ```

3. **Accéder à l'application** :
   - 🌐 API : [http://localhost:5000](http://localhost:5000)
   - 🌐 Frontend : [http://localhost:3000](http://localhost:3000)

## 🗂️ Dataset

Les données utilisées proviennent de Kaggle : [Climb Dataset](https://www.kaggle.com/datasets/jordizar/climb-dataset).

---

### 🚀 Amusez-vous bien avec ce projet FullStack d'escalade ! 🧗‍♀️
