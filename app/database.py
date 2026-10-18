from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Ruta donde se guarda el archivo físico de SQLite
DATABASE_URL = "sqlite:///./reservas.db"

# Motor de conexión
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Fábrica de sesiones
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# Libro de registro
class Base(DeclarativeBase):
    pass

# Inyección de dependencias
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()