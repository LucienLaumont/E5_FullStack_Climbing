from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from database import BaseSQL
from uuid import uuid4

class User(BaseSQL):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now) 

    climbers = relationship("Climber", back_populates="user")
    routes = relationship("Route", back_populates="user")
