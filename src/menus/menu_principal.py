from persistencia.crear_bd import crear_tablas
from persistencia.semilla_bd import cargar_semilla
from persistencia.conexion import motor_actual
from .menu_empleado import menu_empleados
from .menu_departamento import menu_departamentos
from .menu_proyecto import menu_proyectos
from .menu_registro_tiempo import menu_registros


def menu_principal():
    try:
        crear_tablas()
        cargar_semilla()
        print(f"Base de datos conectada: {motor_actual().upper()}")
    except Exception as exc:
        print(f"No se pudo inicializar la base de datos: {exc}")
        if motor_actual() == "mysql":
            print("Revisa que MySQL esté iniciado, que la base exista y que las credenciales de .env sean correctas.")
        return

    while True:
        print("\n=== ECOTECH SOLUTIONS ===\n1 Empleados\n2 Departamentos\n3 Proyectos\n4 Registros de tiempo\n0 Salir")
        op = input("Opción: ").strip()
        if op == "1":
            menu_empleados()
        elif op == "2":
            menu_departamentos()
        elif op == "3":
            menu_proyectos()
        elif op == "4":
            menu_registros()
        elif op == "0":
            print("Hasta luego.")
            break
        else:
            print("Opción no válida.")
