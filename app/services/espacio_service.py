from fastapi import HTTPException, status
from app.models.espacio import Espacio
from app.repositories.espacio_repo import IEspacioRepository
from app.schemas.espacio_schema import EspacioCreate, EspacioUpdate

class EspacioService:
    def __init__(self, repo: IEspacioRepository):
        self.repo = repo

    def obtener_todos(
        self,
        page: int = 1,
        limit: int = 10,
        capacidad: int | None = None,
        disponible: bool | None = None,
    ):
        # Convertimos el número de página en cuántos registros saltar
        skip = (page - 1) * limit
        return self.repo.get_all(
            skip=skip,
            limit=limit,
            capacidad=capacidad,
            disponible=disponible,
        )

    def obtener_por_id(self, id: int):
        espacio = self.repo.get_by_id(id)
        if not espacio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Espacio inexistente"
            )
        return espacio

    def crear(self, datos: EspacioCreate):
        # Validamos que no exista otro espacio con el mismo nombre
        existente = self.repo.get_by_nombre(datos.nombre)
        if existente:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Ya existe un espacio registrado con ese nombre"
            )

        nuevo_espacio = Espacio(
            nombre=datos.nombre,
            capacidad=datos.capacidad,
            disponibilidad_total=datos.disponibilidad_total
        )
        return self.repo.create(nuevo_espacio)

    def actualizar(self, id: int, datos: EspacioUpdate):
        espacio = self.obtener_por_id(id)

        # Si le está cambiando el nombre, verificamos que el nuevo nombre no esté ocupado por otro espacio
        if datos.nombre != espacio.nombre:
            existente = self.repo.get_by_nombre(datos.nombre)
            if existente:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Ya existe otro espacio con ese nombre"
                )

        espacio.nombre = datos.nombre
        espacio.capacidad = datos.capacidad
        espacio.disponibilidad_total = datos.disponibilidad_total

        return self.repo.update(espacio)

    def eliminar(self, id: int):
        espacio = self.obtener_por_id(id)
        self.repo.delete(espacio)
        return {"mensaje": "Espacio eliminado correctamente"}