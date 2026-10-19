from datetime import date
from fastapi import HTTPException, status
from app.models.reserva import Reserva
from app.repositories.espacio_repo import IEspacioRepository
from app.repositories.reserva_repo import IReservaRepository
from app.repositories.usuario_repo import IUsuarioRepository
from app.schemas.reserva_schema import ReservaCreate, ReservaPatch

class ReservaService:
    def __init__(
        self,
        reserva_repo: IReservaRepository,
        usuario_repo: IUsuarioRepository,
        espacio_repo: IEspacioRepository
    ):
        self.reserva_repo = reserva_repo
        self.usuario_repo = usuario_repo
        self.espacio_repo = espacio_repo

    def obtener_todas(
        self,
        page: int = 1,
        limit: int = 10,
        usuario_id: int | None = None,
        espacio_id: int | None = None,
        fecha: date | None = None,
        estado: str | None = None
    ):
        skip = (page - 1) * limit
        return self.reserva_repo.get_all(
            skip=skip,
            limit=limit,
            usuario_id=usuario_id,
            espacio_id=espacio_id,
            fecha=fecha,
            estado=estado
        )

    def obtener_por_id(self, id: int):
        reserva = self.reserva_repo.get_by_id(id)
        if not reserva:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reserva inexistente"
            )
        return reserva

    def crear(self, datos: ReservaCreate):
        # Validar de que el usuario exista 
        usuario = self.usuario_repo.get_by_id(datos.usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario inexistente"
            )

        # Validar que el espacio exista y esté habilitado
        espacio = self.espacio_repo.get_by_id(datos.espacio_id)
        if not espacio:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Espacio inexistente"
            )
        if not espacio.disponibilidad_total:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El espacio seleccionado no se encuentra disponible para reservas"
            )

        # Validar horario coherente
        if datos.hora_inicio >= datos.hora_fin:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Horario no válido: la hora de inicio debe ser anterior a la hora de fin"
            )

        # Impedir horarios superpuestos
        conflicto = self.reserva_repo.buscar_conflicto_horario(
            espacio_id=datos.espacio_id,
            fecha=datos.fecha,
            hora_inicio=datos.hora_inicio,
            hora_fin=datos.hora_fin
        )
        if conflicto:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Reserva duplicada: el espacio ya está reservado entre {conflicto.hora_inicio} y {conflicto.hora_fin}"
            )

        nueva_reserva = Reserva(
            usuario_id=datos.usuario_id,
            espacio_id=datos.espacio_id,
            fecha=datos.fecha,
            hora_inicio=datos.hora_inicio,
            hora_fin=datos.hora_fin,
            estado=datos.estado
        )
        return self.reserva_repo.create(nueva_reserva)

    def actualizar_parcial(self, id: int, datos: ReservaPatch):
        # Actualizamos los atributos que el cliente envió en el JSON
        reserva = self.obtener_por_id(id)

        nueva_fecha = datos.fecha if datos.fecha is not None else reserva.fecha
        nueva_hora_inicio = datos.hora_inicio if datos.hora_inicio is not None else reserva.hora_inicio
        nueva_hora_fin = datos.hora_fin if datos.hora_fin is not None else reserva.hora_fin
        nuevo_estado = datos.estado if datos.estado is not None else reserva.estado

        # Validar que el nuevo horario sea coherente
        if nueva_hora_inicio >= nueva_hora_fin:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Horario no válido: la hora de inicio debe ser anterior a la hora de fin"
            )

        # Si la reserva sigue activa, verificamos que el nuevo horario no choque con otra reserva
        if nuevo_estado != "cancelada":
            conflicto = self.reserva_repo.buscar_conflicto_horario(
                espacio_id=reserva.espacio_id,
                fecha=nueva_fecha,
                hora_inicio=nueva_hora_inicio,
                hora_fin=nueva_hora_fin,
                excluir_reserva_id=reserva.id
            )
            if conflicto:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Reserva duplicada: el horario choca con otra reserva ({conflicto.hora_inicio} - {conflicto.hora_fin})"
                )

        reserva.fecha = nueva_fecha
        reserva.hora_inicio = nueva_hora_inicio
        reserva.hora_fin = nueva_hora_fin
        reserva.estado = nuevo_estado

        return self.reserva_repo.update(reserva)

    def eliminar(self, id: int):
        reserva = self.obtener_por_id(id)
        self.reserva_repo.delete(reserva)
        return {"mensaje": "Reserva eliminada correctamente"}