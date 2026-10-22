"""Carga datos de demostración de forma idempotente.

Ejecutar desde la carpeta src:
    python -m persistencia.crear_bd
    python -m persistencia.semilla_bd

El script usa los DAO existentes y consulta las tablas únicamente para
comprobar relaciones/duplicados que los DAO todavía no exponen.
"""
from datetime import date

from dominio.empleado import Empleado
from persistencia.conexion import abrir_conexion
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO


DEPARTAMENTOS = [
    "Administración",
    "Tecnología",
    "Sustentabilidad",
]

# Contraseñas solo para ambiente académico local. UsuarioDAO/Empleado
# almacena hash PBKDF2 a través del método existente de persistencia.
EMPLEADOS = [
    {
        "usuario": "semilla.ana",
        "contraseña": "EcoTechDemo2026!",
        "nombre": "Ana González",
        "correo": "ana.gonzalez.demo@ecotech.local",
        "direccion": "Oficina central",
        "telefono": "+56911111111",
        "salario": 950000,
        "rol": "Gerente",
        "departamento": "Administración",
    },
    {
        "usuario": "semilla.carlos",
        "contraseña": "EcoTechDemo2026!",
        "nombre": "Carlos Muñoz",
        "correo": "carlos.munoz.demo@ecotech.local",
        "direccion": "Santiago",
        "telefono": "+56922222222",
        "salario": 780000,
        "rol": "Empleado",
        "departamento": "Tecnología",
    },
    {
        "usuario": "semilla.valentina",
        "contraseña": "EcoTechDemo2026!",
        "nombre": "Valentina Rojas",
        "correo": "valentina.rojas.demo@ecotech.local",
        "direccion": "Santiago",
        "telefono": "+56933333333",
        "salario": 820000,
        "rol": "Gerente",
        "departamento": "Sustentabilidad",
    },
    {
        "usuario": "semilla.diego",
        "contraseña": "EcoTechDemo2026!",
        "nombre": "Diego Pérez",
        "correo": "diego.perez.demo@ecotech.local",
        "direccion": "Santiago",
        "telefono": "+56944444444",
        "salario": 690000,
        "rol": "Empleado",
        "departamento": "Tecnología",
    },
]

PROYECTOS = [
    {
        "nombre": "Plataforma de reciclaje inteligente",
        "descripcion": "Seguimiento de materiales reciclables y reportes.",
        "fecha_inicio": "2026-03-01",
        "fecha_fin": "2026-12-15",
    },
    {
        "nombre": "Optimización energética EcoTech",
        "descripcion": "Medición y mejora del consumo energético.",
        "fecha_inicio": "2026-04-01",
        "fecha_fin": "2026-11-30",
    },
]

REGISTROS = [
    ("semilla.carlos", "Plataforma de reciclaje inteligente",
     "2026-10-12", 4.0, "Implementación de módulo de seguimiento"),
    ("semilla.diego", "Plataforma de reciclaje inteligente",
     "2026-10-13", 3.5, "Pruebas de validación de datos"),
    ("semilla.valentina", "Optimización energética EcoTech",
     "2026-10-13", 2.0, "Revisión de indicadores energéticos"),
    ("semilla.ana", "Optimización energética EcoTech",
     "2026-10-14", 1.5, "Coordinación y revisión de avances"),
]


def _fila_a_dict(fila):
    return dict(fila)


