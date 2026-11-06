"""Transforma respuestas en formato diccionario/JSON a entidades del dominio Indicador."""
from dominio.indicador import Indicador


class DeserializadorIndicador:
    @staticmethod
    def desde_api(datos: dict) -> Indicador:
        """Extrae fecha y valor del JSON de mindicador.cl y construye un objeto Indicador."""
        if not isinstance(datos, dict):
            raise ValueError("Estructura de respuesta de API inválida.")

        serie = datos.get("serie", [])
        if not isinstance(serie, list) or not serie:
            raise ValueError("La API no entregó registros en la serie.")

        ultimo_registro = serie[0]
        fecha_raw = ultimo_registro.get("fecha", "")
        valor = ultimo_registro.get("valor")

        # Formatear la fecha a YYYY-MM-DD
        fecha = fecha_raw.split("T")[0] if "T" in fecha_raw else fecha_raw

        return Indicador(
            fecha=fecha,
            valor=valor,
            fuente="mindicador.cl"
        )