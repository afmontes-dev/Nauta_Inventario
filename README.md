# Nauta Systems - Sistema de Inventario Naval ⚓

Un sistema backend robusto construido en Python para la gestión, control financiero y automatización de inventarios de piezas navales.

## 🚀 Tecnologías Utilizadas
* **Python 3**
* **FastAPI:** Framework web moderno y de alto rendimiento para construir APIs con Python.
* **Uvicorn:** Servidor ASGI ultrarrápido.
* **Pydantic:** Validación de datos y gestión de configuraciones.
* **Base de Datos Local:** Gestión de persistencia mediante archivos JSON.

## 🏗️ Arquitectura del Proyecto
El proyecto está construido bajo un patrón de diseño modular para garantizar su escalabilidad:
* `api.py`: Controlador principal (Cerebro de la API) y definición de rutas.
* `datos.py`: Módulo de persistencia (Operaciones de lectura y escritura en JSON).
* `reportes.py`: Módulo de lógica de negocios y cálculos financieros.
* `base_datos.json`: Almacenamiento persistente del inventario.

## 🔌 API Endpoints (CRUD)
El sistema cuenta con una API RESTful documentada automáticamente mediante Swagger UI (OpenAPI):

| Verbo HTTP | Endpoint | Descripción |
| :--- | :--- | :--- |
| **GET** | `/` | Ruta principal para verificar el estado del servidor. |
| **GET** | `/inventario` | Retorna el inventario completo. |
| **GET** | `/inventario/{nombre_pieza}` | Buscador de piezas específicas (insensible a mayúsculas/minúsculas). |
| **GET** | `/finanzas` | Retorna el cálculo total del valor del inventario en USD. |
| **POST** | `/inventario` | Registra una nueva pieza. (El sistema calcula el estado automáticamente). |
| **PUT** | `/inventario/{nombre_pieza}` | Actualiza el stock y precio de una pieza existente, recalculando su estado. |
| **DELETE** | `/inventario/{nombre_pieza}`| Elimina permanentemente una pieza del sistema. |

## 🛠️ Instalación y Ejecución Local

1. Clonar el repositorio.
2. Activar el entorno virtual:
   ```bash
   .\venv\Scripts\activate
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecutar el servidor:
   ```bash
   uvicorn api:app --reload
   ```
5. Acceder a la documentación interactiva en: `http://localhost:8000/docs` 