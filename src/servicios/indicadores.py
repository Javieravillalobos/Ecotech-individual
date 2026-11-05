import requests
from dominio.indicador import Indicador
# Importarás tu indicador_dao cuando lo tengas listo
# from persistencia.indicador_dao import IndicadorDAO 

URL_API_INDICADORS = "https://mindicador.cl/api/dolar"

def obtener_y_guardar_dolar():
    """Consulta la API externa, deserializa el indicador y lo almacena."""
    try:
        respuesta = requests.get(URL_API_INDICADORS, timeout=5)
        if respuesta.status_code != 200:
            raise ConnectionError("No se pudo conectar con la API de indicadores.")
        
        datos = respuesta.json()
        # Tomamos el valor más reciente de la serie que entrega la API
        serie = datos.get("serie", [])
        if not serie:
            raise ValueError("La API no devolvió datos en la serie.")
        
        ultimo_registro = serie[0]
        fecha = ultimo_registro.get("fecha")[:10]  # Extraer solo YYYY-MM-DD
        valor = ultimo_registro.get("valor")
        
        indicador = Indicador(fecha=fecha, valor=valor, fuente="mindicador.cl")
        
        # Aquí guardarías con el DAO (ej: IndicadorDAO.insertar_si_no_existe(indicador))
        return indicador

    except requests.RequestException:
        # Respaldo en caso de que falle la red
        raise ConnectionError("Error de red al intentar consumir la API del dólar.")