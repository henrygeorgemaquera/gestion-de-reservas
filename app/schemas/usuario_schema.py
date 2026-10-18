from pydantic import BaseModel, Field

# Plantilla base con los campos comunes
class UsuarioBase(BaseModel):
    nombre: str = Field(min_lenght=2, max_lenght=100)
    correo: str = Field(min_lenght=5, max_lenght=150)
    telefono: str | None = None

# Para el POST (crear)
class UsuarioCreate(UsuarioBase):
    pass

# Para el PUT (actualizar completo)
class UsuarioUpdate(UsuarioBase):
    pass

# Para la respuesta hacia el cliente 
class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
