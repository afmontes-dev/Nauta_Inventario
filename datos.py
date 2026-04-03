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

def guardar_inventario(datos, ruta="base_datos.json"):
    """Toma la lista actualizada y sobrescribe el archivo JSON"""
    try:
        # Abrimos en modo escritura ("w" de write)
        with open(ruta, "w", encoding="utf-8") as archivo:
            # json.dump() traduce la lista de Python de vuelta a texto JSON
            # indent=2 hace que el archivo quede bonito y fácil de leer
            json.dump(datos, archivo, indent=2)
        return True
    except Exception as e:
        print(f"[ERROR] No se pudo guardar la base de datos: {e}")
        return False