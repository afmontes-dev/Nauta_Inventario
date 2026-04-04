from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import database, models  # Importamos para buscar al usuario en la DB

# --- CONFIGURACIÓN ---
SECRET_KEY = "NAUTA_SECRET_KEY_SUPER_PRO" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def obtener_password_hash(password):
    return pwd_context.hash(password)

def verificar_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def crear_token_acceso(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- LA NUEVA FUNCIÓN MAESTRA ---
def obtener_usuario_actual(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el acceso",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 1. Decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # 2. Extraer el campo 'sub' (username)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        # 3. Lanzar 401 si el token es inválido o expiró
        raise credentials_exception

    # 4. Buscar el usuario en la DB
    usuario = db.query(models.UsuarioDB).filter(models.UsuarioDB.username == username).first()
    
    # 5. Si el usuario no existe en la DB (aunque el token sea válido)
    if usuario is None:
        raise credentials_exception
        
    # 6. Retornar el objeto UsuarioDB completo
    return usuario