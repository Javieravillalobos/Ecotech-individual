"""Servicio que coordina la consulta a la API del dólar, su guardado local y el respaldo offline."""
import requests
from persistencia.indicador_dao import IndicadorDAO
from servicios.deserializador_indicador import DeserializadorIndicador
from servicios.permisos import exigir_sesion

URL_API_INDICADORS = "https://open.er-api.com/v6/latest/USD"


def consultar_indicador_dolar(sesion: dict) -> dict:
    """
    Exige sesión activa, consulta la API externa del dólar, persiste el dato en BD local 
    y retorna el resultado. Si la API falla, busca la última observación guardada (Respaldo).
    """
    exigir_sesion(sesion)  # Control de permisos

    try:
        respuesta = requests.get(URL_API_INDICADORS, timeout=10)
        if respuesta.status_code != 200:
            raise ConnectionError("No se pudo conectar con la API de indicadores.")

        datos = respuesta.json()

        # Deserialización usando la clase especializada
        indicador = DeserializadorIndicador.desde_api(datos)

        # Persistir localmente en la base de datos sin duplicar
        guardado_ok = IndicadorDAO.guardar(indicador)

        return {
            "exito": True,
            "origen": "API (ExchangeRate-API)",
            "indicador": indicador,
            "guardado_bd": guardado_ok,
            "mensaje": "Consulta realizada con éxito a la API externa.",
        }

    except (requests.RequestException, ValueError, KeyError, TypeError, ConnectionError) as error:
        # Contingencia / Respaldo Offline en caso de falla de red o API
        try:
            respaldo = IndicadorDAO.obtener_ultimo()
        except Exception as error_bd:
            return {
                "exito": False, "origen": "Ninguno", "indicador": None,
                "guardado_bd": False,
                "mensaje": (
                    "La API no está disponible y no se pudo consultar el respaldo local. "
                    f"Error de base de datos: {error_bd}"
                ),
            }

        if respaldo:
            return {
                "exito": True,
                "origen": "BD Local (Respaldo Offline)",
                "indicador": respaldo,
                "guardado_bd": False,
                "mensaje": f"Falla en servicio externo ({error}). Mostrando último dato disponible en BD.",
            }

        return {
            "exito": False,
            "origen": "Ninguno",
            "indicador": None,
            "guardado_bd": False,
            "mensaje": "No hay conexión con la API ni registros locales guardados.",
        }


def obtener_historial_local(sesion: dict) -> list:
    """Devuelve todo el historial almacenado en la base de datos local."""
    exigir_sesion(sesion)
    return IndicadorDAO.listar_historial()