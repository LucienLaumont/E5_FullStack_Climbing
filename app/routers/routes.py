from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List
import schemas
from models import get_db
import services.routes as route_service
from starlette.requests import Request
from routers.utils import verify_autorization_header

router = APIRouter()

security = HTTPBearer()

@router.get("/routes/", response_model=List[schemas.Route], tags=["Routes"])
async def get_all_routes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Endpoint pour obtenir toutes les routes avec pagination."""
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be greater than 0")
    routes = route_service.get_all_routes(db, skip=skip, limit=limit)
    if not routes:
        raise HTTPException(status_code=404, detail="No routes found")
    return routes

@router.get("/routes/{name_id}", response_model=schemas.Route, tags=["Routes"])
async def get_route_by_id(name_id: int, db: Session = Depends(get_db)):
    """Endpoint pour obtenir une route par ID."""
    if name_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid route ID")
    route = route_service.get_route_by_id(db, name_id)
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

@router.post("/routes/", dependencies=[Depends(security)], response_model=schemas.Route, tags=["Routes"])
async def create_route(request: Request, route: schemas.RouteCreate, db: Session = Depends(get_db)):
    """Endpoint pour ajouter une nouvelle route."""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    token = verify_autorization_header(auth_header)
    if not token:
        raise HTTPException(status_code=403, detail="Invalid authorization token")
    new_route = route_service.create_route(db, route)
    if not new_route:
        raise HTTPException(status_code=500, detail="Failed to create the route")
    return new_route

@router.put("/routes/{name_id}", dependencies=[Depends(security)], response_model=schemas.Route, tags=["Routes"])
async def update_route(request: Request, name_id: int, updated_data: schemas.RouteCreate, db: Session = Depends(get_db)):
    """Endpoint pour mettre à jour une route existante."""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    token = verify_autorization_header(auth_header)
    if not token:
        raise HTTPException(status_code=403, detail="Invalid authorization token")
    if name_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid route ID")
    route = route_service.update_route(db, name_id, updated_data)
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

@router.delete("/routes/{name_id}", dependencies=[Depends(security)], response_model=dict, tags=["Routes"])
async def delete_route(request: Request, name_id: int, db: Session = Depends(get_db)):
    """Endpoint pour supprimer une route."""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    token = verify_autorization_header(auth_header)
    if not token:
        raise HTTPException(status_code=403, detail="Invalid authorization token")
    if name_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid route ID")
    if route_service.delete_route(db, name_id):
        return {"message": "Route deleted successfully"}
    raise HTTPException(status_code=404, detail="Route not found")

@router.get("/routes/country/{country}", response_model=List[schemas.Route], tags=["Routes"])
async def get_routes_by_country(country: str, db: Session = Depends(get_db)):
    """Endpoint pour obtenir les routes d'un pays spécifique."""
    if not country:
        raise HTTPException(status_code=400, detail="Country name is required")
    routes = route_service.get_routes_by_country(db, country)
    if not routes:
        raise HTTPException(status_code=404, detail=f"No routes found for country '{country}'")
    return routes

@router.get("/routes/top/", response_model=List[schemas.Route], tags=["Routes"])
async def get_top_routes_by_grade(limit: int = 10, db: Session = Depends(get_db)):
    """Endpoint pour obtenir les routes avec la meilleure note moyenne."""
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be greater than 0")
    routes = route_service.get_top_routes_by_grade(db, limit=limit)
    if not routes:
        raise HTTPException(status_code=404, detail="No top routes found")
    return routes

@router.get("/routes/best_by_country/{country}", response_model=List[schemas.Route], tags=["Routes"])
async def get_best_route_by_country(country: str, limit: int = 1, db: Session = Depends(get_db)):
    """Endpoint pour obtenir les meilleures routes d'un pays spécifique."""
    if not country:
        raise HTTPException(status_code=400, detail="Country name is required")
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be greater than 0")
    routes = route_service.get_best_route_by_country(db, country, limit=limit)
    if not routes:
        raise HTTPException(status_code=404, detail=f"No routes found for country '{country}'")
    return routes
