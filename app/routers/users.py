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
async def get_all_users(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Endpoint pour obtenir tous les utilisateurs avec pagination."""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    token = verify_autorization_header(auth_header)
    if not token:
        raise HTTPException(status_code=403, detail="Invalid authorization token")

    user_id = token.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID not found in token")

    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be greater than 0")
    
    users = user_service.get_all_users(db, user_id=user_id, skip=skip, limit=limit)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    
    return users

@router.post("/users/", response_model=schemas.User, tags=["Users"])
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    """Endpoint pour ajouter un nouvel utilisateur."""
    if not user:
        raise HTTPException(status_code=400, detail="User data is required")
    
    new_user = user_service.create_user(db, user)
    if not new_user:
        raise HTTPException(status_code=500, detail="Failed to create user")
    
    return new_user
