import os
from dotenv import load_dotenv

# Importamos nuestras propias herramientas desde los otros archivos
from datos import cargar_inventario
from reportes import generar_alerta_txt, calcular_finanzas, exportar_csv

def iniciar_sistema():
    load_dotenv()
    entorno = os.getenv("MODO_ENTORNO", "desconocido")
    
    print("==================================================")
    print("   SISTEMA DE INVENTARIO NAVAL - NAUTA SYSTEMS")
    print("==================================================")
    print(f"[{entorno.upper()}] Iniciando módulos de automatización...\n")
    
    # 1. El jefe pide los datos
    inventario = cargar_inventario()
    
    # Si la base de datos existe, el jefe delega el trabajo a los reportes
    if inventario:
        generar_alerta_txt(inventario)
        calcular_finanzas(inventario)
        exportar_csv(inventario)
        print("\n[SISTEMA] Todas las operaciones finalizaron con éxito.")

if __name__ == "__main__":
    iniciar_sistema()