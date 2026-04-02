# Analizador de Inventario - Nauta Systems
Script de automatización base para la lectura y gestión de componentes del sector naval.

## 🚀 Características
- **Lectura de Datos**: Extrae información desde `base_datos.json`.
- **Reportes Automáticos**: Genera archivos `.txt` con alertas de stock bajo.
- **Análisis Financiero**: Calcula el valor total del inventario y exporta a `.csv`.
- **Configuración Flexible**: Usa variables de entorno para configurar el modo de operación.

## 🛠️ Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/afmontes-dev/Nauta_Inventario.git
   cd Nauta_Inventario
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuración
Crea un archivo `.env` en la raíz del proyecto para configurar el entorno:

```env
MODO_ENTORNO=desarrollo
```

## 🏃 Ejecución
Ejecuta el script principal:

```bash
python main.py
```

## 📂 Estructura del Proyecto
- `main.py`: Orquestador principal del sistema.
- `datos.py`: Módulo para la lectura de la base de datos.
- `reportes.py`: Módulo para la generación de reportes y análisis financieros.
- `base_datos.json`: Archivo de datos principal.
- `.env`: Variables de entorno.

## 📝 Licencia
Este proyecto es de código cerrado y propiedad de Nauta Systems.