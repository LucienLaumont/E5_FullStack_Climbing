from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas
from models import get_db
import services.routes as route_service

router = APIRouter()

@router.get("/routes/", response_model=List[schemas.Route], tags=["Routes"])
def get_all_routes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Endpoint pour obtenir toutes les routes avec pagination."""
    return route_service.get_all_routes(db, skip=skip, limit=limit)

@router.get("/routes/{name_id}", response_model=schemas.Route, tags=["Routes"])
def get_route_by_id(name_id: int, db: Session = Depends(get_db)):
    """Endpoint pour obtenir une route par ID."""
    route = route_service.get_route_by_id(db, name_id)
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

@router.post("/routes/", response_model=schemas.Route, tags=["Routes"])
def create_route(route: schemas.RouteCreate, db: Session = Depends(get_db)):
    """Endpoint pour ajouter une nouvelle route."""
    return route_service.create_route(db, route)

@router.put("/routes/{name_id}", response_model=schemas.Route, tags=["Routes"])
def update_route(name_id: int, updated_data: schemas.RouteCreate, db: Session = Depends(get_db)):
    """Endpoint pour mettre à jour une route existante."""
    route = route_service.update_route(db, name_id, updated_data)
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

@router.delete("/routes/{name_id}", response_model=dict, tags=["Routes"])
def delete_route(name_id: int, db: Session = Depends(get_db)):
    """Endpoint pour supprimer une route."""
    if route_service.delete_route(db, name_id):
        return {"message": "Route deleted successfully"}
    raise HTTPException(status_code=404, detail="Route not found")

@router.get("/routes/country/{country}", response_model=List[schemas.Route], tags=["Routes"])
def get_routes_by_country(country: str, db: Session = Depends(get_db)):
    """Endpoint pour obtenir les routes d'un pays spécifique."""
    return route_service.get_routes_by_country(db, country)

@router.get("/routes/top/", response_model=List[schemas.Route], tags=["Routes"])
def get_top_routes_by_grade(limit: int = 10, db: Session = Depends(get_db)):
    """Endpoint pour obtenir les routes avec la meilleure note moyenne."""
    return route_service.get_top_routes_by_grade(db, limit=limit)

@router.get("/routes/best_by_country/{country}", response_model=List[schemas.Route], tags=["Routes"])
def get_best_route_by_country(country: str, limit: int = 1, db: Session = Depends(get_db)):
    """Endpoint pour obtenir les meilleures routes d'un pays spécifique."""
    return route_service.get_best_route_by_country(db, country, limit=limit)
