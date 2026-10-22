from datetime import date

from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from .comun import ejecutar, entero, numero, texto


def _pedir_datos(fila=None):
    if fila is None:
        empleado_id = entero("ID empleado: ")
        proyecto_id = entero("ID proyecto: ")
        fecha = texto(f"Fecha AAAA-MM-DD [{date.today().isoformat()}]: ", True) or date.today().isoformat()
        horas = numero("Horas (mayor que 0 y hasta 24): ", minimo=0.01, maximo=24)
        descripcion = texto("Descripción de tarea: ")
    else:
        empleado_txt = texto(f"ID empleado [{fila['empleado_id']}] (Enter conserva): ", True)
        proyecto_txt = texto(f"ID proyecto [{fila['proyecto_id']}] (Enter conserva): ", True)
        empleado_id = int(empleado_txt) if empleado_txt else fila['empleado_id']
        proyecto_id = int(proyecto_txt) if proyecto_txt else fila['proyecto_id']
        fecha = texto(f"Fecha [{fila['fecha']}]: ", True) or fila['fecha']
        horas_txt = texto(f"Horas [{fila['horas_trabajadas']}]: ", True)
        horas = float(horas_txt.replace(",", ".")) if horas_txt else float(fila['horas_trabajadas'])
        descripcion = texto(f"Descripción [{fila['descripcion_tarea']}]: ", True) or fila['descripcion_tarea']
    if not EmpleadoDAO.buscar_por_id(empleado_id):
        raise ValueError("No existe el empleado indicado.")
    if not ProyectoDAO.buscar_por_id(proyecto_id):
        raise ValueError("No existe el proyecto indicado.")
    return empleado_id, proyecto_id, fecha, horas, descripcion


def menu_registros():
    while True:
        print("\n-- Registros de tiempo --\n1 Crear\n2 Listar\n3 Buscar\n4 Actualizar\n5 Eliminar\n0 Volver")
        op = input("Opción: ").strip()
        if op == "0":
            return
        if op == "1":
            def crear():
                datos = _pedir_datos()
                ident = RegistroTiempoDAO.insertar(*datos)
                print(f"Registro creado con ID {ident}.")
            ejecutar(crear)
        elif op == "2":
            def listar():
                filas = RegistroTiempoDAO.listar()
                if not filas:
                    print("No hay registros de tiempo.")
                for fila in filas:
                    print(f"{fila['id_registro']}: {fila['fecha']} | {fila['empleado']} | {fila['proyecto']} | {fila['horas_trabajadas']} h | {fila['descripcion_tarea']}")
            ejecutar(listar)
        elif op == "3":
            ejecutar(lambda: print(RegistroTiempoDAO.buscar_por_id(entero("ID registro: ")) or "No encontrado."))
        elif op == "4":
            def actualizar():
                ident = entero("ID registro: ")
                fila = RegistroTiempoDAO.buscar_por_id(ident)
                if not fila:
                    print("No encontrado.")
                    return
                datos = _pedir_datos(fila)
                print("Actualizado." if RegistroTiempoDAO.actualizar(ident, *datos) else "No encontrado.")
            ejecutar(actualizar)
        elif op == "5":
            ejecutar(lambda: print("Eliminado." if RegistroTiempoDAO.eliminar(entero("ID registro: ")) else "No encontrado."))
        else:
            print("Opción no válida.")
