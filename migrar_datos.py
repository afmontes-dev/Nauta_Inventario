import json
from database import SessionLocal, engine
import models

# 1. Leer el archivo JSON viejo
try:
    with open("base_datos.json", "r", encoding="utf-8") as f:
        datos_viejos = json.load(f)
except FileNotFoundError:
    print("No se encontró el archivo JSON.")
    datos_viejos = []

# 2. Conectarse a la DB
db = SessionLocal()

# 3. Insertar cada pieza en SQL
print(f"Migrando {len(datos_viejos)} piezas...")

for item in datos_viejos:
    # Verificamos si ya existe para no duplicar si corres el script dos veces
    existe = db.query(models.PiezaDB).filter(models.PiezaDB.pieza == item["pieza"]).first()
    if not existe:
        nueva_pieza = models.PiezaDB(
            pieza=item["pieza"],
            stock=item["stock"],
            precio=item["precio"],
            estado=item["estado"]
        )
        db.add(nueva_pieza)

# 4. Guardar cambios y cerrar
db.commit()
db.close()
print("¡Migración completada con éxito!")