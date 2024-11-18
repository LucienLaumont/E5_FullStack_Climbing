from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List
import schemas
from models import get_db
import services.climbers as climber_service
from starlette.requests import Request
from routers.utils import verify_autorization_header

router = APIRouter()

security = HTTPBearer()

# Gestion des grimpeurs
@router.get("/climbers/", response_model=List[schemas.Climber], tags=["Climbers"])
async def get_all_climbers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Endpoint pour obtenir tous les grimpeurs avec pagination."""
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be greater than 0")
    climbers = climber_service.get_all_climbers(db, skip=skip, limit=limit)
    if not climbers:
        raise HTTPException(status_code=404, detail="No climbers found")
    return climbers

@router.get("/climbers/{climber_id}", response_model=schemas.Climber, tags=["Climbers"])
async def get_climber_by_id(climber_id: int, db: Session = Depends(get_db)):
    """Endpoint pour obtenir un grimpeur par ID."""
    if climber_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid climber ID")
    climber = climber_service.get_climber_by_id(db, climber_id)
    if not climber:
        raise HTTPException(status_code=404, detail="Climber not found")
    return climber

@router.post("/climbers/", dependencies=[Depends(security)], response_model=schemas.Climber, tags=["Climbers"])
async def create_climber(request: Request, climber: schemas.Climber, db: Session = Depends(get_db)):
    """Endpoint pour ajouter un nouveau grimpeur."""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    token = verify_autorization_header(auth_header)
    if not token:
        raise HTTPException(status_code=403, detail="Invalid authorization token")
    new_climber = climber_service.create_climber(db, climber)
    if not new_climber:
        raise HTTPException(status_code=500, detail="Failed to create climber")
    return new_climber

@router.put("/climbers/{climber_id}", dependencies=[Depends(security)], response_model=schemas.Climber, tags=["Climbers"])
async def update_climber(request: Request, climber_id: int, updated_data: schemas.Climber, db: Session = Depends(get_db)):
    """Endpoint pour mettre à jour un grimpeur existant."""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    token = verify_autorization_header(auth_header)
    if not token:
        raise HTTPException(status_code=403, detail="Invalid authorization token")
    if climber_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid climber ID")
    climber = climber_service.update_climber(db, climber_id, updated_data)
    if not climber:
        raise HTTPException(status_code=404, detail="Climber not found")
    return climber

@router.delete("/climbers/{climber_id}", dependencies=[Depends(security)], response_model=dict, tags=["Climbers"])
async def delete_climber(request: Request, climber_id: int, db: Session = Depends(get_db)):
    """Endpoint pour supprimer un grimpeur."""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    token = verify_autorization_header(auth_header)
    if not token:
        raise HTTPException(status_code=403, detail="Invalid authorization token")
    if climber_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid climber ID")
    if climber_service.delete_climber(db, climber_id):
        return {"message": "Climber deleted successfully"}
    raise HTTPException(status_code=404, detail="Climber not found")

# Gestion des filtres et données
@router.get("/climbers/countries/", response_model=List[str], tags=["Climbers"])
async def get_countries(db: Session = Depends(get_db)):
    """Endpoint pour obtenir la liste des pays avec des grimpeurs."""
    countries = climber_service.get_country(db)
    if not countries:
        raise HTTPException(status_code=404, detail="No countries found")
    return countries

@router.get("/climbers/filter_by_sex/", response_model=List[schemas.Climber], tags=["Climbers"])
async def get_climbers_by_sex(sex: int, db: Session = Depends(get_db)):
    """Endpoint pour obtenir tous les grimpeurs filtrés par sexe."""
    if sex not in [0, 1]:
        raise HTTPException(status_code=400, detail="Invalid sex value, must be 0 or 1")
    climbers = climber_service.get_climbers_by_sex(db, sex)
    if not climbers:
        raise HTTPException(status_code=404, detail="No climbers found for the specified sex")
    return climbers

@router.get("/climbers/filter_experience/", response_model=List[schemas.Climber], tags=["Climbers"])
async def get_climbers_by_years_climbing(min_years: int = 0, max_years: int = 5, db: Session = Depends(get_db)):
    """Endpoint pour obtenir tous les grimpeurs filtrés par leur niveau d'expérience."""
    if min_years < 0 or max_years < min_years:
        raise HTTPException(status_code=400, detail="Invalid experience range")
    climbers = climber_service.get_climbers_by_years_climbing(db, min_years, max_years)
    if not climbers:
        raise HTTPException(status_code=404, detail="No climbers found for the specified experience range")
    return climbers

