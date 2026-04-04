import json

def cargar_inventario(ruta: str = "base_datos.json") -> list | None:
    """
    Carga la base de datos desde un archivo JSON.
    Retorna una lista de diccionarios o None si hay un error crítico.
    """
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        # Si no existe, devolvemos una lista vacía para que el sistema pueda empezar
        return []
    except Exception as e:
        print(f"[ERROR] No se pudo cargar la base de datos: {e}")
        return None

def guardar_inventario(datos: list, ruta: str = "base_datos.json") -> bool:
    """
    Toma la lista actualizada y la sobrescribe en el archivo JSON.
    Retorna True si tuvo éxito, False en caso contrario.
    """
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=2)
        return True
    except Exception as e:
        print(f"[ERROR] Fallo al escribir en el disco: {e}")
        return False