from fastapi import FastAPI
from pydantic import BaseModel
from datos import cargar_inventario, guardar_inventario
from reportes import calcular_finanzas

# 1. Instanciamos la aplicación
app = FastAPI(title="Nauta Systems API")

# 2. Definimos las reglas para piezas nuevas (sin pedir el "estado")
class PiezaNueva(BaseModel):
    pieza: str
    stock: int
    precio: float

# ==========================================
# RUTAS DE LECTURA (GET)
# ==========================================

@app.get("/")
def ruta_principal():
    return {
        "sistema": "Nauta Systems",
        "estado": "En línea",
        "mensaje": "Bienvenido al servidor de inventario naval"
    }

@app.get("/inventario")
def obtener_inventario():
    datos = cargar_inventario()
    if datos is None:
        return {"error": "No se pudo cargar la base de datos"}
    return {"total_piezas": len(datos), "inventario": datos}

@app.get("/finanzas")
def obtener_finanzas():
    datos = cargar_inventario()
    if datos is None:
        return {"error": "No se pudo cargar la base de datos"}
    
    valor_total = calcular_finanzas(datos)
    return {
        "estado": "Calculado", 
        "valor_total_usd": valor_total, 
        "moneda": "USD"
    }

@app.get("/inventario/{nombre_pieza}")
def buscar_pieza(nombre_pieza: str):
    datos = cargar_inventario()
    if datos is None:
        return {"error": "Base de datos no disponible"}
        
    for item in datos:
        if item["pieza"].lower() == nombre_pieza.lower():
            return {
                "encontrado": True, 
                "resultado": item
            }
            
    return {
        "encontrado": False, 
        "mensaje": f"La pieza '{nombre_pieza}' no existe en el almacén de Nauta Systems."
    }

# ==========================================
# RUTAS DE ESCRITURA (POST)
# ==========================================

@app.post("/inventario")
def agregar_pieza(nueva_pieza: PiezaNueva):
    inventario = cargar_inventario()
    if inventario is None:
        return {"error": "Base de datos no disponible"}
        
    # El cerebro de la API calcula el estado automáticamente
    if nueva_pieza.stock < 5:
        estado_calculado = "critico"
    else:
        estado_calculado = "optimo"
        
    pieza_dict = {
        "pieza": nueva_pieza.pieza,
        "stock": nueva_pieza.stock,
        "estado": estado_calculado,
        "precio": nueva_pieza.precio
    }
    
    inventario.append(pieza_dict)
    exito = guardar_inventario(inventario)
    
    if exito:
        return {
            "exito": True, 
            "mensaje": f"La pieza '{nueva_pieza.pieza}' se registró como '{estado_calculado}'."
        }
    else:
        return {"error": "Hubo un problema al escribir en la base de datos."}