from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.usuario import Usuario

# (Principio SOLID: Inversión de Dependencias)
class IUsuarioRepository(ABC):
    @abstractmethod
    def get_all(self): pass
    
    @abstractmethod
    def get_by_id(self, id: int): pass
    
    @abstractmethod
    def create(self, usuario: Usuario): pass
    
    @abstractmethod
    def update(self, usuario: Usuario): pass
    
    @abstractmethod
    def delete(self, usuario: Usuario): pass

# La implementación
class UsuarioRepository(IUsuarioRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):

        return self.db.execute(select(Usuario)).scalars().all()

    def get_by_id(self, id: int):
        return self.db.get(Usuario, id)

    def create(self, usuario: Usuario):
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def update(self, usuario: Usuario):
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def delete(self, usuario: Usuario):
        self.db.delete(usuario)
        self.db.commit()