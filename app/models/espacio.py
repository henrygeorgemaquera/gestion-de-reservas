from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Espacio(Base):
    __tablename__ = "espacios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    ubicacion: Mapped[str] = mapped_column(String(200), nullable=False)
    capacidad: Mapped[int] = mapped_column(Integer, nullable=False)
    disponibilidad_total: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relación 1..N: Un espacio puede tener muchas reservas
    reservas = relationship("Reserva", back_populates="espacio", cascade="all, delete-orphan")