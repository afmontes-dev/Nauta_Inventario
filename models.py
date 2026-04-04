from sqlalchemy import Column, Integer, String, Float
from database import Base

class PiezaDB(Base):
    __tablename__ = "inventario"

    id = Column(Integer, primary_key=True, index=True)
    pieza = Column(String, unique=True, index=True)
    stock = Column(Integer)
    estado = Column(String)
    precio = Column(Float)