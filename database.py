from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Definimos dónde vivirá la base de datos (un archivo .db)
SQLALCHEMY_DATABASE_URL = "sqlite:///./nauta_systems.db"

# 2. Creamos el motor (engine)
# check_same_thread es solo para SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Creamos la fábrica de sesiones (para hacer consultas)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Clase base para nuestros modelos
Base = declarative_base()

# Función para obtener la base de datos en las rutas de FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()