import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Activamos el cronómetro antes de que la petición entre al servidor
        start_time = time.perf_counter()
        
        # Dejamos que la petición continúe su camino hacia los Routers/Endpoints
        response = await call_next(request)
        
        # Detenemos el cronómetro
        process_time = time.perf_counter() - start_time
        
        # Inyectamos una cabecera personalizada con el tiempo medido en segundos
        response.headers["X-Process-Time"] = str(process_time)
        
        return response