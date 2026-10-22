import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from persistencia.conexion import ConexionMySQL


class TestCompatibilidadSQLMySQL(unittest.TestCase):
    def test_convierte_marcadores_de_parametros(self):
        consulta = "SELECT * FROM empleado WHERE id_empleado = ? AND correo = ?"
        self.assertEqual(
            ConexionMySQL._sql(consulta),
            "SELECT * FROM empleado WHERE id_empleado = %s AND correo = %s",
        )

    def test_consulta_sin_parametros_no_cambia(self):
        consulta = "SELECT * FROM empleado ORDER BY id_empleado"
        self.assertEqual(ConexionMySQL._sql(consulta), consulta)


if __name__ == "__main__":
    unittest.main()
