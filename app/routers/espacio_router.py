from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.espacio_repo import EspacioRepository
from app.schemas.espacio_schema import EspacioCreate, EspacioResponse, EspacioUpdate
from app.services.espacio_service import EspacioService

router = APIRouter(prefix="/api/espacios", tags=["Espacios"])

def get_espacio_service(db: Session = Depends(get_db)):
    repo = EspacioRepository(db)
    return EspacioService(repo)

@router.get("", response_model=list[EspacioResponse])
def listar_espacios(
    page: int = Query(default=1, ge=1, description="Número de página"),
    limit: int = Query(default=10, ge=1, le=100, description="Cantidad de elementos por página"),
    capacidad: int | None = Query(default=None, gt=0, description="Capacidad mínima requerida"),
    disponible: bool | None = Query(default=None, description="Filtrar por disponibilidad total (true/false)"),
    service: EspacioService = Depends(get_espacio_service)
):
    return service.obtener_todos(
        page=page,
        limit=limit,
        capacidad=capacidad,
        disponible=disponible,
    )

@router.get("/{id}", response_model=EspacioResponse)
def obtener_espacio(id: int, service: EspacioService = Depends(get_espacio_service)):
    return service.obtener_por_id(id)

@router.post("", response_model=EspacioResponse, status_code=status.HTTP_201_CREATED)
def crear_espacio(datos: EspacioCreate, service: EspacioService = Depends(get_espacio_service)):
    return service.crear(datos)

@router.put("/{id}", response_model=EspacioResponse)
def actualizar_espacio(id: int, datos: EspacioUpdate, service: EspacioService = Depends(get_espacio_service)):
    return service.actualizar(id, datos)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def eliminar_espacio(id: int, service: EspacioService = Depends(get_espacio_service)):
    return service.eliminar(id)