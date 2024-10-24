from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List
from starlette.requests import Request
from routers.utils import verify_autorization_header
import schemas
from models import get_db
import services.users as user_service

router = APIRouter()

security = HTTPBearer()

@router.get("/users/", dependencies=[Depends(security)], response_model=List[schemas.User], tags=["Users"])
async def get_all_users(request: Request,skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Endpoint pour obtenir tous les users avec pagination."""
    auth_header = request.headers.get("Authorization")
    token = verify_autorization_header(auth_header)
    user_id = token.get("user_id")

    return user_service.get_all_users(db,user_id = user_id, skip=skip, limit=limit)

@router.post("/users/", response_model=schemas.User, tags=["Users"])
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    """Endpoint pour ajouter un nouveau users."""
    return user_service.create_user(db, user)