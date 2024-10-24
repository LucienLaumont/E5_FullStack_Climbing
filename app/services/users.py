from sqlalchemy.orm import Session
from typing import List
import models, schemas
from sqlalchemy.dialects.postgresql import UUID

def get_all_users(db: Session, skip: int = 0, limit: int = 10) -> List[models.User]:
    """Obtenir tous les users avec pagination."""
    records = db.query(models.User).offset(skip).limit(limit).all()
    return records