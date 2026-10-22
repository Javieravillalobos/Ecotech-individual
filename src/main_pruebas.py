#"https://open.er-api.com/v6/latest/USD"

import requests

def obtener_datos():
    respuesta = requests.get(
        "https://open.er-api.com/v6/latest/USD",
        timeout=(3, 5),
    )

    respuesta.raise_for_status()
    return respuesta.json()

json = obtener_datos()
print(json)

import math

def extraer_primero(datos):
    # Verificar que la respuesta sea un diccionario.
    if not isinstance(datos, dict):
        raise ValueError("Respuesta inesperada.")

    # Obtener la lista de registros del indicador.
    serie = datos.get("serie")

    # Comprobar que sea una lista y contenga registros.
    if not isinstance(serie, list) or not serie:
        raise ValueError("No hay valores disponibles.")

    # Seleccionar el primer registro y obtener su valor.
    registro = serie[0]
    valor = registro["valor"]

    # Aceptar solo números finitos y mayores que cero.
    if (
        type(valor) not in (int, float)
        or not math.isfinite(valor)
        or valor <= 0
    ):
        raise ValueError("Valor del indicador inválido.")

    # Devolver la fecha y el valor como una tupla.
    return registro["fecha"], valor