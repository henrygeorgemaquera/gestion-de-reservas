from abc import ABC, abstractmethod
from datetime import date, time
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.reserva import Reserva

# SOLID
class IReservaRepository(ABC):
    @abstractmethod
    def get_all(
        self,
        skip: int = 0,
        limit: int = 10,
        usuario_id: int | None = None,
        espacio_id: int | None = None,
        fecha: date | None = None,
        estado: str | None = None
    ): pass

    @abstractmethod
    def get_by_id(self, id: int): pass

    @abstractmethod
    def buscar_conflicto_horario(
        self,
        espacio_id: int,
        fecha: date,
        hora_inicio: time,
        hora_fin: time,
        excluir_reserva_id: int | None = None
    ): pass

    @abstractmethod
    def create(self, reserva: Reserva): pass

    @abstractmethod
    def update(self, reserva: Reserva): pass

    @abstractmethod
    def delete(self, reserva: Reserva): pass


# La implementación
class ReservaRepository(IReservaRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        skip: int = 0,
        limit: int = 10,
        usuario_id: int | None = None,
        espacio_id: int | None = None,
        fecha: date | None = None,
        estado: str | None = None
    ):
        statement = select(Reserva)

        if usuario_id is not None:
            statement = statement.where(Reserva.usuario_id == usuario_id)
        if espacio_id is not None:
            statement = statement.where(Reserva.espacio_id == espacio_id)
        if fecha is not None:
            statement = statement.where(Reserva.fecha == fecha)
        if estado is not None:
            statement = statement.where(Reserva.estado == estado)

        statement = statement.offset(skip).limit(limit)
        return self.db.execute(statement).scalars().all()

    def get_by_id(self, id: int):
        return self.db.get(Reserva, id)

    def buscar_conflicto_horario(
        self,
        espacio_id: int,
        fecha: date,
        hora_inicio: time,
        hora_fin: time,
        excluir_reserva_id: int | None = None
    ):
        # Busca reservas con choque de horario
        statement = select(Reserva).where(
            Reserva.espacio_id == espacio_id,
            Reserva.fecha == fecha,
            Reserva.estado != "cancelada",
            Reserva.hora_inicio < hora_fin,
            Reserva.hora_fin > hora_inicio
        )

        # Si estamos editando una reserva existente no debe chocar consigo misma
        if excluir_reserva_id is not None:
            statement = statement.where(Reserva.id != excluir_reserva_id)

        return self.db.execute(statement).scalars().first()

    def create(self, reserva: Reserva):
        self.db.add(reserva)
        self.db.commit()
        self.db.refresh(reserva)
        return reserva

    def update(self, reserva: Reserva):
        self.db.commit()
        self.db.refresh(reserva)
        return reserva

    def delete(self, reserva: Reserva):
        self.db.delete(reserva)
        self.db.commit()