from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy.dialects.postgresql import UUID
import schemas
from models import get_db
import services.users as user_service

router = APIRouter()

security = HTTPBearer()

@router.get("/users/", response_model=List[schemas.User], tags=["Users"])
async def get_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Endpoint pour obtenir tous les grimpeurs avec pagination."""
    return user_service.get_all_users(db, skip=skip, limit=limit)