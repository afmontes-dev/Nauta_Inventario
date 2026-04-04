from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List

# Importaciones de nuestros módulos locales
import models
import schemas
import auth
from database import engine, get_db
from reportes import calcular_estado, calcular_finanzas

# Creamos las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Nauta Systems API",
    description="Sistema de gestión de inventario para repuestos navales",
    version="1.2"
)

from fastapi.security import OAuth2PasswordBearer # Asegúrate de tener este import
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    # Esta función simplemente verifica que el token exista. 
    # Por ahora, si hay token, dejamos pasar.
    if not token:
        raise HTTPException(status_code=401, detail="No autorizado")
    return token

# --- RUTAS DE INVENTARIO ---

@app.get("/", tags=["General"])
def ruta_principal():
    return {"mensaje": "Bienvenido a la consola de mando de Nauta Systems"}

@app.get("/inventario", tags=["Inventario"])
def obtener_inventario(db: Session = Depends(get_db)):
    # 1. Traer los objetos de la base de datos
    piezas = db.query(models.PiezaDB).all()
    
    # 2. Si no hay nada, devolvemos una lista vacía para que no explote
    if not piezas:
        return {"total": 0, "items": []}
        
    return {"total": len(piezas), "items": piezas}

@app.post("/inventario", status_code=status.HTTP_201_CREATED, tags=["Inventario"])
def agregar_pieza(
    nueva_pieza: schemas.PiezaNueva, 
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme) # <--- EL CANDADO FINAL
):
    # 1. Validación de duplicados (Nadie puede duplicar piezas, ni el capitán)
    existe = db.query(models.PiezaDB).filter(models.PiezaDB.pieza == nueva_pieza.pieza).first()
    if existe:
        raise HTTPException(status_code=409, detail=f"La pieza '{nueva_pieza.pieza}' ya existe.")
    
    # 2. Lógica de negocio (Estado calculado automáticamente)
    estado_calculado = calcular_estado(nueva_pieza.stock)
    
    # 3. Guardar en SQL (Persistencia de acero)
    pieza_db = models.PiezaDB(
        pieza=nueva_pieza.pieza,
        stock=nueva_pieza.stock,
        precio=nueva_pieza.precio,
        estado=estado_calculado
    )
    
    db.add(pieza_db)
    db.commit()
    db.refresh(pieza_db)
    
    return {"mensaje": "Pieza registrada con éxito", "data": pieza_db}

@app.get("/finanzas", tags=["Reportes"])
def obtener_finanzas(db: Session = Depends(get_db)):
    piezas = db.query(models.PiezaDB).all()
    # Convertimos objetos de DB a diccionarios para la función de finanzas
    datos_lista = [{"precio": p.precio, "stock": p.stock} for p in piezas]
    total = calcular_finanzas(datos_lista)
    return {"valor_total_inventario": total, "moneda": "USD"}

# --- RUTAS DE SEGURIDAD (BLOQUE 2) ---

@app.post("/usuarios/registrar", response_model=schemas.UsuarioRespuesta, tags=["Seguridad"]) # <-- Cambiado aquí
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    # 1. Verificar si el usuario ya existe
    existe = db.query(models.UsuarioDB).filter(models.UsuarioDB.username == usuario.username).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El nombre de usuario ya está registrado"
        )
    
    # 2. Encriptar contraseña
    hashed_pwd = auth.obtener_password_hash(usuario.password)
    
    # 3. Crear registro
    nuevo_usuario = models.UsuarioDB(
        username=usuario.username,
        password_hash=hashed_pwd
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return nuevo_usuario # Ahora FastAPI solo sacará el ID y el Username

@app.put("/inventario/{nombre_pieza}", tags=["Inventario"])
def actualizar_pieza(
    nombre_pieza: str, 
    datos: schemas.PiezaActualizar, 
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme) # <--- EL CANDADO MÁGICO
):
    # 1. Buscar la pieza en la base de datos
    pieza_db = db.query(models.PiezaDB).filter(models.PiezaDB.pieza == nombre_pieza).first()
    
    if not pieza_db:
        raise HTTPException(status_code=404, detail="Pieza no encontrada")
    
    # 2. Actualizar solo los campos enviados (si el token es válido)
    if datos.stock is not None:
        pieza_db.stock = datos.stock
        # Importante: Usamos tu lógica de reportes para recalcular el estado
        pieza_db.estado = calcular_estado(datos.stock) 
        
    if datos.precio is not None:
        pieza_db.precio = datos.precio
        
    # 3. Guardar cambios en el "archivo de acero" (.db)
    db.commit()
    db.refresh(pieza_db)
    
    return {"mensaje": "Pieza actualizada con éxito", "data": pieza_db}

# Importante: Asegúrate de tener 'oauth2_scheme' definido antes de las rutas
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.delete("/inventario/{nombre_pieza}", tags=["Inventario"])
def eliminar_pieza(
    nombre_pieza: str, 
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme) # <--- ¡ESTE ES EL CANDADO!
):
    # 1. El sistema verificará el token ANTES de entrar aquí
    pieza_db = db.query(models.PiezaDB).filter(models.PiezaDB.pieza == nombre_pieza).first()
    
    if not pieza_db:
        raise HTTPException(status_code=404, detail="Pieza no encontrada")
    
    # 2. Si llegamos aquí, es porque el usuario está autenticado y la pieza existe
    db.delete(pieza_db)
    db.commit()
    
    return {"mensaje": f"Pieza '{nombre_pieza}' eliminada con éxito"}

from fastapi.security import OAuth2PasswordRequestForm # <-- AÑADE ESTE IMPORT ARRIBA

@app.post("/token", tags=["Seguridad"])
def login_para_obtener_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # 1. Buscar al usuario
    usuario = db.query(models.UsuarioDB).filter(models.UsuarioDB.username == form_data.username).first()
    
    # 2. Validar usuario y contraseña (usando auth.py)
    if not usuario or not auth.verificar_password(form_data.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Generar el Token (Llave Digital)
    token_acceso = auth.crear_token_acceso(data={"sub": usuario.username})
    
    return {"access_token": token_acceso, "token_type": "bearer"}