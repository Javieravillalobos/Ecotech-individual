import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from persistencia.crear_bd import crear_tablas
from persistencia.indicador_dao import IndicadorDAO
from servicios.deserializador_indicador import DeserializadorIndicador
from servicios.indicadores import consultar_indicador_dolar


class TestDeserializadorIndicador(unittest.TestCase):
    def test_deserializa_respuesta_de_exchange_rate_api(self):
        indicador = DeserializadorIndicador.desde_api(
            {
                "result": "success",
                "base_code": "USD",
                "time_last_update_utc": "Fri, 06 Nov 2026 00:02:31 +0000",
                "rates": {"CLP": 966.048728},
            }
        )

        self.assertEqual(indicador.fecha, "2026-11-06")
        self.assertEqual(indicador.valor, 966.048728)
        self.assertEqual(indicador.fuente, "ExchangeRate-API")

    def test_conserva_compatibilidad_con_respuesta_mindicador(self):
        indicador = DeserializadorIndicador.desde_api(
            {"serie": [{"fecha": "2026-11-06T00:00:00.000Z", "valor": 950.0}]}
        )

        self.assertEqual(indicador.fecha, "2026-11-06")
        self.assertEqual(indicador.fuente, "mindicador.cl")


class TestPersistenciaIndicador(unittest.TestCase):
    def test_consulta_api_y_guarda_el_indicador(self):
        with tempfile.TemporaryDirectory() as directorio:
            db_path = str(Path(directorio) / "indicadores.db")
            with patch.dict(os.environ, {"DB_ENGINE": "sqlite", "DB_NAME": db_path}):
                crear_tablas()
                respuesta = SimpleNamespace(
                    status_code=200,
                    json=lambda: {
                        "result": "success",
                        "time_last_update_utc": "Fri, 06 Nov 2026 00:02:31 +0000",
                        "rates": {"CLP": 966.048728},
                    },
                )
                with (
                    patch("servicios.indicadores.exigir_sesion"),
                    patch("servicios.indicadores.requests.get", return_value=respuesta),
                ):
                    resultado = consultar_indicador_dolar({"usuario": "test"})
                respaldo = IndicadorDAO.obtener_ultimo()

        self.assertTrue(resultado["exito"])
        self.assertTrue(resultado["guardado_bd"])
        self.assertEqual(resultado["origen"], "API (ExchangeRate-API)")
        self.assertEqual(respaldo.fecha, "2026-11-06")
        self.assertEqual(respaldo.valor, 966.048728)
        self.assertEqual(respaldo.fuente, "ExchangeRate-API")

    def test_incluye_error_real_si_falla_el_respaldo_local(self):
        with (
            patch("servicios.indicadores.exigir_sesion"),
            patch(
                "servicios.indicadores.requests.get",
                side_effect=ConnectionError("sin conexión"),
            ),
            patch.object(IndicadorDAO, "obtener_ultimo", side_effect=RuntimeError("BD apagada")),
        ):
            resultado = consultar_indicador_dolar({"usuario": "test"})

        self.assertIn("BD apagada", resultado["mensaje"])


if __name__ == "__main__":
    unittest.main()
