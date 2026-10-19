from fastapi import FastAPI
from app.routers import usuario_router, espacio_router, reserva_router
from app.middleware.process_time import ProcessTimeMiddleware

app = FastAPI(
    title="Plataforma de Reserva de Espacios",
    description="Backend API para la gestión de reservas y espacios físicos.",
    version="1.0.0"
)

# Registramos el Middleware de tiempos de respuesta
app.add_middleware(ProcessTimeMiddleware)

# Registramos el router de usuarios
app.include_router(usuario_router.router)
app.include_router(espacio_router.router)
app.include_router(reserva_router.router)