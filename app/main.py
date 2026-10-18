from fastapi import FastAPI
from app.routers import usuario_router

app = FastAPI(
    title="Plataforma de Reserva de Espacios",
    description="Backend API para la gestión de reservas y espacios físicos.",
    version="1.0.0"
)

# Registramos el router de usuarios
app.include_router(usuario_router.router)