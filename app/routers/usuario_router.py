from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.usuario_schema import UsuarioResponse, UsuarioCreate, UsuarioUpdate
from app.repositories.usuario_repo import UsuarioRepository
from app.services.usuario_service import UsuarioService

# El prefijo y etiqueta para que se vea ordenado en Swagger UI
router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])

# Función inyectora que conecta Base, Repo y Service)
def get_usuario_service(db: Session = Depends(get_db)):
    repo = UsuarioRepository(db)
    return UsuarioService(repo)

# Los 5 Endpoints exigidos por la Cátedra
@router.get("", response_model=list[UsuarioResponse])
def listar_usuarios(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    service: UsuarioService = Depends(get_usuario_service)
):
    return service.obtener_todos(page=page, limit=limit)

@router.get("/{id}", response_model=UsuarioResponse)
def obtener_usuario(id: int, service: UsuarioService = Depends(get_usuario_service)):
    return service.obtener_por_id(id)

@router.post("", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(datos: UsuarioCreate, service: UsuarioService = Depends(get_usuario_service)):
    return service.crear(datos)

@router.put("/{id}", response_model=UsuarioResponse)
def actualizar_usuario(id: int, datos: UsuarioUpdate, service: UsuarioService = Depends(get_usuario_service)):
    return service.actualizar(id, datos)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def eliminar_usuario(id: int, service: UsuarioService = Depends(get_usuario_service)):
    return service.eliminar(id)