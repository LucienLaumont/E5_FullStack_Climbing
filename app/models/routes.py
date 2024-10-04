from sqlalchemy import Column, String, Integer, Float
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

