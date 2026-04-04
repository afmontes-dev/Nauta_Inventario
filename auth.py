from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

# --- CONFIGURACIÓN DE SEGURIDAD ---
# En un proyecto real, esto iría en el archivo .env
SECRET_KEY = "NAUTA_SECRET_KEY_SUPER_PRO" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Motor de encriptación
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def obtener_password_hash(password):
    """Convierte texto plano en un hash ilegible"""
    return pwd_context.hash(password)

def verificar_password(plain_password, hashed_password):
    """Compara una clave ingresada con el hash guardado"""
    return pwd_context.verify(plain_password, hashed_password)

def crear_token_acceso(data: dict):
    """Genera la 'Llave Digital' (Token JWT)"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt