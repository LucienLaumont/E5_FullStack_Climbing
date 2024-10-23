from sqlalchemy import Column, String, Integer, DateTime, Float
from database import BaseSQL

class Climber(BaseSQL):

    __tablename__ = "climbers"

    user_id = Column(Integer, primary_key=True, index=True)
    country = Column(String, nullable=False)
    sex = Column(Integer, nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    age = Column(Float, nullable=False)
    years_cl = Column(Integer, nullable=False)
    date_first = Column(DateTime, nullable=False)
    date_last = Column(DateTime, nullable=False)
    grades_count = Column(Integer, nullable=False)
    grades_first = Column(Integer, nullable=False)
    grades_last = Column(Integer, nullable=False)
    grades_max = Column(Integer, nullable=False)
    grades_mean = Column(Float, nullable=False)
    year_first = Column(Integer, nullable=False)
    year_last = Column(Integer, nullable=False)

    class Config:
        orm_mode = True


