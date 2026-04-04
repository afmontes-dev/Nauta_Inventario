from pydantic import BaseModel
from typing import Optional

# --- Esquemas de Inventario ---
class PiezaBase(BaseModel):
    pieza: str
    stock: int
    precio: float

class PiezaNueva(PiezaBase):
    pass

class PiezaRespuesta(PiezaBase):
    id: int
    estado: str
    class Config:
        from_attributes = True

# --- Esquemas de Seguridad ---
class UsuarioCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class PiezaActualizar(BaseModel):
    stock: Optional[int] = None
    precio: Optional[float] = None

class UsuarioRespuesta(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True