from sqlalchemy import Column, Integer, String, Float
from database import Base

# 1. Tabla de Inventario (Solo una vez)
class PiezaDB(Base):
    __tablename__ = "inventario"
    id = Column(Integer, primary_key=True, index=True)
    pieza = Column(String, unique=True, index=True)
    stock = Column(Integer)
    estado = Column(String)
    precio = Column(Float)

# 2. Tabla de Usuarios (La nueva)
class UsuarioDB(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)