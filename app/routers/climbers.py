from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas
from models import get_db
import services.climbers as climber_service

router = APIRouter()

@router.get("/climbers/", response_model=List[schemas.Climber], tags=["Climbers"])
def get_all_climbers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Endpoint pour obtenir tous les grimpeurs avec pagination."""
    return climber_service.get_all_climbers(db, skip=skip, limit=limit)

@router.get("/climbers/{climber_id}", response_model=schemas.Climber, tags=["Climbers"])
def get_climber_by_id(climber_id: int, db: Session = Depends(get_db)):
    """Endpoint pour obtenir un grimpeur par ID."""
    climber = climber_service.get_climber_by_id(db, climber_id)
    if not climber:
        raise HTTPException(status_code=404, detail="Climber not found")
    return climber

@router.post("/climbers/", response_model=schemas.Climber, tags=["Climbers"])
def create_climber(climber: schemas.ClimberCreate, db: Session = Depends(get_db)):
    """Endpoint pour ajouter un nouveau grimpeur."""
    return climber_service.create_climber(db, climber)

@router.put("/climbers/{climber_id}", response_model=schemas.Climber, tags=["Climbers"])
def update_climber(climber_id: int, updated_data: schemas.ClimberCreate, db: Session = Depends(get_db)):
    """Endpoint pour mettre à jour un grimpeur existant."""
    climber = climber_service.update_climber(db, climber_id, updated_data)
    if not climber:
        raise HTTPException(status_code=404, detail="Climber not found")
    return climber

@router.delete("/climbers/{climber_id}", response_model=dict, tags=["Climbers"])
def delete_climber(climber_id: int, db: Session = Depends(get_db)):
    """Endpoint pour supprimer un grimpeur."""
    if climber_service.delete_climber(db, climber_id):
        return {"message": "Climber deleted successfully"}
    raise HTTPException(status_code=404, detail="Climber not found")

@router.get("/climbers/countries/", response_model=List[str], tags=["Climbers"])
def get_countries(db: Session = Depends(get_db)):
    """Endpoint pour obtenir la liste des pays avec des grimpeurs."""
    return climber_service.get_country(db)

@router.get("/climbers/countries/{country_name}", response_model=List[schemas.Climber], tags=["Climbers"])
def get_climbers_by_country(country_name: str, db: Session = Depends(get_db)):
    """Endpoint pour obtenir les grimpeurs originaires d'un pays spécifique."""
    return climber_service.get_climbers_by_country(country_name, db)

@router.get("/climbers/count_by_country/", response_model=List[dict], tags=["Climbers"])
def get_climbers_count_by_country(db: Session = Depends(get_db)):
    """Endpoint pour obtenir le nombre de grimpeurs par pays."""
    return climber_service.get_climbers_count_by_country(db)

@router.get("/climbers/youngest/", response_model=List[schemas.Climber], tags=["Climbers"])
def get_youngest_climbers(limit: int = 10, db: Session = Depends(get_db)):
    """Endpoint pour obtenir les grimpeurs les plus jeunes."""
    return climber_service.get_youngest_climbers(db, limit=limit)

@router.get("/climbers/oldest/", response_model=List[schemas.Climber], tags=["Climbers"])
def get_oldest_climbers(limit: int = 10, db: Session = Depends(get_db)):
    """Endpoint pour obtenir les grimpeurs les plus âgés."""
    return climber_service.get_oldest_climbers(db, limit=limit)

@router.get("/climbers/tallest/", response_model=List[schemas.Climber], tags=["Climbers"])
def get_tallest_climbers(limit: int = 10, db: Session = Depends(get_db)):
    """Endpoint pour obtenir les grimpeurs les plus grands."""
    return climber_service.get_tallest_climbers(db, limit=limit)

@router.get("/climbers/shortest/", response_model=List[schemas.Climber], tags=["Climbers"])
def get_shortest_climbers(limit: int = 10, db: Session = Depends(get_db)):
    """Endpoint pour obtenir les grimpeurs les plus petits."""
    return climber_service.get_shortest_climbers(db, limit=limit)
