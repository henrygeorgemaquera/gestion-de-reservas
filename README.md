# Plataforma de Gestión y Reserva de Espacios - Backend API

API REST desarrollada con **FastAPI** para administrar espacios físicos y organizar el proceso de reservas de una institución, reemplazando el uso de planillas y correos electrónicos.

---

## Descripción del Problema
Actualmente, hacer las reservas de forma manual por mensajes o planillas genera varios problemas:
- Reservas duplicadas en un mismo horario y salón.
- Dificultad para saber si un espacio está realmente disponible.
- Información desactualizada.
- No saber con claridad quién pidió cada reserva ni tener un historial centralizado.

Este proyecto soluciona esto mediante un backend estructurado por capas que valida los datos de entrada y evita choques de horario antes de guardar una reserva en la base de datos.

---

## Instalación de Dependencias
Se recomienda tener **Python 3.10 o superior**. Para preparar el proyecto desde cero en tu computadora, abre la terminal en la carpeta raíz y ejecuta:

```bash
# 1. Crear el entorno virtual
python -m venv venv

# 2. Activar el entorno virtual
# En Windows (PowerShell):
.\venv\Scripts\Activate
# En Mac / Linux:
source venv/bin/activate

# 3. Instalar las librerías del proyecto desde requirements.txt
pip install -r requirements.txt
```
*(También se pueden instalar directamente con: `pip install "fastapi[standard]" uvicorn sqlalchemy alembic`)*.

---

## Base de Datos y Migraciones (Alembic)
La base de datos utiliza **SQLite** (`reservas.db`) y su estructura se maneja con **Alembic** para no tener que borrar la base de datos al hacer cambios en los modelos.

El proyecto incluye dos migraciones en la carpeta `alembic/versions/`:
1. **Migración inicial:** Crea las tablas `usuarios`, `espacios` y `reservas`.
2. **Segunda migración:** Modifica el modelo `Usuario` para agregar la columna opcional `telefono`.

Para aplicar las migraciones y crear las tablas físicas, ejecuta:

```bash
alembic upgrade head
```

---

## Datos Iniciales (Seeder)
Se creó el script `seed.py`. Este archivo carga **5 usuarios, 10 espacios y 15 reservas** iniciales. Si se ejecuta más de una vez, verifica si ya existen datos para no duplicarlos.

Para cargar los datos, ejecuta:

```bash
python seed.py
```

---

## Ejecución del Proyecto
Con el entorno virtual activado, inicia el servidor local ejecutando:

```bash
uvicorn app.main:app --reload
```

Una vez encendido el servidor, puedes ver y probar la documentación automática que genera FastAPI en el navegador:
- **Swagger UI (para probar los endpoints):** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

---

## Arquitectura del Proyecto
El código está dentro de la carpeta `app/` separado por responsabilidades para no mezclar las rutas web con las consultas a la base de datos:

- **Database (`app/database.py`):** Configura la conexión a SQLite (`engine`), la sesión (`SessionLocal`), la clase `Base` para los modelos y la función `get_db()`.
- **Models (`app/models/`):** Clases de SQLAlchemy (`Usuario`, `Espacio`, `Reserva`) que representan las tablas reales en la base de datos y sus relaciones (`ForeignKey` y `relationship`).
- **DTO / Schemas (`app/schemas/`):** Modelos de Pydantic (`BaseModel`) que validan el JSON que envía el usuario y dan formato a las respuestas. Así evitamos devolver directamente el modelo de SQLAlchemy.
- **Repository (`app/repositories/`):** Es la única capa que hace consultas con SQLAlchemy (`select`, `add`, `commit`, `delete`).
- **Service (`app/services/`):** Contiene la lógica de negocio y validaciones. Aquí se programó la regla principal que revisa que dos reservas en el mismo espacio y fecha no tengan horarios que se superpongan, además de lanzar los códigos de errores cuando correspondan.
- **Router / Endpoints (`app/routers/`):** Define las rutas HTTP, recibe los Query Params de filtros/paginación y llama al Service correspondiente.
- **Dependencies:** Se usa `Depends()` de FastAPI tanto para inyectar la sesión de base de datos (`get_db` usando `try / yield / finally` para cerrar siempre la conexión) como para pasar los repositorios a los servicios.
- **Middleware (`app/middlewares/process_time.py`):** Implementa un middleware que mide cuánto tarda cada petición en procesarse y agrega ese valor en la cabecera `X-Process-Time` de la respuesta.

