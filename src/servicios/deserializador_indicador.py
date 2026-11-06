"""Transforma respuestas en formato diccionario/JSON a entidades del dominio Indicador."""
from datetime import datetime

from dominio.indicador import Indicador


class DeserializadorIndicador:
    @staticmethod
    def desde_api(datos: dict) -> Indicador:
        """Extrae la fecha y el valor CLP/USD de la respuesta de la API."""
        if not isinstance(datos, dict):
            raise ValueError("Estructura de respuesta de API inválida.")

        if datos.get("result") == "success":
            rates = datos.get("rates")
            if not isinstance(rates, dict) or "CLP" not in rates:
                raise ValueError("La API no entregó el tipo de cambio CLP.")

            fecha_raw = datos.get("time_last_update_utc", "")
            try:
                fecha = datetime.strptime(
                    fecha_raw, "%a, %d %b %Y %H:%M:%S %z"
                ).date().isoformat()
            except ValueError as error:
                raise ValueError("La API entregó una fecha de actualización inválida.") from error

            return Indicador(fecha=fecha, valor=rates["CLP"], fuente="ExchangeRate-API")

        serie = datos.get("serie")
        if isinstance(serie, list) and serie:
            ultimo_registro = serie[0]
            if not isinstance(ultimo_registro, dict):
                raise ValueError("La API entregó un registro inválido.")

            fecha_raw = ultimo_registro.get("fecha", "")
            fecha = fecha_raw.split("T")[0] if isinstance(fecha_raw, str) else ""
            return Indicador(
                fecha=fecha,
                valor=ultimo_registro.get("valor"),
                fuente="mindicador.cl",
            )

        raise ValueError("La API no entregó datos de tipo de cambio reconocibles.")