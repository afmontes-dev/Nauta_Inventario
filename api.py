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
# Reglas para cuando alguien quiere actualizar (solo le pedimos stock y precio)
class PiezaActualizar(BaseModel):
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

# ==========================================
# RUTAS DE ELIMINACIÓN (DELETE)
# ==========================================

@app.delete("/inventario/{nombre_pieza}")
def eliminar_pieza(nombre_pieza: str):
    inventario = cargar_inventario()
    if inventario is None:
        return {"error": "Base de datos no disponible"}
        
    # Recorremos el inventario usando 'enumerate' para saber en qué posición exacta (índice) estamos
    for i, item in enumerate(inventario):
        if item["pieza"].lower() == nombre_pieza.lower():
            # Si hay coincidencia, sacamos la pieza de la lista usando su índice 'i'
            pieza_eliminada = inventario.pop(i)
            
            # Guardamos la lista actualizada (ahora con un elemento menos)
            exito = guardar_inventario(inventario)
            
            if exito:
                return {"exito": True, "mensaje": f"La pieza '{pieza_eliminada['pieza']}' fue eliminada permanentemente."}
            else:
                return {"error": "Error al intentar guardar los cambios en el archivo."}
                
    # Si el bucle termina sin encontrar nada, avisamos que la pieza no existe
    return {"error": True, "mensaje": f"La pieza '{nombre_pieza}' no se encontró en el inventario."}

# ==========================================
# RUTAS DE ACTUALIZACIÓN (PUT)
# ==========================================

@app.put("/inventario/{nombre_pieza}")
def actualizar_pieza(nombre_pieza: str, datos_nuevos: PiezaActualizar):
    inventario = cargar_inventario()
    if inventario is None:
        return {"error": "Base de datos no disponible"}
        
    for item in inventario:
        if item["pieza"].lower() == nombre_pieza.lower():
            # 1. Actualizamos los valores numéricos
            item["stock"] = datos_nuevos.stock
            item["precio"] = datos_nuevos.precio
            
            # 2. El servidor vuelve a usar su inteligencia para recalcular el estado
            if item["stock"] < 5:
                item["estado"] = "critico"
            else:
                item["estado"] = "optimo"
                
            # 3. Guardamos los cambios
            exito = guardar_inventario(inventario)
            
            if exito:
                return {
                    "exito": True, 
                    "mensaje": f"La pieza '{item['pieza']}' fue actualizada con éxito.",
                    "datos_actualizados": item
                }
            else:
                return {"error": "Error al intentar guardar los cambios."}
                
    # Si termina el ciclo y no la encuentra
    return {"error": True, "mensaje": f"La pieza '{nombre_pieza}' no existe."}