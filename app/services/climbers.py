from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import distinct, func, case
from fastapi import HTTPException
from datetime import datetime
import models, schemas


def get_all_climbers(db: Session, skip: int = 0, limit: int = 10) -> List[models.Climber]:
    """Obtenir tous les grimpeurs avec pagination."""
    records = db.query(models.Climber).offset(skip).limit(limit).all()
    return records

def get_climber_by_id(db: Session, climber_id: int) -> models.Climber:
    """Obtenir une route par son identifiant (name_id)."""
    record = db.query(models.Climber).filter(models.Climber.climber_id == climber_id).first()
    return record

def create_climber(db: Session, climber: schemas.Climber) -> models.Climber:
    """Ajouter un nouveau grimpeur dans la base de données."""
    db_climber = models.Climber(**climber.dict())  # Utilise Pydantic pour convertir en dict
    db.add(db_climber)
    db.commit()
    db.refresh(db_climber)
    return db_climber

def update_climber(db: Session, climber_id: int, updated_data: schemas.Climber) -> models.Climber:
    """Mettre à jour un grimpeur existant en une seule ligne."""
    db.query(models.Climber).filter(models.Climber.climber_id == climber_id).update(updated_data.dict(exclude_unset=True))
    db.commit()
    db_climber = db.query(models.Climber).filter(models.Climber.climber_id == climber_id).first()
    return db_climber

def delete_climber(db: Session, user_id: int) -> bool:
    """Supprimer une route de la base de données."""
    db_user = db.query(models.Climber).filter(models.Climber.climber_id == user_id).first()

    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

#############################################################################################
#############################################################################################
#############################################################################################

def get_country(db: Session) -> List[str]:
    """Obtenir la liste des pays distincts où se trouvent les grimpeurs."""
    # Utilise distinct pour obtenir les pays uniques
    countries = db.query(distinct(models.Climber.country)).all()
    return [country[0] for country in countries]  # Retourne une liste de pays sous forme de chaînes

def get_climbers_by_sex(db: Session, sex: int):
    """Obtenir tous les grimpeurs filtrés par sexe (0 = femmes, 1 = hommes)."""
    
    # Validation du paramètre `sex`
    if sex not in [0, 1]:
        raise HTTPException(status_code=400, detail="Le paramètre 'sex' doit être 0 pour les femmes ou 1 pour les hommes")

    # Requête pour filtrer les grimpeurs selon le sexe
    records = db.query(models.Climber).filter(models.Climber.sex == sex).all()

    # Si aucun grimpeur trouvé
    if not records:
        raise HTTPException(status_code=404, detail="Aucun grimpeur trouvé pour ce sexe")

    return records

def get_climbers_by_years_climbing(db: Session, min_years: int = 0, max_years: Optional[int] = None):
    """Filtrer les grimpeurs en fonction du nombre d'années d'escalade."""
    query = db.query(models.Climber).filter(models.Climber.years_cl >= min_years)
    if max_years:
        query = query.filter(models.Climber.years_cl <= max_years)
    
    return query.all()

def get_climbers_by_country(db: Session, country: str = "FRA"):
    """Obtenir les grimpeurs venant d'un pays particulier, par défaut 'FRA'."""
    climbers = db.query(models.Climber).filter(models.Climber.country == country).all()

    if not climbers:
        raise HTTPException(status_code=404, detail=f"Aucun grimpeur trouvé pour le pays {country}")

    return climbers

def get_climbers_by_height(db: Session, min_height: float = 190, max_height: Optional[float] = None):
    """Filtrer les grimpeurs en fonction de la taille."""
    query = db.query(models.Climber).filter(models.Climber.height >= min_height)
    if max_height is not None:
        query = query.filter(models.Climber.height <= max_height)
    
    return query.all()

