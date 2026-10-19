from datetime import date
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.espacio_repo import EspacioRepository
from app.repositories.reserva_repo import ReservaRepository
from app.repositories.usuario_repo import UsuarioRepository
from app.schemas.reserva_schema import ReservaCreate, ReservaPatch, ReservaResponse
from app.services.reserva_service import ReservaService

router = APIRouter(prefix="/api/reservas", tags=["Reservas"])

def get_reserva_service(db: Session = Depends(get_db)):
    reserva_repo = ReservaRepository(db)
    usuario_repo = UsuarioRepository(db)
    espacio_repo = EspacioRepository(db)
    return ReservaService(reserva_repo, usuario_repo, espacio_repo)

@router.get("", response_model=list[ReservaResponse])
def listar_reservas(
    page: int = Query(default=1, ge=1, description="Número de página"),
    limit: int = Query(default=10, ge=1, le=100, description="Elementos por página"),
    usuario_id: int | None = Query(default=None, description="Filtrar por ID de usuario"),
    espacio_id: int | None = Query(default=None, description="Filtrar por ID de espacio"),
    fecha: date | None = Query(default=None, description="Filtrar por fecha (YYYY-MM-DD)"),
    estado: str | None = Query(default=None, description="Filtrar por estado (confirmada, pendiente, cancelada)"),
    service: ReservaService = Depends(get_reserva_service)
):
    return service.obtener_todas(
        page=page,
        limit=limit,
        usuario_id=usuario_id,
        espacio_id=espacio_id,
        fecha=fecha,
        estado=estado
    )

@router.get("/{id}", response_model=ReservaResponse)
def obtener_reserva(id: int, service: ReservaService = Depends(get_reserva_service)):
    return service.obtener_por_id(id)

@router.post("", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
def crear_reserva(datos: ReservaCreate, service: ReservaService = Depends(get_reserva_service)):
    return service.crear(datos)

@router.patch("/{id}", response_model=ReservaResponse)
def actualizar_reserva_parcial(id: int, datos: ReservaPatch, service: ReservaService = Depends(get_reserva_service)):
    return service.actualizar_parcial(id, datos)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def eliminar_reserva(id: int, service: ReservaService = Depends(get_reserva_service)):
    return service.eliminar(id)