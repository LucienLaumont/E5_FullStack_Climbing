from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from database import BaseSQL

class Route(BaseSQL):
    __tablename__ = "routes"

    name_id = Column(Integer, primary_key=True, index=True)
    country = Column(String, nullable=False)
    crag = Column(String, nullable=False)
    sector = Column(String, nullable=False)
    name = Column(String, nullable=False)
    tall_recommend_sum = Column(Integer, nullable=False, default=-1)
    grade_mean = Column(Float, nullable=False)
    cluster = Column(Integer, nullable=False)
    rating_tot = Column(Float, nullable=False)
    # Clé étrangère qui fait référence à la table users
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    # Définir la relation avec le modèle User
    user = relationship("User", back_populates="routes")
    class Config:
        orm_mode = True