@router.get("/climbers/by_country/", response_model=List[schemas.Climber], tags=["Climbers"])
async def get_climbers_by_country(country: str = "FRA", db: Session = Depends(get_db)):
    """Endpoint pour obtenir les grimpeurs venant d'un pays particulier (par défaut 'FRA')."""
    if not country:
        raise HTTPException(status_code=400, detail="Country is required")
    climbers = climber_service.get_climbers_by_country(db, country)
    if not climbers:
        raise HTTPException(status_code=404, detail=f"No climbers found for country '{country}'")
    return climbers

@router.get("/climbers/filter_height/", response_model=List[schemas.Climber], tags=["Climbers"])
async def get_climbers_by_height(min_height: float = 190, max_height: float = 200, db: Session = Depends(get_db)):
    """Endpoint pour obtenir les grimpeurs filtrés par leur taille."""
    if min_height < 0 or max_height < min_height:
        raise HTTPException(status_code=400, detail="Invalid height range")
    climbers = climber_service.get_climbers_by_height(db, min_height, max_height)
    if not climbers:
        raise HTTPException(status_code=404, detail="No climbers found for the specified height range")
    return climbers

@router.get("/climbers/filter_weight/", response_model=List[schemas.Climber], tags=["Climbers"])
async def get_climbers_by_weight(min_weight: float = 90, max_weight: float = 100, db: Session = Depends(get_db)):
    """Endpoint pour obtenir les grimpeurs filtrés par leur poids."""
    if min_weight < 0 or max_weight < min_weight:
        raise HTTPException(status_code=400, detail="Invalid weight range")
    climbers = climber_service.get_climbers_by_weight(db, min_weight, max_weight)
    if not climbers:
        raise HTTPException(status_code=404, detail="No climbers found for the specified weight range")
    return climbers

@router.get("/climbers/filter_age/", response_model=List[schemas.Climber], tags=["Climbers"])
async def get_climbers_by_age(min_age: int = 55, max_age: int = 58, db: Session = Depends(get_db)):
    """Endpoint pour obtenir les grimpeurs filtrés par leur âge."""
    if min_age < 0 or max_age < min_age:
        raise HTTPException(status_code=400, detail="Invalid age range")
    climbers = climber_service.get_climbers_by_age(db, min_age, max_age)
    if not climbers:
        raise HTTPException(status_code=404, detail="No climbers found for the specified age range")
    return climbers

# Dashboard Endpoints
@router.get("/BarChart_Climbers_Genders/", response_model=dict, tags=["Dashboard"])
async def get_climbers_by_genders(db: Session = Depends(get_db), max_age: int = Query(None)):
    """Retourne les grimpeurs par genres avec une limite d'âge maximale optionnelle."""
    data = climber_service.get_climbers_by_genders(db, max_age)
    if not data:
        raise HTTPException(status_code=404, detail="No data found for genders")
    return data

@router.get("/PieChart_Climbers_Experience/", response_model=dict, tags=["Dashboard"])
async def get_climbers_by_experience(db: Session = Depends(get_db), max_age: int = Query(None)):
    """Retourne la répartition des grimpeurs par tranches d'années d'expérience."""
    data = climber_service.get_climbers_by_experience(db, max_age)
    if not data:
        raise HTTPException(status_code=404, detail="No data found for experience levels")
    return data

@router.get("/PieChart_Climbers_Countries/", response_model=dict, tags=["Dashboard"])
async def get_climbers_by_countries(db: Session = Depends(get_db), max_age: int = Query(None), limit: int = 6):
    """Retourne la répartition des grimpeurs par pays."""
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be greater than 0")
    data = climber_service.get_climbers_by_countries(db, max_age, limit)
    if not data:
        raise HTTPException(status_code=404, detail="No data found for climbers by countries")
    return data

@router.get("/scatterGradesByAge", tags=["Dashboard"])
async def get_average_grades_by_age(db: Session = Depends(get_db), max_age: int = Query(None)):
    """Retourne les grades_max par âge en fonction de l'âge maximum spécifié."""
    data = climber_service.get_grades_by_age(db, max_age)
    if not data:
        raise HTTPException(status_code=404, detail="No data found for grades by age")
    return data

