def iniciar_sistema():
    print("=== Analizador de Inventario Naval - Nauta Systems ===")
    print("Cargando módulos de automatización...\n")
    
    # Simulando un JSON que extrajiste de una base de datos o API
    inventario = [
        {"pieza": "Motor Fuera de Borda", "stock": 12, "estado": "optimo"},
        {"pieza": "Válvula de Presión", "stock": 3, "estado": "critico"},
        {"pieza": "Filtro de Aceite", "stock": 45, "estado": "optimo"},
        {"pieza": "Panel de Control", "stock": 1, "estado": "critico"}
    ]
    
    print(f"Total de categorías en base de datos: {len(inventario)}")
    
    # Delegamos la responsabilidad de analizar a otra función
    analizar_stock_critico(inventario)

def analizar_stock_critico(datos):
    """Filtra y muestra únicamente las piezas con stock menor a 5"""
    print("\n--- REPORTE DE STOCK CRÍTICO ---")
    for item in datos:
        if item["stock"] < 5:
            print(f"[ALERTA] {item['pieza']} - Solo quedan {item['stock']} unidades.")
    print("--------------------------------\n")

if __name__ == "__main__":
    iniciar_sistema()