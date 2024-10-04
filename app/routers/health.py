from fastapi import FastAPI, Header, Request, APIRouter
from typing import Optional
import base64
import json

router = APIRouter()

# Page d'accueil personnalisée
@router.get("/")
async def read_root():
    return {
        "message": "Welcome to the Climbing Profiles & Routes API 🧗‍♂️🧗‍♀️",
        "description": "Explore climber profiles and epic climbing routes from around the world!",
        "endpoints": {
            "/api": "Basic Hello API",
            "/health": "API Health Check",
            "/api/headers": "Decode custom headers"
        }
    }


@router.get("/api")
def read_hello():
    return {"Hello": "Api"}


@router.get("/health")
def read_root():
    return {"message": "Api is running fine!"}


@router.get("/api/headers")
def read_hello(request: Request, x_userinfo: Optional[str] = Header(None, convert_underscores=True)):
    print(request["headers"])
    return {"Headers": json.loads(base64.b64decode(x_userinfo))}