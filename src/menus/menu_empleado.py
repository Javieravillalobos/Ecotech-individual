import re
import math
from getpass import getpass


from .menu_dominio_empleado import crear_empleado_desde_datos
from persistencia.empleado_dao import EmpleadoDAO
from .comun import ejecutar, entero, numero, texto


def pedir_usuario(mensaje="Usuario: ", actual=None):
    while True:
        valor = input(mensaje).strip()

        if actual is not None and valor == "":
            return actual

        if not valor:
            print("El usuario es obligatorio.")
            continue

        if not re.fullmatch(r"[A-Za-z0-9_.-]{3,30}", valor):
            print(
                "Usuario inválido. Use entre 3 y 30 caracteres: "
                "letras sin tildes, números, punto, guion o guion bajo."
            )
            continue

        return valor


def pedir_nombre(mensaje="Nombre: ", actual=None):
    while True:
        valor = input(mensaje).strip()

        if actual is not None and valor == "":
            return actual

        if not valor:
            print("Ingrese un nombre. Es obligatorio.")
            continue

        if not all(
            caracter.isalpha()
            or caracter.isspace()
            or caracter in "-'’"
            for caracter in valor
        ):
            print(
                "Nombre inválido. Use solamente letras, espacios, "
                "tildes, ñ, apóstrofes o guiones."
            )
            continue

        if not any(caracter.isalpha() for caracter in valor):
            print("El nombre debe contener al menos una letra.")
            continue

        if len(valor) < 2 or len(valor) > 100:
            print("El nombre debe tener entre 2 y 100 caracteres.")
            continue

        return valor


def pedir_correo(mensaje="Correo: ", actual=None):
    patron = r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+$"

    while True:
        valor = input(mensaje).strip()

        if actual is not None and valor == "":
            return actual

        if not valor:
            print("El correo es obligatorio.")
            continue

        if len(valor) > 254 or not re.fullmatch(patron, valor):
            print("Correo inválido. Ejemplo: usuario@correo.cl")
            continue

        return valor


def pedir_contrasena(mensaje="Contraseña: ", permitir_vacia=False):
    while True:
        valor = getpass(mensaje)

        if permitir_vacia and valor == "":
            return None

        if not valor.strip():
            print("La contraseña es obligatoria.")
            continue

        if len(valor) < 8:
            print("La contraseña debe tener al menos 8 caracteres.")
            continue

        if len(valor) > 128:
            print("La contraseña no puede superar los 128 caracteres.")
            continue

        if any(caracter.isspace() for caracter in valor):
            print("La contraseña no debe contener espacios.")
            continue

        return valor


def pedir_telefono(mensaje="Teléfono (opcional): ", actual=None):
    while True:
        valor = input(mensaje).strip()

        if actual is not None and valor == "":
            return actual

        if not valor:
            return None

        if not re.fullmatch(r"\+?[0-9() -]+", valor):
            print("Teléfono inválido. Use números, +, espacios, "
                  "paréntesis o guiones.")
            continue

        cantidad_digitos = sum(c.isdigit() for c in valor)

        if not 7 <= cantidad_digitos <= 15:
            print("El teléfono debe contener entre 7 y 15 dígitos.")
            continue

        return valor


def pedir_salario(mensaje="Salario: ", actual=None):
    while True:
        valor = input(mensaje).strip()

        if actual is not None and valor == "":
            return float(actual)

        if not valor:
            print("El salario es obligatorio.")
            continue

        if not re.fullmatch(r"\d+(?:[.,]\d{1,2})?", valor):
            print("Salario inválido. Ejemplo: 650000 o 650000,50.")
            continue

        try:
            salario = float(valor.replace(",", "."))
        except ValueError:
            print("Ingrese un salario numérico válido.")
            continue

        if not math.isfinite(salario):
            print("El salario debe ser un número finito.")
            continue

        if salario < 0:
            print("El salario no puede ser negativo.")
            continue

        return salario


def pedir_rol(mensaje="Rol [Empleado]: ", actual=None):
    while True:
        valor = input(mensaje).strip()

        if actual is not None and valor == "":
            return actual

        if not valor:
            return "Empleado"

        if len(valor) > 50:
            print("El rol no puede superar los 50 caracteres.")
            continue

        if not all(
            caracter.isalpha()
            or caracter.isspace()
            or caracter in "-_"
            for caracter in valor
        ):
            print("El rol solo admite letras, espacios, guiones "
                  "y guiones bajos.")
            continue

        return valor


def pedir_direccion(mensaje="Dirección (opcional): ", actual=None):
    while True:
        valor = input(mensaje).strip()

        if actual is not None and valor == "":
            return actual

        if not valor:
            return None

        if len(valor) > 200:
            print("La dirección no puede superar los 200 caracteres.")
            continue

        return valor


