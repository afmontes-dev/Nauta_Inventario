import os
from dotenv import load_dotenv
from datetime import datetime

def iniciar_sistema():
    load_dotenv()
    entorno = os.getenv("MODO_ENTORNO", "desconocido")
    
    print(f"=== Analizador de Inventario Naval - Nauta Systems ===")
    print(f"[{entorno.upper()}] Conectando a servidor de base de datos...\n")
    
    inventario = [
        {"pieza": "Motor Fuera de Borda", "stock": 12, "estado": "optimo", "precio": 4500.50},
        {"pieza": "Válvula de Presión", "stock": 3, "estado": "critico", "precio": 150.00},
        {"pieza": "Filtro de Aceite", "stock": 45, "estado": "optimo", "precio": 25.50},
        {"pieza": "Panel de Control", "stock": 1, "estado": "critico", "precio": 1200.00}
    ]
    
    generar_reporte_archivo(inventario)
    calcular_valor_total(inventario)

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

def calcular_valor_total(datos):
    """Calcula el valor total en dólares de todo el inventario"""
    valor_total = 0.0  # Empezamos con la alcancía en cero
    
    for item in datos:
        # Por cada pieza, calculamos su valor y lo sumamos a la alcancía
        subtotal = item["stock"] * item["precio"]
        valor_total += subtotal
        
    # Imprimimos el resultado con formato de moneda
    print(f"\n[FINANZAS] El valor total del inventario es: ${valor_total:,.2f}")
    
if __name__ == "__main__":
    iniciar_sistema()