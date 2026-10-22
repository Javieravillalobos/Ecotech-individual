from persistencia.proyecto_dao import ProyectoDAO
from persistencia.empleado_dao import EmpleadoDAO
from .comun import ejecutar, entero, texto


def menu_proyectos():
    while True:
        print("\n-- Proyectos --\n1 Crear\n2 Listar\n3 Buscar\n4 Actualizar\n5 Eliminar\n6 Asignar empleado\n0 Volver")
        op = input("Opción: ").strip()
        if op == "0":
            return
        if op == "1":
            def crear():
                ident = ProyectoDAO.insertar(texto("Nombre: "), texto("Descripción: ", True),
                    texto("Fecha inicio AAAA-MM-DD (opcional): ", True),
                    texto("Fecha fin AAAA-MM-DD (opcional): ", True))
                print(f"Proyecto creado con ID {ident}.")
            ejecutar(crear)
        elif op == "2":
            def listar():
                filas = ProyectoDAO.listar()
                if not filas:
                    print("No hay proyectos registrados.")
                for fila in filas:
                    print(f"{fila['id_proyecto']}: {fila['nombre']} | {fila['fecha_inicio']} - {fila['fecha_fin']}")
            ejecutar(listar)
        elif op == "3":
            ejecutar(lambda: print(ProyectoDAO.buscar_por_id(entero("ID: ")) or "No encontrado."))
        elif op == "4":
            def actualizar():
                ident = entero("ID: ")
                fila = ProyectoDAO.buscar_por_id(ident)
                if not fila:
                    print("No encontrado.")
                    return
                print("Actualizado." if ProyectoDAO.actualizar(ident,
                    texto(f"Nombre [{fila['nombre']}]: ", True) or fila['nombre'],
                    texto(f"Descripción [{fila['descripcion']}]: ", True) or fila['descripcion'],
                    texto(f"Inicio [{fila['fecha_inicio']}]: ", True) or fila['fecha_inicio'],
                    texto(f"Fin [{fila['fecha_fin']}]: ", True) or fila['fecha_fin']) else "No encontrado.")
            ejecutar(actualizar)
        elif op == "5":
            ejecutar(lambda: print("Eliminado." if ProyectoDAO.eliminar(entero("ID: ")) else "No encontrado."))
        elif op == "6":
            def asignar():
                proyecto_id = entero("ID proyecto: ")
                empleado_id = entero("ID empleado: ")
                if not ProyectoDAO.buscar_por_id(proyecto_id):
                    raise ValueError("No existe ese proyecto.")
                if not EmpleadoDAO.buscar_por_id(empleado_id):
                    raise ValueError("No existe ese empleado.")
                ProyectoDAO.asignar_empleado(proyecto_id, empleado_id)
                print("Empleado asignado al proyecto.")
            ejecutar(asignar)
        else:
            print("Opción no válida.")
