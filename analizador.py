import os
from dotenv import load_dotenv
from datetime import datetime

def iniciar_sistema():
    load_dotenv()
    entorno = os.getenv("MODO_ENTORNO", "desconocido")
    
    print(f"=== Analizador de Inventario Naval - Nauta Systems ===")
    print(f"[{entorno.upper()}] Conectando a servidor de base de datos...\n")
    
    inventario = [
        {"pieza": "Motor Fuera de Borda", "stock": 12, "estado": "optimo"},
        {"pieza": "Válvula de Presión", "stock": 3, "estado": "critico"},
        {"pieza": "Filtro de Aceite", "stock": 45, "estado": "optimo"},
        {"pieza": "Panel de Control", "stock": 1, "estado": "critico"}
    ]
    
    generar_reporte_archivo(inventario)

def generar_reporte_archivo(datos):
    """Genera un archivo .txt con el reporte de stock crítico"""
    # Obtenemos la fecha y hora exacta para que los reportes no se sobreescriban
    fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"reporte_nauta_{fecha_actual}.txt"
    
    # Manejo profesional de archivos en Python usando 'with'
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("--- REPORTE DE STOCK CRÍTICO ---\n")
        piezas_criticas = 0
        
        for item in datos:
            if item["stock"] < 5:
                archivo.write(f"[ALERTA] {item['pieza']} - Quedan {item['stock']} unidades.\n")
                piezas_criticas += 1
                
        archivo.write("--------------------------------\n")
        archivo.write(f"Total de piezas críticas detectadas: {piezas_criticas}\n")
    
    print(f"[EXITO] Reporte generado automáticamente: {nombre_archivo}")

if __name__ == "__main__":
    iniciar_sistema()