def get_climbers_by_weight(db: Session, min_weight: float = 90, max_weight: Optional[float] = None):
    """Filtrer les grimpeurs en fonction du poids."""
    query = db.query(models.Climber).filter(models.Climber.weight >= min_weight)
    if max_weight is not None:
        query = query.filter(models.Climber.weight <= max_weight)
    
    return query.all()

def get_climbers_by_age(db: Session, min_age: int = 55, max_age: Optional[int] = None):
    """Filtrer les grimpeurs en fonction de l'âge."""
    query = db.query(models.Climber).filter(models.Climber.age >= min_age)
    if max_age is not None:
        query = query.filter(models.Climber.age <= max_age)
    
    return query.all()


#############################################################################################
#############################################################################################
#############################################################################################

def get_climbers_by_genders(db: Session,max_age: int = None):
    # Créer la requête de base pour compter les hommes et les femmes
    query = db.query(models.Climber.sex, func.count(models.Climber.climber_id).label('count'))

    # Appliquer les filtres sur l'âge si fournis
    if max_age is not None:
        query = query.filter(models.Climber.age <= max_age)

    # Grouper les résultats par sexe
    query = query.group_by(models.Climber.sex)

    # Exécuter la requête et obtenir les résultats
    results = query.all()

    # Transformer les résultats en un dictionnaire pour l'API
    data = {sex: count for sex, count in results}

    return data

def get_climbers_by_experience(db: Session, max_age: int):
    """
    Retourne la répartition des grimpeurs par tranches d'années d'expérience
    en fonction de l'âge maximum.
    
    Tranches d'expérience :
    - 0-2 ans
    - 3-5 ans
    - 6-10 ans
    - 10+ ans
    """
    # Initialisation des tranches d'expérience
    experience_buckets = {
        "0-2 ans": 0,
        "3-5 ans": 0,
        "6-10 ans": 0,
        "10+ ans": 0,
    }
    
    # Requête pour récupérer les grimpeurs dont l'âge est inférieur ou égal à l'âge max
    climbers = db.query(models.Climber).filter(models.Climber.age <= max_age).all()

    # Parcourir les grimpeurs et les classer dans les tranches d'années d'expérience
    for climber in climbers:
        if climber.years_cl <= 2:
            experience_buckets["0-2 ans"] += 1
        elif 3 <= climber.years_cl <= 5:
            experience_buckets["3-5 ans"] += 1
        elif 6 <= climber.years_cl <= 10:
            experience_buckets["6-10 ans"] += 1
        else:
            experience_buckets["10+ ans"] += 1
    
    return experience_buckets

def get_climbers_by_countries(db: Session, max_age: int, limit: int):
    """
    Retourne la répartition des grimpeurs par pays (max 5 pays),
    filtrée par l'âge maximum spécifié.
    """
    # Requête pour obtenir le nombre de grimpeurs par pays, filtré par l'âge maximum
    country_counts = (
        db.query(models.Climber.country, func.count(models.Climber.climber_id).label("count"))
        .filter(models.Climber.age <= max_age)
        .group_by(models.Climber.country)
        .order_by(func.count(models.Climber.climber_id).desc())  # Trier par nombre de grimpeurs
        .limit(limit)  # Limiter à 5 pays
        .all()
    )

    # Conversion du résultat en dictionnaire { 'Pays': nombre_grimpeurs }
    result = {country: count for country, count in country_counts}
    return result

def get_grades_by_age(db: Session, max_age: int):
    """
    Retourne la moyenne des grades maximum par âge des grimpeurs, filtrés par un âge maximum.
    """
    # Requête pour calculer la moyenne des grades_max pour chaque âge
    grades_by_age = (
        db.query(models.Climber.age, func.avg(models.Climber.grades_max).label("average_grade_max"))
        .filter(models.Climber.age <= max_age)
        .group_by(models.Climber.age)
        .all()
    )

    # Retourne les résultats sous forme de liste de dicts [{'age': age, 'average_grade_max': avg_grade}]
    return [{"age": age, "average_grade_max": average_grade_max} for age, average_grade_max in grades_by_age]
