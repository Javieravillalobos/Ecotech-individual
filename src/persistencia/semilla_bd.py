"""Carga datos de demostración de forma idempotente.

Ejecutar desde la carpeta src:
    python -m persistencia.crear_bd
    python -m persistencia.semilla_bd
"""
from persistencia.conexion import abrir_conexion
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.usuario_dao import UsuarioDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from dominio.empleado import Empleado
from dominio.usuario import Usuario


DEPARTAMENTOS = [
    "Administración",
    "Tecnología",
    "Sustentabilidad",
]

# Definición de empleados y sus credenciales de usuario correspondientes
EMPLEADOS_Y_USUARIOS = [
    {
        "nombre": "Ana González",
        "correo": "ana.gonzalez.demo@ecotech.local",
        "direccion": "Oficina central",
        "telefono": "+56911111111",
        "salario": 950000,
        "departamento": "Administración",
        "es_gerente": True,
        "usuario": "semilla.ana",
        "contraseña": "EcoTechDemo2026!",
        "rol": "admin",
    },
    {
        "nombre": "Carlos Muñoz",
        "correo": "carlos.munoz.demo@ecotech.local",
        "direccion": "Santiago",
        "telefono": "+56922222222",
        "salario": 780000,
        "departamento": "Tecnología",
        "es_gerente": False,
        "usuario": "semilla.carlos",
        "contraseña": "EcoTechDemo2026!",
        "rol": "empleado",
    },
    {
        "nombre": "Valentina Rojas",
        "correo": "valentina.rojas.demo@ecotech.local",
        "direccion": "Santiago",
        "telefono": "+56933333333",
        "salario": 820000,
        "departamento": "Sustentabilidad",
        "es_gerente": True,
        "usuario": "semilla.valentina",
        "contraseña": "EcoTechDemo2026!",
        "rol": "empleado",
    },
    {
        "nombre": "Diego Pérez",
        "correo": "diego.perez.demo@ecotech.local",
        "direccion": "Santiago",
        "telefono": "+56944444444",
        "salario": 690000,
        "departamento": "Tecnología",
        "es_gerente": False,
        "usuario": "semilla.diego",
        "contraseña": "EcoTechDemo2026!",
        "rol": "empleado",
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
    ("semilla.carlos", "Plataforma de reciclaje inteligente", "2026-10-12", 4.0, "Implementación de módulo de seguimiento"),
    ("semilla.diego", "Plataforma de reciclaje inteligente", "2026-10-13", 3.5, "Pruebas de validación de datos"),
    ("semilla.valentina", "Optimización energética EcoTech", "2026-10-13", 2.0, "Revisión de indicadores energéticos"),
    ("semilla.ana", "Optimización energética EcoTech", "2026-10-14", 1.5, "Coordinación y revisión de avances"),
]


def cargar_semilla():
    """Inserta datos iniciales garantizando la integridad referencial."""
    
    # 1. Departamentos
    deptos_existentes = {f["nombre"]: int(f["id_depto"]) for f in DepartamentoDAO.listar()}
    for nombre in DEPARTAMENTOS:
        if nombre not in deptos_existentes:
            id_depto = DepartamentoDAO.insertar(nombre)
            deptos_existentes[nombre] = id_depto

    # 2. Empleados y Usuarios
    empleados_existentes = EmpleadoDAO.listar()
    correos_existentes = {e.correo.casefold(): e for e in empleados_existentes}
    
    empleados_creados = 0
    usuarios_creados = 0
    empleados_por_usuario = {}

    for datos in EMPLEADOS_Y_USUARIOS:
        correo_key = datos["correo"].casefold()
        
        # Insertar o recuperar Empleado
        if correo_key in correos_existentes:
            empleado = correos_existentes[correo_key]
        else:
            empleado = Empleado(
                nombre=datos["nombre"],
                correo=datos["correo"],
                direccion=datos["direccion"],
                telefono=datos["telefono"],
                salario=datos["salario"],
                departamento_id=deptos_existentes[datos["departamento"]],
            )
            EmpleadoDAO.insertar(empleado)
            correos_existentes[correo_key] = empleado
            empleados_creados += 1

        empleados_por_usuario[datos["usuario"]] = empleado

        # Asignar Gerente al Departamento si corresponde
        if datos.get("es_gerente"):
            DepartamentoDAO.asignar_gerente(
                id_depto=deptos_existentes[datos["departamento"]],
                gerente_id=empleado.id_empleado
            )

        # Insertar Usuario asociado si no existe
        usuario_existente = UsuarioDAO.obtener_por_username(datos["usuario"])
        if not usuario_existente:
            nuevo_usuario = Usuario(
                username=datos["usuario"],
                password=datos["contraseña"],
                empleado_id=empleado.id_empleado,
                rol=datos["rol"],
            )
            UsuarioDAO.insertar(nuevo_usuario)
            usuarios_creados += 1

    # 3. Proyectos
    proyectos_existentes = {f["nombre"]: int(f["id_proyecto"]) for f in ProyectoDAO.listar()}
    proyectos_creados = 0

    for datos in PROYECTOS:
        if datos["nombre"] not in proyectos_existentes:
            p_id = ProyectoDAO.insertar(
                datos["nombre"], datos["descripcion"],
                datos["fecha_inicio"], datos["fecha_fin"]
            )
            proyectos_existentes[datos["nombre"]] = p_id
            proyectos_creados += 1

    # 4. Asignaciones Proyecto - Empleado
    conn = abrir_conexion()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT proyecto_id, empleado_id FROM proyecto_empleado")
            relaciones = {(int(f["proyecto_id"]), int(f["empleado_id"])) for f in cursor.fetchall()}
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
        emp = empleados_por_usuario.get(username)
        p_id = proyectos_existentes.get(nombre_proyecto)
        if emp and emp.id_empleado and p_id:
            pair = (p_id, int(emp.id_empleado))
            if pair not in relaciones:
                ProyectoDAO.asignar_empleado(*pair)
                relaciones.add(pair)
                relaciones_creadas += 1

    # 5. Registros de Tiempo
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
        emp = empleados_por_usuario.get(username)
        p_id = proyectos_existentes.get(nombre_proyecto)
        if emp and emp.id_empleado and p_id:
            clave = (int(emp.id_empleado), int(p_id), fecha, float(horas), descripcion)
            if clave not in claves_registros:
                RegistroTiempoDAO.insertar(
                    int(emp.id_empleado), int(p_id),
                    fecha, horas, descripcion
                )
                claves_registros.add(clave)
                registros_creados += 1

    # Resumen de ejecución
    conn = abrir_conexion()
    try:
        conteos = {}
        with conn.cursor() as cursor:
            for tabla in ("departamento", "empleado", "usuario", "proyecto", "proyecto_empleado", "registro_tiempo"):
                cursor.execute(f"SELECT COUNT(*) AS total FROM {tabla}")
                conteos[tabla] = cursor.fetchone()["total"]
    finally:
        conn.close()

    print("\n✓ Carga de semilla finalizada con éxito.")
    print(f"Departamentos en BD: {conteos['departamento']}")
    print(f"Empleados en BD:     {conteos['empleado']}")
    print(f"Usuarios en BD:       {conteos['usuario']}")
    print(f"Proyectos en BD:     {conteos['proyecto']}")
    print(f"Asignaciones P-E:    {conteos['proyecto_empleado']}")
    print(f"Registros de tiempo: {conteos['registro_tiempo']}")
    print("\nInsertados en esta ejecución:")
    print(f"  + Empleados nuevos: {empleados_creados}")
    print(f"  + Usuarios nuevos:  {usuarios_creados}")
    print(f"  + Proyectos nuevos: {proyectos_creados}")
    print(f"  + Asignaciones:     {relaciones_creadas}")
    print(f"  + Registros tiempo: {registros_creados}")


if __name__ == "__main__":
    cargar_semilla()