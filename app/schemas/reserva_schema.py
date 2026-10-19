from datetime import date, time
from pydantic import BaseModel, Field

class ReservaBase(BaseModel):
    usuario_id: int = Field(gt=0)
    espacio_id: int = Field(gt=0)
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado: str = Field(default="confirmada", min_length=3, max_length=50)

# Para el POST
class ReservaCreate(ReservaBase):
    pass

# Para el patch
class ReservaPatch(BaseModel):
    fecha: date | None = None
    hora_inicio: time | None = None
    hora_fin: time | None = None
    estado: str | None = Field(default=None, min_length=3, max_length=50)

# Para la salida
class ReservaResponse(ReservaBase):
    id: int

    class Config:
        from_attributes = True