### Principios SOLID aplicados
1. **Single Responsibility Principle (SRP):** Aplicado en la separación en carpetas (`routers`, `services`, `repositories`, `schemas`). Por ejemplo, `reserva_router.py` solo recibe peticiones HTTP, `reserva_service.py` solo valida reglas de horarios y `reserva_repo.py` solo hace consultas en la base de datos.
2. **Dependency Inversion Principle (DIP):** Aplicado entre los Services y Repositories. En `usuario_repo.py`, `espacio_repo.py` y `reserva_repo.py` se crearon interfaces abstractas con `ABC` (`IUsuarioRepository`, `IEspacioRepository`, `IReservaRepository`). Los servicios reciben estas interfaces en su `__init__` en lugar de instanciar directamente la clase de SQLAlchemy.
3. **Open/Closed Principle (OCP):** Gracias a las clases abstractas `ABC` en los repositorios, si en el futuro se quisiera cambiar la forma de guardar datos o crear un repositorio de prueba, se puede crear una nueva clase que herede de la interfaz sin tener que modificar el código de los `Services`.

### Uso de Métodos HTTP (Diferencia entre PUT y PATCH)
- **PUT (`/api/usuarios/{id}` y `/api/espacios/{id}`):** Se utiliza para reemplazar el recurso completo, por lo que el esquema de entrada exige enviar todos los campos principales del objeto.
- **PATCH (`/api/reservas/{id}`):** Se utiliza para hacer una actualización parcial. En `ReservaPatch` todos los atributos son opcionales (`None`), lo que permite modificar solo el `estado` (por ejemplo, cambiarlo a `"cancelada"`) o cambiar solo la hora sin tener que enviar toda la reserva otra vez.

---

## Tabla de Endpoints

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| **GET** | `/api/usuarios` | Lista los usuarios registrados (con paginación `page` y `limit`). |
| **GET** | `/api/usuarios/{id}` | Obtiene un usuario específico por su ID. |
| **POST** | `/api/usuarios` | Crea un nuevo usuario. |
| **PUT** | `/api/usuarios/{id}` | Actualiza todos los datos de un usuario existente. |
| **DELETE** | `/api/usuarios/{id}` | Elimina un usuario por su ID. |
| **GET** | `/api/espacios` | Lista los espacios con paginación y filtros opcionales (`capacidad` mínima y `disponible`). |
| **GET** | `/api/espacios/{id}` | Obtiene un espacio específico por su ID. |
| **POST** | `/api/espacios` | Crea un nuevo espacio físico. |
| **PUT** | `/api/espacios/{id}` | Actualiza todos los datos de un espacio existente. |
| **DELETE** | `/api/espacios/{id}` | Elimina un espacio por su ID. |
| **GET** | `/api/reservas` | Lista las reservas con paginación y filtros opcionales (`usuario_id`, `espacio_id`, `fecha`, `estado`). |
| **GET** | `/api/reservas/{id}` | Obtiene una reserva específica por su ID. |
| **POST** | `/api/reservas` | Crea una reserva validando que existan el usuario/espacio y que el horario no se superponga. |
| **PATCH** | `/api/reservas/{id}` | Actualiza parcialmente una reserva (ej. cambiar estado a cancelada o cambiar horario). |
| **DELETE** | `/api/reservas/{id}` | Elimina una reserva por su ID. |