import csv
from datetime import datetime

def generar_alerta_txt(datos: list[dict]) -> None:
    """
    Filtra piezas en estado crítico y genera un reporte de texto para compras.
    """
    criticos = [item for item in datos if item["estado"] == "critico"]
    
    with open("alertas_stock.txt", "w", encoding="utf-8") as f:
        f.write("--- ALERTA DE REPOSICIÓN NAUTA SYSTEMS ---\n")
        if not criticos:
            f.write("Todo el stock se encuentra en niveles óptimos.\n")
        for p in criticos:
            f.write(f"REVISAR: {p['pieza']} | Stock actual: {p['stock']}\n")
    print("[SISTEMA] Reporte de alertas generado en 'alertas_stock.txt'")

def exportar_csv(datos: list[dict]) -> None:
    """
    Exporta el inventario completo a un formato CSV compatible con Excel.
    """
    try:
        with open("inventario_nauta.csv", "w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=["pieza", "stock", "estado", "precio"])
            escritor.writeheader()
            escritor.writerows(datos)
        print("[SISTEMA] Inventario exportado exitosamente a 'inventario_nauta.csv'")
    except Exception as e:
        print(f"[ERROR] No se pudo exportar a CSV: {e}")

def calcular_finanzas(datos: list[dict]) -> float:
    """
    Calcula el valor total del inventario multiplicando stock por precio de cada item.
    Retorna un número decimal (float).
    """
    total = 0.0
    for item in datos:
        total += float(item["stock"]) * float(item["precio"])
    return total

def calcular_estado(stock: int) -> str:
    """
    Aplica la regla de negocio para determinar el estado de una pieza.
    """
    return "critico" if stock < 5 else "optimo"