from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas
from models import get_db
import services.climbers as climber_service
from starlette.requests import Request
from routers.utils import verify_autorization_header

router = APIRouter()

security = HTTPBearer()

@router.get("/climbers/", response_model=List[schemas.Climber], tags=["Climbers"])
async def get_all_climbers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Endpoint pour obtenir tous les grimpeurs avec pagination."""
    return climber_service.get_all_climbers(db, skip=skip, limit=limit)

@router.get("/climbers/{climber_id}", response_model=schemas.Climber, tags=["Climbers"])
async def get_climber_by_id(climber_id: int, db: Session = Depends(get_db)):
    """Endpoint pour obtenir un grimpeur par ID."""
    climber = climber_service.get_climber_by_id(db, climber_id)
    if not climber:
        raise HTTPException(status_code=404, detail="Climber not found")
    return climber

@router.post("/climbers/",dependencies=[Depends(security)], response_model=schemas.Climber, tags=["Climbers"])
async def create_climber(request: Request, climber: schemas.Climber, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    token = verify_autorization_header(auth_header)
    user_id = token.get("user_id")
    """Endpoint pour ajouter un nouveau grimpeur."""
    return climber_service.create_climber(db, climber)

@router.put("/climbers/{climber_id}",dependencies=[Depends(security)], response_model=schemas.Climber, tags=["Climbers"])
async def update_climber(request: Request, climber_id: int, updated_data: schemas.Climber, db: Session = Depends(get_db)):
    """Endpoint pour mettre à jour un grimpeur existant."""
    auth_header = request.headers.get("Authorization")
    token = verify_autorization_header(auth_header)
    user_id = token.get("user_id")
    climber = climber_service.update_climber(db, climber_id, updated_data)
    if not climber:
        raise HTTPException(status_code=404, detail="Climber not found")
    return climber

@router.delete("/climbers/{climber_id}",dependencies=[Depends(security)], response_model=dict, tags=["Climbers"])
async def delete_climber(request: Request, climber_id: int, db: Session = Depends(get_db)):
    """Endpoint pour supprimer un grimpeur."""
    auth_header = request.headers.get("Authorization")
    token = verify_autorization_header(auth_header)
    user_id = token.get("user_id")
    if climber_service.delete_climber(db, climber_id):
        return {"message": "Climber deleted successfully"}
    raise HTTPException(status_code=404, detail="Climber not found")

#############################################################################################
#############################################################################################
#############################################################################################

@router.get("/climbers/countries/", response_model=List[str], tags=["Climbers"])
async def get_countries(db: Session = Depends(get_db)):
    """Endpoint pour obtenir la liste des pays avec des grimpeurs."""
    return climber_service.get_country(db)

@router.get("/climbers/filter_by_sex/", response_model=List[schemas.Climber], tags=["Climbers"])
async def get_climbers_by_sex(sex: int, db: Session = Depends(get_db)):
    """Endpoint pour obtenir tous les grimpeurs filtrés par sexe."""
    return climber_service.get_climbers_by_sex(db, sex)

@router.get("/climbers/filter_experience/", response_model=List[schemas.Climber], tags=["Climbers"])
async def get_climbers_by_years_climbing(min_years: int = 0, max_years: int = 5, db: Session = Depends(get_db)):
    """Endpoint pour obtenir tous les grimpeurs filtrés par leur niveau d'expérience."""
    return climber_service.get_climbers_by_years_climbing(db, min_years,max_years)

@router.get("/climbers/by_country/", response_model=List[schemas.Climber], tags=["Climbers"])
async def get_climbers_by_country(country: str = "FRA", db: Session = Depends(get_db)):
    """Endpoint pour obtenir les grimpeurs venant d'un pays particulier (par défaut 'FRA')."""
    return climber_service.get_climbers_by_country(db, country)

@router.get("/climbers/filter_height/", response_model=List[schemas.Climber], tags=["Climbers"])
async def get_climbers_by_height(min_height: float = 190, max_height: float = 200, db: Session = Depends(get_db)):
    """Endpoint pour obtenir les grimpeurs filtrés par leur taille."""
    return climber_service.get_climbers_by_height(db, min_height, max_height)

@router.get("/climbers/filter_weight/", response_model=List[schemas.Climber], tags=["Climbers"])
async def get_climbers_by_weight(min_weight: float = 90, max_weight: float = 100, db: Session = Depends(get_db)):
    """Endpoint pour obtenir les grimpeurs filtrés par leur poids."""
    return climber_service.get_climbers_by_weight(db, min_weight, max_weight)

@router.get("/climbers/filter_age/", response_model=List[schemas.Climber], tags=["Climbers"])
def get_climbers_by_age(min_age: int = 55, max_age: int = 58, db: Session = Depends(get_db)):
    """Endpoint pour obtenir les grimpeurs filtrés par leur âge."""
    return climber_service.get_climbers_by_age(db, min_age, max_age)

#############################################################################################
#############################################################################################
#############################################################################################


