from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    correo: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    # Nueva columna para la segunda migración de ALEMBIC
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # Relación 1..N: Un usuario puede tener 1 o más reservas
    reservas = relationship("Reserva", back_populates="usuario", cascade="all, delete-orphan")

