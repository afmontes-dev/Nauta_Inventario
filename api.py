from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import models, schemas, auth
from database import engine, get_db
from reportes import calcular_estado, calcular_finanzas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Nauta Systems API", version="1.2")

# --- RUTAS DE INVENTARIO ---

@app.get("/inventario", tags=["Inventario"])
def obtener_inventario(db: Session = Depends(get_db)):
    piezas = db.query(models.PiezaDB).all()
    return {"total": len(piezas), "items": piezas}

@app.post("/inventario", status_code=status.HTTP_201_CREATED, tags=["Inventario"])
def agregar_pieza(
    nueva_pieza: schemas.PiezaNueva, 
    db: Session = Depends(get_db),
    usuario_actual: models.UsuarioDB = Depends(auth.obtener_usuario_actual) # <--- EL NUEVO CANDADO
):
    existe = db.query(models.PiezaDB).filter(models.PiezaDB.pieza == nueva_pieza.pieza).first()
    if existe:
        raise HTTPException(status_code=409, detail=f"La pieza '{nueva_pieza.pieza}' ya existe.")
    
    pieza_db = models.PiezaDB(
        **nueva_pieza.dict(), 
        estado=calcular_estado(nueva_pieza.stock)
    )
    db.add(pieza_db)
    db.commit()
    db.refresh(pieza_db)
    return {"mensaje": f"Pieza registrada por {usuario_actual.username}", "data": pieza_db}

@app.put("/inventario/{nombre_pieza}", tags=["Inventario"])
def actualizar_pieza(
    nombre_pieza: str, 
    datos: schemas.PiezaActualizar, 
    db: Session = Depends(get_db),
    usuario_actual: models.UsuarioDB = Depends(auth.obtener_usuario_actual) # <--- CANDADO REAL
):
    pieza_db = db.query(models.PiezaDB).filter(models.PiezaDB.pieza == nombre_pieza).first()
    if not pieza_db:
        raise HTTPException(status_code=404, detail="Pieza no encontrada")
    
    if datos.stock is not None:
        pieza_db.stock = datos.stock
        pieza_db.estado = calcular_estado(datos.stock) 
    if datos.precio is not None:
        pieza_db.precio = datos.precio
        
    db.commit()
    db.refresh(pieza_db)
    return {"mensaje": "Actualización exitosa", "operador": usuario_actual.username}

@app.delete("/inventario/{nombre_pieza}", tags=["Inventario"])
def eliminar_pieza(
    nombre_pieza: str, 
    db: Session = Depends(get_db), 
    usuario_actual: models.UsuarioDB = Depends(auth.obtener_usuario_actual) # <--- CANDADO REAL
):
    pieza_db = db.query(models.PiezaDB).filter(models.PiezaDB.pieza == nombre_pieza).first()
    if not pieza_db:
        raise HTTPException(status_code=404, detail="Pieza no encontrada")
    
    db.delete(pieza_db)
    db.commit()
    return {"mensaje": f"Pieza eliminada por {usuario_actual.username}"}

# --- RUTAS DE SEGURIDAD ---

@app.post("/token", tags=["Seguridad"])
def login_para_obtener_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    usuario = db.query(models.UsuarioDB).filter(models.UsuarioDB.username == form_data.username).first()
    if not usuario or not auth.verificar_password(form_data.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_acceso = auth.crear_token_acceso(data={"sub": usuario.username})
    return {"access_token": token_acceso, "token_type": "bearer"}

@app.post("/usuarios/registrar", response_model=schemas.UsuarioRespuesta, tags=["Seguridad"])
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    existe = db.query(models.UsuarioDB).filter(models.UsuarioDB.username == usuario.username).first()
    if existe:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    
    nuevo_usuario = models.UsuarioDB(
        username=usuario.username,
        password_hash=auth.obtener_password_hash(usuario.password)
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario