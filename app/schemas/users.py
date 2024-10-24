from pydantic import BaseModel
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID

# Schéma de base pour les users
class UserBase(BaseModel):
    username : str
    password : str

# Schéma pour la création d'une nouveau user
class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
