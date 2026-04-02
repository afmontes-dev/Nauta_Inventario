import os
import json
import csv
from dotenv import load_dotenv
from datetime import datetime

def iniciar_sistema():
    load_dotenv()
    entorno = os.getenv("MODO_ENTORNO", "desconocido")
    
    print(f"=== Analizador de Inventario Naval - Nauta Systems ===")
    print(f"[{entorno.upper()}] Conectando a servidor de base de datos...\n")
    
    # NUEVA LÓGICA: Leer datos desde el archivo externo
    try:
        # Abrimos el archivo en modo lectura ("r" de read)
        with open("base_datos.json", "r", encoding="utf-8") as archivo_json:
            # json.load() traduce el texto del archivo a una lista de diccionarios de Python
            inventario = json.load(archivo_json)
            print(f"[SISTEMA] Base de datos externa cargada. Total de piezas únicas: {len(inventario)}\n")
            
    except FileNotFoundError:
        print("[ERROR] Base de datos no encontrada. Deteniendo sistema de seguridad.")
        return # Si no hay datos, abortamos la ejecución
    
    generar_reporte_archivo(inventario)
    calcular_valor_total(inventario)
    exportar_finanzas_csv(inventario)

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

def exportar_finanzas_csv(datos):
    """Exporta el inventario a un formato amigable para Excel"""
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    nombre_csv = f"finanzas_nauta_{fecha_actual}.csv"
    
    # Abrimos el archivo en modo escritura. 'newline=""' evita saltos de línea extra en Windows
    with open(nombre_csv, mode="w", newline="", encoding="utf-8") as archivo_csv:
        # Definimos cuáles serán los títulos de nuestras columnas
        columnas = ["pieza", "stock", "estado", "precio", "subtotal_usd"]
        
        # DictWriter es un traductor. Le damos las columnas y él acomoda los diccionarios
        escritor = csv.DictWriter(archivo_csv, fieldnames=columnas)
        
        # Escribimos la primera fila (los títulos)
        escritor.writeheader()
        
        # Recorremos el inventario y escribimos fila por fila
        for item in datos:
            # Calculamos el subtotal en tiempo real para agregarlo al reporte
            subtotal = item["stock"] * item["precio"]
            
            # Escribimos la fila asegurándonos de que coincida con las columnas
            escritor.writerow({
                "pieza": item["pieza"],
                "stock": item["stock"],
                "estado": item["estado"],
                "precio": item["precio"],
                "subtotal_usd": subtotal
            })
            
    print(f"[EXITO] Reporte financiero exportado para Excel: {nombre_csv}")

if __name__ == "__main__":
    iniciar_sistema()