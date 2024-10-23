from typing import Optional
from fastapi import FastAPI, Request, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
import json
import base64
from starlette_exporter import PrometheusMiddleware, handle_metrics
from models import engine
from database import BaseSQL
import routers

# Création de l'application FastAPI
app = FastAPI(
    title="🌍 Climbing Profiles & Routes API 🧗‍♂️🧗‍♀️",
    description="""Explore the world of climbers and climbing routes like never before! Whether you're a seasoned pro or just starting out, this API connects you with the global climbing community. 🌍

🎯 What Can You Do?
Discover Climbers from Around the World 🌍

Want to know who's climbing the toughest routes in France or scaling peaks in Japan? 🌄 Check out detailed profiles of climbers from all over the world. Learn about their stats, experience, and more! 📊

Explore Epic Climbing Routes 🧗‍♂️

Looking for the most challenging climbs? Find routes by country, difficulty, and location. 🌍💪 Whether it’s the towering cliffs of Yosemite 🏞️ or the hidden gems of Montserrat, we’ve got you covered!

Get Cool Stats 📊

From finding the youngest climbers 🍼 to the tallest ones 👀, or seeing which country is home to the most climbers—our API brings climbing data to life! 📈

🚀 Why Use This API?
Adventure Seekers 🧗: Discover new challenges and top-rated routes.
Climbing Enthusiasts 💪: Explore climber profiles and connect with the community.
Developers 👨‍💻: Easily integrate climbing data into your own apps or services.""",
    version="0.0.1",
)

# CORS
origins = [
    "http://localhost:4200",
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(routers.ClimberRouter)
app.include_router(routers.RouteRouter)
app.include_router(routers.HealthRouter)

# Middleware Prometheus
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

# Initialisation de la base de données au démarrage
@app.on_event("startup")
async def startup_event():
    BaseSQL.metadata.create_all(bind=engine)
