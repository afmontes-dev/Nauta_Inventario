import csv
from datetime import datetime

def generar_alerta_txt(datos):
    fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"reporte_nauta_{fecha_actual}.txt"
    
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("--- REPORTE DE STOCK CRÍTICO ---\n")
        piezas_criticas = 0
        for item in datos:
            if item["stock"] < 5:
                archivo.write(f"[ALERTA] {item['pieza']} - Quedan {item['stock']} unidades.\n")
                piezas_criticas += 1
        archivo.write("--------------------------------\n")
        archivo.write(f"Total de piezas críticas detectadas: {piezas_criticas}\n")
    print(f"[REPORTES] TXT de alertas generado: {nombre_archivo}")

def calcular_finanzas(datos):
    valor_total = 0.0
    for item in datos:
        valor_total += item["stock"] * item["precio"]
    print(f"[FINANZAS] El valor total del inventario es: ${valor_total:,.2f}")

def exportar_csv(datos):
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    nombre_csv = f"finanzas_nauta_{fecha_actual}.csv"
    
    with open(nombre_csv, mode="w", newline="", encoding="utf-8") as archivo_csv:
        columnas = ["pieza", "stock", "estado", "precio", "subtotal_usd"]
        escritor = csv.DictWriter(archivo_csv, fieldnames=columnas)
        escritor.writeheader()
        
        for item in datos:
            subtotal = item["stock"] * item["precio"]
            escritor.writerow({
                "pieza": item["pieza"],
                "stock": item["stock"],
                "estado": item["estado"],
                "precio": item["precio"],
                "subtotal_usd": subtotal
            })
    print(f"[REPORTES] CSV financiero exportado: {nombre_csv}")