from pydantic import BaseModel, Field

class EspacioBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    ubicacion: str = Field(min_length=2, max_length=200)
    capacidad: int = Field(gt=0, description="La capacidad debe ser mayor a 0")
    disponibilidad_total: bool = True

# Para un POST
class EspacioCreate(EspacioBase):
    pass

# Para un PUT
class EspacioUpdate(EspacioBase):
    pass

# Para la respuesta
class EspacioResponse(EspacioBase):
    id: int

    class Config:
        from_attributes = True