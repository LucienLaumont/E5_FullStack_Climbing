from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import distinct, func
from fastapi import HTTPException
from datetime import datetime
import models, schemas


def get_all_climbers(db: Session, skip: int = 0, limit: int = 10) -> List[models.Climber]:
    """Obtenir tous les grimpeurs avec pagination."""
    records = db.query(models.Climber).offset(skip).limit(limit).all()
    return records

def get_climber_by_id(db: Session, user_id: int) -> models.Climber:
    """Obtenir une route par son identifiant (name_id)."""
    record = db.query(models.Climber).filter(models.Climber.user_id == user_id).first()
    return record

def create_climber(db: Session, climber: schemas.ClimberCreate) -> models.Climber:
    """Ajouter un nouveau grimpeur dans la base de données."""
    db_climber = models.Climber(**climber.dict())  # Utilise Pydantic pour convertir en dict
    db.add(db_climber)
    db.commit()
    db.refresh(db_climber)
    return db_climber

def update_climber(db: Session, climber_id: int, updated_data: schemas.ClimberCreate) -> models.Climber:
    """Mettre à jour un grimpeur existant dans la base de données."""
    db_climber = db.query(models.Climber).filter(models.Climber.user_id == climber_id).first()

    if db_climber:
        updated_data_dict = updated_data.dict(exclude_unset=True)  # Seuls les champs avec des valeurs
        for key, value in updated_data_dict.items():
            setattr(db_climber, key, value)  # Met à jour chaque attribut de manière dynamique
        
        db.commit()
        db.refresh(db_climber)
        return db_climber
    else:
        return None

def update_climber(db: Session, climber_id: int, updated_data: schemas.ClimberCreate) -> models.Climber:
    """Mettre à jour un grimpeur existant en une seule ligne."""
    db.query(models.Climber).filter(models.Climber.user_id == climber_id).update(updated_data.dict(exclude_unset=True))
    db.commit()
    db_climber = db.query(models.Climber).filter(models.Climber.user_id == climber_id).first()
    return db_climber

def delete_climber(db: Session, user_id: int) -> bool:
    """Supprimer une route de la base de données."""
    db_user = db.query(models.Climber).filter(models.Climber.user_id == user_id).first()

    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False



def get_country(db: Session) -> List[str]:
    """Obtenir la liste des pays distincts où se trouvent les grimpeurs."""
    # Utilise distinct pour obtenir les pays uniques
    countries = db.query(distinct(models.Climber.country)).all()
    return [country[0] for country in countries]  # Retourne une liste de pays sous forme de chaînes


def get_climbers_by_country(name: str, db: Session) -> List[models.Climber]:
    """Obtenir des grimpeurs originaire d'un pays."""
    records = db.query(models.Climber).filter(models.Climber.country == name).all()
    return records

def get_climbers_count_by_country(db: Session):
    """Obtenir le nombre de grimpeurs pour chaque pays."""
    # Utilise la fonction SQL COUNT et GROUP BY pour compter les grimpeurs par pays
    records = db.query(
        models.Climber.country, func.count(models.Climber.user_id).label('climber_count')
    ).group_by(models.Climber.country).all()

    return records

def get_youngest_climbers(db: Session, limit: int = 10) -> List[models.Climber]:
    """Obtenir les grimpeurs les plus jeunes."""
    records = db.query(models.Climber).order_by(models.Climber.age.asc()).limit(limit).all()
    return records

def get_oldest_climbers(db: Session, limit: int = 10) -> List[models.Climber]:
    """Obtenir les grimpeurs les plus âgés."""
    records = db.query(models.Climber).order_by(models.Climber.age.desc()).limit(limit).all()
    return records

def get_tallest_climbers(db: Session, limit: int = 10) -> List[models.Climber]:
    """Obtenir les grimpeurs les plus grands."""
    records = db.query(models.Climber).order_by(models.Climber.height.desc()).limit(limit).all()
    return records

def get_shortest_climbers(db: Session, limit: int = 10) -> List[models.Climber]:
    """Obtenir les grimpeurs les plus petits."""
    records = db.query(models.Climber).order_by(models.Climber.height.asc()).limit(limit).all()
    return records