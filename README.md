# 🚀 Nauta Systems - v1.2 (Security & SQL Update)

Sistema profesional de gestión de inventario para repuestos navales, desarrollado con **FastAPI**. Esta versión migra la persistencia de datos a una estructura relacional y añade capas de seguridad de grado industrial.

## 🛠️ Tecnologías y Arquitectura
* **Base de Datos:** SQLite con **SQLAlchemy** (ORM) para una gestión de datos robusta.
* **Seguridad:** Autenticación **OAuth2** con tokens **JWT** (JSON Web Tokens).
* **Encriptación:** Almacenamiento seguro de contraseñas mediante **Bcrypt**.
* **Validación:** Modelos de datos estrictos y tipado fuerte con **Pydantic**.

---

## 🔐 Jerarquía de Seguridad
El sistema protege la integridad de los datos mediante un flujo de autenticación. Las operaciones que modifican el inventario están restringidas al rol de administrador (Capitán).

| Nivel | Acción | Endpoint | Requiere Token |
| :--- | :--- | :--- | :--- |
| **Público** | Ver Inventario | \`GET /inventario\` | No |
| **Público** | Ver Reportes | \`GET /finanzas\` | No |
| **Público** | Registrar Usuario | \`POST /usuarios/registrar\` | No |
| **Público** | Login (Obtener Token) | \`POST /token\` | No |
| **Privado** | **Agregar Pieza** | \`POST /inventario\` | **SÍ** ✅ |
| **Privado** | **Editar Pieza** | \`PUT /inventario/{id}\` | **SÍ** ✅ |
| **Privado** | **Borrar Pieza** | \`DELETE /inventario/{id}\` | **SÍ** ✅ |

---

## 📦 Estructura del Proyecto
* \`api.py\`: Punto de entrada de la aplicación y definición de rutas (endpoints).
* \`models.py\`: Definición de las tablas de la base de datos (Piezas y Usuarios).
* \`schemas.py\`: Esquemas de Pydantic para validación de entrada y salida de datos.
* \`auth.py\`: Lógica de seguridad, hashing de passwords y gestión de JWT.
* \`database.py\`: Configuración del motor de base de datos y sesiones de SQLAlchemy.
* \`reportes.py\`: Módulo de lógica de negocio para cálculos automáticos de stock y estado.

---

## ⚓ Instalación y Uso Local

1. **Clonar el repositorio:**
   \`\`\`bash
   git clone https://github.com/afmontes-dev/Nauta_Inventario.git
   \`\`\`
2. **Activar el entorno virtual:**
   \`\`\`bash
   .\venv\Scripts\activate
   \`\`\`
3. **Instalar dependencias:**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`
4. **Ejecutar el servidor de desarrollo:**
   \`\`\`bash
   uvicorn api:app --reload
   \`\`\`

> **Nota de Seguridad:** El archivo de base de datos \`nauta_systems.db\` se encuentra excluido del repositorio via \`.gitignore\` para proteger los datos sensibles y hashes de usuarios. El sistema generará una base de datos limpia automáticamente al iniciar por primera vez.

---

## 👨‍🏫 Guía de Autenticación en Swagger (UI)
1. Accede a \`http://127.0.0.1:8000/docs\`.
2. Crea un usuario en la ruta \`/usuarios/registrar\`.
3. Haz clic en el botón superior derecho **"Authorize"**.
4. Ingresa tus credenciales para recibir tu token de acceso.
5. Las rutas de gestión de inventario quedarán desbloqueadas para su uso.

---

## 📝 Notas del Desarrollador
Esta versión v1.2 marca la transición de Nauta Systems hacia una aplicación escalable. Se ha priorizado la seguridad del lado del servidor (Backend) y la integridad referencial de los datos, preparando el ecosistema para la implementación de una interfaz de usuario (Frontend).
"@; git checkout -b docs/readme-v1.2; git add README.md; git commit -m "docs: actualizar readme a v1.2"; git checkout main; git merge docs/readme-v1.2; git push origin main; git branch -d docs/readme-v1.2