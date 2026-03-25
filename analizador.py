def iniciar_sistema():
    # Esta función tiene una sola responsabilidad: arrancar el programa
    print("=== Analizador de Inventario Naval - Nauta Systems ===")
    print("Cargando módulos de automatización...")
    
    piezas_base = ["Motor Fuera de Borda", "Válvula de Presión", "Filtro de Aceite"]
    print(f"Estado inicial: {len(piezas_base)} categorías de piezas detectadas.")

# Este es el punto de entrada profesional de cualquier script en Python
if __name__ == "__main__":
    iniciar_sistema()