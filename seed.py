from datetime import date, time
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Usuario, Espacio, Reserva

def cargar_datos_iniciales():
    # Abrimos una sesión con SessionLocal
    db = SessionLocal()

    try:
        # Verificamos si ya hay usuarios cargados para no duplicar datos ni romper los campos únicos
        usuario_existente = db.execute(select(Usuario)).scalars().first()
        if usuario_existente:
            print("Los datos iniciales ya fueron cargados anteriormente. No se realizaron cambios.")
            return

        print("Sembrando datos iniciales en la base de datos...")

        # Creación de 5 usuarios
        usuarios = [
            Usuario(nombre="Ana Gómez", correo="ana.gomez@ucn.cl", telefono="+56911111111"),
            Usuario(nombre="Carlos Pérez", correo="carlos.perez@ucn.cl", telefono="+56922222222"),
            Usuario(nombre="Beatriz Silva", correo="beatriz.silva@ucn.cl", telefono="+56933333333"),
            Usuario(nombre="Diego Morales", correo="diego.morales@ucn.cl", telefono="+56944444444"),
            Usuario(nombre="Elena Torres", correo="elena.torres@ucn.cl", telefono="+56955555555"),
        ]
        db.add_all(usuarios)
        db.commit()  # Guardamos para que SQLite les asigne sus IDs

        # Creación de 10 espacios
        espacios = [
            Espacio(nombre="Sala de Estudio A1", ubicacion="Biblioteca Piso 1", capacidad=6, disponibilidad_total=True),
            Espacio(nombre="Sala de Estudio A2", ubicacion="Biblioteca Piso 1", capacidad=8, disponibilidad_total=True),
            Espacio(nombre="Laboratorio de Redes", ubicacion="Pabellón R Piso 2", capacidad=30, disponibilidad_total=True),
            Espacio(nombre="Laboratorio de Software", ubicacion="Pabellón R Piso 1", capacidad=40, disponibilidad_total=True),
            Espacio(nombre="Auditorio Principal", ubicacion="Edificio Central", capacidad=120, disponibilidad_total=True),
            Espacio(nombre="Sala de Conferencias B", ubicacion="Decanato Piso 2", capacidad=20, disponibilidad_total=True),
            Espacio(nombre="Sala Multimedia", ubicacion="Pabellón K Piso 3", capacidad=25, disponibilidad_total=False),
            Espacio(nombre="Box de Reunión 1", ubicacion="Cowork Ingeniería", capacidad=4, disponibilidad_total=True),
            Espacio(nombre="Box de Reunión 2", ubicacion="Cowork Ingeniería", capacidad=4, disponibilidad_total=False),
            Espacio(nombre="Cancha Multiuso", ubicacion="Sector Deportes", capacidad=50, disponibilidad_total=True),
        ]
        db.add_all(espacios)
        db.commit()  # Guardamos para que SQLite les asigne sus IDs

        # Creación de 15 reservas
        reservas = [
            Reserva(usuario_id=1, espacio_id=1, fecha=date(2026, 10, 20), hora_inicio=time(9, 0), hora_fin=time(11, 0), estado="confirmada"),
            Reserva(usuario_id=2, espacio_id=1, fecha=date(2026, 10, 20), hora_inicio=time(11, 0), hora_fin=time(13, 0), estado="confirmada"),
            Reserva(usuario_id=3, espacio_id=2, fecha=date(2026, 10, 20), hora_inicio=time(10, 0), hora_fin=time(12, 0), estado="confirmada"),
            Reserva(usuario_id=4, espacio_id=3, fecha=date(2026, 10, 21), hora_inicio=time(8, 30), hora_fin=time(10, 30), estado="confirmada"),
            Reserva(usuario_id=5, espacio_id=3, fecha=date(2026, 10, 21), hora_inicio=time(14, 0), hora_fin=time(16, 0), estado="pendiente"),
            Reserva(usuario_id=1, espacio_id=4, fecha=date(2026, 10, 21), hora_inicio=time(10, 0), hora_fin=time(12, 0), estado="confirmada"),
            Reserva(usuario_id=2, espacio_id=5, fecha=date(2026, 10, 22), hora_inicio=time(9, 0), hora_fin=time(13, 0), estado="confirmada"),
            Reserva(usuario_id=3, espacio_id=6, fecha=date(2026, 10, 22), hora_inicio=time(15, 0), hora_fin=time(17, 0), estado="cancelada"),
            Reserva(usuario_id=4, espacio_id=8, fecha=date(2026, 10, 23), hora_inicio=time(9, 0), hora_fin=time(10, 0), estado="confirmada"),
            Reserva(usuario_id=5, espacio_id=8, fecha=date(2026, 10, 23), hora_inicio=time(10, 30), hora_fin=time(12, 0), estado="confirmada"),
            Reserva(usuario_id=1, espacio_id=10, fecha=date(2026, 10, 24), hora_inicio=time(16, 0), hora_fin=time(18, 0), estado="confirmada"),
            Reserva(usuario_id=2, espacio_id=10, fecha=date(2026, 10, 24), hora_inicio=time(18, 0), hora_fin=time(20, 0), estado="pendiente"),
            Reserva(usuario_id=3, espacio_id=4, fecha=date(2026, 10, 25), hora_inicio=time(8, 0), hora_fin=time(10, 0), estado="confirmada"),
            Reserva(usuario_id=4, espacio_id=6, fecha=date(2026, 10, 25), hora_inicio=time(11, 0), hora_fin=time(13, 0), estado="confirmada"),
            Reserva(usuario_id=5, espacio_id=2, fecha=date(2026, 10, 26), hora_inicio=time(14, 0), hora_fin=time(16, 0), estado="cancelada"),
        ]
        db.add_all(reservas)
        db.commit()

        print("¡Seeder ejecutado con éxito! Se insertaron 5 usuarios, 10 espacios y 15 reservas.")

    except Exception as e:
        # Si algo falla, revertimos todo con rollback() para no dejar datos corruptos
        db.rollback()
        print(f" Error al cargar los datos iniciales: {e}")
    finally:
        # cerramos la sesión 
        db.close()

if __name__ == "__main__":
    cargar_datos_iniciales()