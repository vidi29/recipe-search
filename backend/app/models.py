from sqlalchemy import Column, Integer, Text, String, Float, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    ingredients = Column(Text, nullable=False)  # store as joined string
    steps = Column(Text)
    calories = Column(Float, nullable=True)
    halal = Column(Integer, default=0)  # 0/1
    vegetarian = Column(Integer, default=0)  # 0/1
    image_path = Column(String(512), nullable=True)
