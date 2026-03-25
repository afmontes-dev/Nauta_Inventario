import os
from dotenv import load_dotenv

def iniciar_sistema():
    # 1. Cargar las variables secretas del archivo .env a la memoria
    load_dotenv()
    
    # 2. Leer las variables específicas
    api_key = os.getenv("NAUTA_API_KEY")
    entorno = os.getenv("MODO_ENTORNO", "desconocido") # "desconocido" es un valor por defecto por si falla
    
    print(f"=== Analizador de Inventario Naval - Nauta Systems ===")
    # NUNCA imprimimos la clave completa en consola, solo una parte para debug
    print(f"[{entorno.upper()}] Conectando a servidor con API Key: {api_key[:5]}***\n")
    
    inventario = [
        {"pieza": "Motor Fuera de Borda", "stock": 12, "estado": "optimo"},
        {"pieza": "Válvula de Presión", "stock": 3, "estado": "critico"},
        {"pieza": "Filtro de Aceite", "stock": 45, "estado": "optimo"},
        {"pieza": "Panel de Control", "stock": 1, "estado": "critico"}
    ]
    
    analizar_stock_critico(inventario)

def analizar_stock_critico(datos):
    """Filtra y muestra únicamente las piezas con stock menor a 5"""
    print("--- REPORTE DE STOCK CRÍTICO ---")
    for item in datos:
        if item["stock"] < 5:
            print(f"[ALERTA] {item['pieza']} - Solo quedan {item['stock']} unidades.")
    print("--------------------------------\n")

if __name__ == "__main__":
    iniciar_sistema()