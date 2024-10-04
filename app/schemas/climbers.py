from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schéma pour les données de grimpeurs (Climbers)
class ClimberBase(BaseModel):
    country: str
    sex: int
    height: float
    weight: float
    age: float
    years_cl: int
    date_first: datetime
    date_last: datetime
    grades_count: int
    grades_first: int
    grades_last: int
    grades_max: int
    grades_mean: float
    year_first: int
    year_last: int

# Schéma pour la création de grimpeurs
class ClimberCreate(ClimberBase):
    pass

# Schéma pour la réponse avec l'ID de l'utilisateur
class Climber(ClimberBase):
    user_id: int

    class Config:
        orm_mode = True
