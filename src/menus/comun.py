from getpass import getpass


def texto(mensaje, permitir_vacio=False):
    valor = input(mensaje).strip()
    if not valor and not permitir_vacio:
        raise ValueError("El campo no puede estar vacío.")
    return valor


def entero(mensaje):
    try:
        valor = int(input(mensaje).strip())
    except ValueError as exc:
        raise ValueError("Debe ingresar un número entero.") from exc
    if valor <= 0:
        raise ValueError("Debe ingresar un entero mayor que cero.")
    return valor


def numero(mensaje, minimo=None, maximo=None):
    try:
        valor = float(input(mensaje).strip().replace(",", "."))
    except ValueError as exc:
        raise ValueError("Debe ingresar un número válido.") from exc
    if minimo is not None and valor < minimo:
        raise ValueError(f"El número debe ser como mínimo {minimo}.")
    if maximo is not None and valor > maximo:
        raise ValueError(f"El número no puede superar {maximo}.")
    return valor


def ejecutar(accion):
    try:
        accion()
    except ValueError as exc:
        print(f"Datos inválidos: {exc}")
    except Exception as exc:
        # Mensaje entendible para la aplicación académica; no se imprime información sensible.
        print(f"No se pudo completar la operación: {exc}")
