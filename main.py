# main.py
import reportes
from database import SessionLocal
import models

def ejecutar_reporte_cli():
    # 1. Abrir conexión con el "archivo de acero" (.db)
    db = SessionLocal()
    
    try:
        # 2. Consultar todas las piezas
        piezas_db = db.query(models.PiezaDB).all()
        
        if not piezas_db:
            print("[SISTEMA] No hay datos en la base de datos para procesar.")
            return

        # 3. Convertir objetos de DB a una lista de diccionarios 
        # (Esto es necesario para que tus funciones de 'reportes.py' sigan funcionando)
        inventario = [
            {
                "pieza": p.pieza, 
                "stock": p.stock, 
                "precio": p.precio, 
                "estado": p.estado
            } for p in piezas_db
        ]

        # 4. Usar tu lógica de reportes (¡Aquí no cambia nada, gracias a DRY!)
        print("\n" + "="*30)
        print("   REPORTE NAUTA SYSTEMS")
        print("="*30)
        
        valor_total = reportes.calcular_finanzas(inventario)
        print(f"[FINANZAS] Valor total en bodega: ${valor_total:,.2f} USD")
        
        # Generar archivos físicos
        reportes.generar_alerta_txt(inventario)
        reportes.exportar_csv(inventario)
        
    except Exception as e:
        print(f"[ERROR] Ocurrió un fallo al leer la base de datos: {e}")
    finally:
        # 5. SIEMPRE cerrar la sesión
        db.close()

if __name__ == "__main__":
    ejecutar_reporte_cli()