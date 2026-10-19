from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.espacio import Espacio

# SOLID
class IEspacioRepository(ABC):
    @abstractmethod
    def get_all(
        self,
        skip: int = 0,
        limit: int = 10,
        capacidad: int | None = None,
        disponible: bool | None = None,
    ): pass

    @abstractmethod
    def get_by_id(self, id: int): pass

    @abstractmethod
    def get_by_nombre(self, nombre: str): pass

    @abstractmethod
    def create(self, espacio: Espacio): pass

    @abstractmethod
    def update(self, espacio: Espacio): pass

    @abstractmethod
    def delete(self, espacio: Espacio): pass


# La implementación
class EspacioRepository(IEspacioRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(
        self,
        skip: int = 0,
        limit: int = 10,
        capacidad: int | None = None,
        disponible: bool | None = None,
    ):
        statement = select(Espacio)

        # Aplicamos filtros dinámicos solo si el usuario los envió en la URL
        if capacidad is not None:
            statement = statement.where(Espacio.capacidad >= capacidad)
        if disponible is not None:
            statement = statement.where(Espacio.disponibilidad_total == disponible)

        # Aplicamos paginación con .offset() y .limit()
        statement = statement.offset(skip).limit(limit)

        return self.db.execute(statement).scalars().all()

    def get_by_id(self, id: int):
        return self.db.get(Espacio, id)

    def get_by_nombre(self, nombre: str):
        statement = select(Espacio).where(Espacio.nombre == nombre)
        return self.db.execute(statement).scalars().first()

    def create(self, espacio: Espacio):
        self.db.add(espacio)
        self.db.commit()
        self.db.refresh(espacio)
        return espacio

    def update(self, espacio: Espacio):
        self.db.commit()
        self.db.refresh(espacio)
        return espacio

    def delete(self, espacio: Espacio):
        self.db.delete(espacio)
        self.db.commit()