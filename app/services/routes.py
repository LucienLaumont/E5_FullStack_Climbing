from sqlalchemy.orm import Session
from typing import List
import models, schemas

def get_all_routes(db: Session, skip: int = 0, limit: int = 10) -> List[models.Route]:
    """Obtenir toutes les routes avec pagination."""
    records = db.query(models.Route).offset(skip).limit(limit).all()
    return records

def get_route_by_id(db: Session, name_id: int) -> models.Route:
    """Obtenir une route par son identifiant (name_id)."""
    record = db.query(models.Route).filter(models.Route.name_id == name_id).first()
    return record

def create_route(db: Session, route: schemas.RouteCreate) -> models.Route:
    """Ajouter une nouvelle route dans la base de données."""
    db_route = models.Route(**route.dict())
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route

def update_route(db: Session, name_id: int, updated_data: schemas.RouteCreate) -> models.Route:
    """Mettre à jour une route existante."""
    db_route = db.query(models.Route).filter(models.Route.name_id == name_id).first()

    if db_route:
        updated_data_dict = updated_data.dict(exclude_unset=True)
        for key, value in updated_data_dict.items():
            setattr(db_route, key, value)
        
        db.commit()
        db.refresh(db_route)
        return db_route
    return None

def delete_route(db: Session, name_id: int) -> bool:
    """Supprimer une route de la base de données."""
    db_route = db.query(models.Route).filter(models.Route.name_id == name_id).first()

    if db_route:
        db.delete(db_route)
        db.commit()
        return True
    return False

def get_routes_by_country(db: Session, country: str) -> List[models.Route]:
    """Obtenir des routes par pays."""
    records = db.query(models.Route).filter(models.Route.country == country).all()
    return records

def get_top_routes_by_grade(db: Session, limit: int = 10) -> List[models.Route]:
    """Obtenir les routes avec la meilleure note moyenne."""
    records = db.query(models.Route).order_by(models.Route.grade_mean.desc()).limit(limit).all()
    return records

def get_best_route_by_country(db: Session, country: str, limit: int = 1) -> List[models.Route]:
    """Obtenir la ou les meilleures routes pour un pays donné, triées par la meilleure note moyenne."""
    records = db.query(models.Route)\
                .filter(models.Route.country == country)\
                .order_by(models.Route.grade_mean.desc())\
                .limit(limit).all()
    return records