def pedir_id():
    while True:
        valor = input("ID: ").strip()

        if not valor.isdigit() or int(valor) <= 0:
            print("Ingrese un ID entero positivo.")
            continue

        return int(valor)

def menu_empleados():
    while True:
        print(
            "\n-- Empleados --\n"
            "1 Registrar\n"
            "2 Listar\n"
            "3 Buscar\n"
            "4 Actualizar\n"
            "5 Eliminar\n"
            "0 Volver"
        )

        op = input("Opción: ").strip()

        if op == "0":
            return

        elif op == "1":
            ejecutar(registrar)

        elif op == "2":
            ejecutar(listar)

        elif op == "3":
            ejecutar(buscar)

        elif op == "4":
            ejecutar(actualizar)

        elif op == "5":
            ejecutar(eliminar)

        else:
            print("Opción no válida. Seleccione una opción del menú.")


def registrar():
    print("\n-- Registrar empleado --")

    datos = {
        "username": pedir_usuario(),
        "password": pedir_contrasena(),
        "nombre": pedir_nombre(),
        "correo": pedir_correo(),
        "direccion": pedir_direccion() or "",
        "telefono": pedir_telefono() or "",
        "salario": pedir_salario(),
        "rol": pedir_rol(),
        "departamento_id": None,
    }

    # Se crea y valida el objeto antes de acceder a la base de datos.
    empleado = crear_empleado_desde_datos(datos)
    EmpleadoDAO.insertar(empleado)

    print(f"Empleado creado con ID {empleado.id_empleado}.")


def listar():
    print("\n-- Lista de empleados --")

    empleados = EmpleadoDAO.listar()

    if not empleados:
        print("No hay empleados registrados.")
        return

    for empleado in empleados:
        print(
            f"{empleado.id_empleado}: "
            f"{empleado.nombre} | "
            f"{empleado.correo} | "
            f"{empleado.rol} | "
            f"${float(empleado.salario):.2f}"
        )

def buscar():
    print("\n-- Buscar empleado --")

    ident = pedir_id()
    empleado = EmpleadoDAO.buscar_por_id(ident)

    if not empleado:
        print("Empleado no encontrado.")
        return

    print(f"ID: {empleado.id_empleado}")
    print(f"Nombre: {empleado.nombre}")
    print(f"Correo: {empleado.correo}")
    print(f"Dirección: {empleado.direccion or '-'}")
    print(f"Teléfono: {empleado.telefono or '-'}")
    print(f"Rol: {empleado.rol}")
    print(f"Salario: ${float(empleado.salario):.2f}")


def actualizar():
    print("\n-- Actualizar empleado --")

    ident = pedir_id()
    empleado = EmpleadoDAO.buscar_por_id(ident)

    if not empleado:
        print("Empleado no encontrado.")
        return

    print("Presione Enter para conservar el valor actual.")

    nombre = pedir_nombre(
        f"Nombre [{empleado.nombre}]: ",
        actual=empleado.nombre
    )

    correo = pedir_correo(
        f"Correo [{empleado.correo}]: ",
        actual=empleado.correo
    )

    direccion = pedir_direccion(
        f"Dirección [{empleado.direccion or ''}]: ",
        actual=empleado.direccion
    )

    telefono = pedir_telefono(
        f"Teléfono [{empleado.telefono or ''}]: ",
        actual=empleado.telefono
    )

    salario = pedir_salario(
        f"Salario [{empleado.salario}]: ",
        actual=empleado.salario
    )

    rol = pedir_rol(
        f"Rol [{empleado.rol}]: ",
        actual=empleado.rol
    )

    if not empleado.actualizarPerfil(
        nombre,
        correo,
        direccion,
        telefono
    ):
        raise ValueError(
            "El perfil no es válido. No se guardaron los cambios."
        )

    empleado.salario = salario
    empleado.rol = rol

    empleado.validar()

    if EmpleadoDAO.actualizar(empleado):
        print("Empleado actualizado correctamente.")
    else:
        print("No se realizaron cambios en la base de datos.")


def eliminar():
    print("\n-- Eliminar empleado --")

    ident = pedir_id()
    empleado = EmpleadoDAO.buscar_por_id(ident)

    if not empleado:
        print("Empleado no encontrado.")
        return

    print(
        f"Empleado seleccionado: {empleado.nombre} "
        f"(ID {empleado.id_empleado})"
    )

    while True:
        confirmar = input(
            "¿Confirma la eliminación? (s/n): "
        ).strip().lower()

        if confirmar == "s":
            resultado = EmpleadoDAO.eliminar(ident)

            if resultado:
                print("Empleado eliminado correctamente.")
            else:
                print("No se pudo eliminar el empleado.")

            return

        elif confirmar == "n":
            print("Eliminación cancelada.")
            return

        else:
            print("Respuesta inválida. Escriba 's' o 'n'.")