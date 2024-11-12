from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class ClimberBase(BaseModel):
    climber_id: int
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

class ClimberCreate(ClimberBase):
    pass

class Climber(ClimberBase):
    
    class Config:
        orm_mode = True
