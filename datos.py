import json

def cargar_inventario(ruta="base_datos.json"):
    """Se encarga exclusivamente de extraer los datos y devolverlos"""
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            print(f"[DATOS] Base de datos leída con éxito. Piezas detectadas: {len(datos)}")
            return datos
    except FileNotFoundError:
        print(f"[ERROR] No se encontró la base de datos en: {ruta}")
        return None