from fastapi import HTTPException, status
from app.repositories.usuario_repo import IUsuarioRepository
from app.models.usuario import Usuario
from app.schemas.usuario_schema import UsuarioCreate, UsuarioUpdate

class UsuarioService:
    # Recibe el repositorio por el constructor (Inyección de Dependencias)
    def __init__(self, repo: IUsuarioRepository):
        self.repo = repo

    def obtener_todos(self, page: int = 1, limit: int = 10):
        skip = (page - 1) * limit
        return self.repo.get_all(skip=skip, limit=limit)

    def obtener_por_id(self, id: int):
        usuario = self.repo.get_by_id(id)
        if not usuario:
            # Si el repo dice que no existe, lanzamos 404
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario inexistente")
        return usuario

    def crear(self, datos: UsuarioCreate):
        nuevo_usuario = Usuario(
            nombre=datos.nombre,
            correo=datos.correo,
            telefono=datos.telefono
        )
        return self.repo.create(nuevo_usuario)

    def actualizar(self, id: int, datos: UsuarioUpdate):
        # Buscamos al usuario (si no existe, la función de obtener por id lanzará el error)
        usuario = self.obtener_por_id(id)
        
        # Al ser PUT, sobreescribimos todos los datos
        usuario.nombre = datos.nombre
        usuario.correo = datos.correo
        usuario.telefono = datos.telefono
        
        return self.repo.update(usuario)

    def eliminar(self, id: int):
        usuario = self.obtener_por_id(id)
        self.repo.delete(usuario)
        return {"mensaje": "Usuario eliminado correctamente"}