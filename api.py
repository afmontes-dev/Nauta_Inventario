from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from reportes import calcular_finanzas, calcular_estado
from sqlalchemy.orm import Session
from database import get_db

import models
from database import engine

# Esto crea las tablas en el archivo .db automáticamente
models.Base.metadata.create_all(bind=engine)

# 1. Instanciamos la aplicación con metadatos profesionales
app = FastAPI(title="Nauta Systems API v1.1")

# 2. Esquemas de validación (Pydantic)
class PiezaNueva(BaseModel):
    pieza: str
    stock: int
    precio: float

class PiezaActualizar(BaseModel):
    stock: int
    precio: float

# ==========================================
# RUTAS DE LECTURA (GET)
# ==========================================

@app.get("/")
def ruta_principal():
    return {"sistema": "Nauta Systems", "estado": "Operativo"}

@app.get("/inventario")
def obtener_inventario(db: Session = Depends(get_db)): # <-- Inyectamos la sesión
    # En SQL no cargamos un JSON, hacemos una consulta (Query)
    piezas = db.query(models.PiezaDB).all()
    return {"total": len(piezas), "items": piezas}

@app.get("/finanzas")
def obtener_finanzas():
    datos = cargar_inventario()
    if datos is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al acceder a los datos financieros."
        )
    
    valor_total = calcular_finanzas(datos)
    return {"estado": "Calculado", "valor_total_usd": valor_total}

@app.get("/inventario/{nombre_pieza}")
def buscar_pieza(nombre_pieza: str):
    datos = cargar_inventario()
    if datos is None:
        raise HTTPException(status_code=500, detail="Error de servidor.")
        
    for item in datos:
        if item["pieza"].lower() == nombre_pieza.lower():
            return item
            
    # REGLA 1: Si no existe, lanzamos 404 real
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"La pieza '{nombre_pieza}' no se encuentra en el registro."
    )

# ==========================================
# RUTAS DE ESCRITURA (POST, PUT, DELETE)
# ==========================================

@app.post("/inventario", status_code=status.HTTP_201_CREATED)
def agregar_pieza(nueva_pieza: PiezaNueva, db: Session = Depends(get_db)):
    # 1. Validación de duplicados (Ahora con una consulta SQL rápida)
    existe = db.query(models.PiezaDB).filter(models.PiezaDB.pieza == nueva_pieza.pieza).first()
    if existe:
        raise HTTPException(status_code=409, detail=f"La pieza '{nueva_pieza.pieza}' ya existe.")
    
    # 2. Calcular estado (seguimos usando nuestro 'cerebro' en reportes.py)
    from reportes import calcular_estado
    estado_calculado = calcular_estado(nueva_pieza.stock)
    
    # 3. Crear el objeto de base de datos
    nueva_pieza_db = models.PiezaDB(
        pieza=nueva_pieza.pieza,
        stock=nueva_pieza.stock,
        precio=nueva_pieza.precio,
        estado=estado_calculado
    )
    
    # 4. Guardar en la DB
    db.add(nueva_pieza_db)
    db.commit()
    db.refresh(nueva_pieza_db) # Para obtener el ID generado automáticamente
    
    return {"mensaje": "Registro creado en DB", "data": nueva_pieza_db}

@app.put("/inventario/{nombre_pieza}")
def actualizar_pieza(nombre_pieza: str, datos_nuevos: PiezaActualizar):
    inventario = cargar_inventario()
    if inventario is None:
        raise HTTPException(status_code=500, detail="Error de servidor.")
        
    for item in inventario:
        if item["pieza"].lower() == nombre_pieza.lower():
            item["stock"] = datos_nuevos.stock
            item["precio"] = datos_nuevos.precio
            item["estado"] = calcular_estado(item["stock"])
            
            if guardar_inventario(inventario):
                return {"mensaje": "Actualización exitosa", "data": item}
            raise HTTPException(status_code=500, detail="Error al guardar cambios.")
                
    # REGLA 1: Si intentas actualizar algo que no existe -> 404
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Imposible actualizar: '{nombre_pieza}' no existe."
    )

@app.delete("/inventario/{nombre_pieza}")
def eliminar_pieza(nombre_pieza: str):
    inventario = cargar_inventario()
    if inventario is None:
        raise HTTPException(status_code=500, detail="Error de servidor.")
        
    for i, item in enumerate(inventario):
        if item["pieza"].lower() == nombre_pieza.lower():
            pieza_removida = inventario.pop(i)
            if guardar_inventario(inventario):
                return {"mensaje": f"Pieza '{pieza_removida['pieza']}' eliminada correctamente."}
            raise HTTPException(status_code=500, detail="Error al procesar eliminación.")
                
    # REGLA 1: Si intentas borrar algo que no existe -> 404
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Error: No se pudo eliminar '{nombre_pieza}' porque no existe."
    )