def cargar_semilla():
    """Inserta únicamente registros que aún no existen."""
    conn = abrir_conexion()
    try:
        usuarios_existentes = {
            fila["username"] for fila in conn.execute(
                "SELECT username FROM usuario"
            ).fetchall()
        }
    finally:
        conn.close()

    departamentos_por_nombre = {
        fila["nombre"]: int(fila["id_depto"])
        for fila in DepartamentoDAO.listar()
    }
    for nombre in DEPARTAMENTOS:
        if nombre not in departamentos_por_nombre:
            DepartamentoDAO.insertar(nombre)

    departamentos_por_nombre = {
        fila["nombre"]: int(fila["id_depto"])
        for fila in DepartamentoDAO.listar()
    }

    # También se comprueban los correos para no intentar duplicar una
    # persona si ya existe con otro nombre de usuario.
    empleados_existentes = EmpleadoDAO.listar()
    usernames_existentes = {e.username for e in empleados_existentes}
    correos_existentes = {e.correo.casefold() for e in empleados_existentes}

    empleados_por_usuario = {
        e.username: e for e in empleados_existentes
    }

    empleados_creados = 0
    for datos in EMPLEADOS:
        if datos["username"] in usernames_existentes:
            empleados_por_usuario[datos["username"]] = next(
                e for e in empleados_existentes
                if e.username == datos["username"]
            )
            continue

        if datos["correo"].casefold() in correos_existentes:
            print(
                "AVISO: se omitió el empleado "
                f"{datos['username']} porque el correo ya existe."
            )
            continue

        empleado = Empleado(
            username=datos["username"],
            password=datos["password"],
            nombre=datos["nombre"],
            correo=datos["correo"],
            direccion=datos["direccion"],
            telefono=datos["telefono"],
            salario=datos["salario"],
            rol=datos["rol"],
            departamento_id=departamentos_por_nombre[datos["departamento"]],
        )
        EmpleadoDAO.insertar(empleado)
        empleados_por_usuario[empleado.username] = empleado
        usernames_existentes.add(empleado.username)
        correos_existentes.add(empleado.correo.casefold())
        empleados_creados += 1

    proyectos_por_nombre = {
        fila["nombre"]: int(fila["id_proyecto"])
        for fila in ProyectoDAO.listar()
    }
    proyectos_creados = 0
    for datos in PROYECTOS:
        if datos["nombre"] not in proyectos_por_nombre:
            ident = ProyectoDAO.insertar(
                datos["nombre"], datos["descripcion"],
                datos["fecha_inicio"], datos["fecha_fin"]
            )
            proyectos_por_nombre[datos["nombre"]] = ident
            proyectos_creados += 1

    # Relación proyecto-empleado: se comprueba antes de insertar para
    # que ejecutar la semilla otra vez no choque con la clave primaria.
    conn = abrir_conexion()
    try:
        relaciones = {
            (int(f["proyecto_id"]), int(f["empleado_id"]))
            for f in conn.execute(
                "SELECT proyecto_id, empleado_id FROM proyecto_empleado"
            ).fetchall()
        }
    finally:
        conn.close()

    relaciones_creadas = 0
    asignaciones = [
        ("Plataforma de reciclaje inteligente", "semilla.carlos"),
        ("Plataforma de reciclaje inteligente", "semilla.diego"),
        ("Optimización energética EcoTech", "semilla.valentina"),
        ("Optimización energética EcoTech", "semilla.ana"),
    ]
    for nombre_proyecto, username in asignaciones:
        empleado = empleados_por_usuario.get(username)
        proyecto_id = proyectos_por_nombre.get(nombre_proyecto)
        if empleado is None or empleado.id_empleado is None or proyecto_id is None:
            print(f"AVISO: no se pudo asignar {username} a {nombre_proyecto}.")
            continue
        relacion = (proyecto_id, int(empleado.id_empleado))
        if relacion not in relaciones:
            ProyectoDAO.asignar_empleado(*relacion)
            relaciones.add(relacion)
            relaciones_creadas += 1

    registros_existentes = RegistroTiempoDAO.listar()
    claves_registros = {
        (
            int(r["empleado_id"]), int(r["proyecto_id"]),
            str(r["fecha"]), float(r["horas_trabajadas"]),
            str(r["descripcion_tarea"])
        )
        for r in registros_existentes
    }

    registros_creados = 0
    for username, nombre_proyecto, fecha, horas, descripcion in REGISTROS:
        empleado = empleados_por_usuario.get(username)
        proyecto_id = proyectos_por_nombre.get(nombre_proyecto)
        if empleado is None or empleado.id_empleado is None or proyecto_id is None:
            print(
                "AVISO: se omitió un registro de tiempo por falta de "
                "empleado o proyecto válido."
            )
            continue

        clave = (
            int(empleado.id_empleado), int(proyecto_id),
            fecha, float(horas), descripcion
        )
        if clave in claves_registros:
            continue

        RegistroTiempoDAO.insertar(
            int(empleado.id_empleado), int(proyecto_id),
            fecha, horas, descripcion
        )
        claves_registros.add(clave)
        registros_creados += 1

    # Resumen con cantidades totales reales de la base.
    conn = abrir_conexion()
    try:
        conteos = {}
        for tabla in (
            "departamento", "usuario", "empleado",
            "proyecto", "proyecto_empleado", "registro_tiempo"
        ):
            conteos[tabla] = conn.execute(
                f"SELECT COUNT(*) AS total FROM {tabla}"
            ).fetchone()["total"]
    finally:
        conn.close()

    print("\nSemilla finalizada.")
    print(f"Departamentos totales: {conteos['departamento']}")
    print(f"Usuarios totales: {conteos['usuario']}")
    print(f"Empleados totales: {conteos['empleado']}")
    print(f"Proyectos totales: {conteos['proyecto']}")
    print(f"Asignaciones proyecto-empleado: {conteos['proyecto_empleado']}")
    print(f"Registros de tiempo totales: {conteos['registro_tiempo']}")
    print("\nInsertados en esta ejecución:")
    print(f"  Empleados: {empleados_creados}")
    print(f"  Proyectos: {proyectos_creados}")
    print(f"  Asignaciones: {relaciones_creadas}")
    print(f"  Registros de tiempo: {registros_creados}")


if __name__ == "__main__":
    cargar_semilla()
