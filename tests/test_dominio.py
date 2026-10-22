import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from dominio.usuario import Usuario
from dominio.empleado import Empleado
from dominio.departamento import Departamento
from dominio.proyecto import Proyecto
from dominio.registro_tiempo import RegistroTiempo


class TestDominio(unittest.TestCase):
    def test_autenticacion(self):
        u = Usuario("alumno", "clave-segura")
        self.assertTrue(u.autenticar("clave-segura"))
        self.assertFalse(u.autenticar("incorrecta"))

    def test_empleado_valido(self):
        e = Empleado("alumno", "clave", nombre="Ana", correo="ana@example.com")
        self.assertEqual(e.obtenerSalario(), 0.0)

    def test_salario_negativo(self):
        with self.assertRaises(ValueError):
            Empleado("alumno", "clave", nombre="Ana", correo="ana@example.com", salario=-1)

    def test_departamento(self):
        d = Departamento(nombre="TI")
        self.assertEqual(d.cantidad_empleados(), 0)

    def test_proyecto(self):
        p = Proyecto(nombre="Proyecto A")
        self.assertEqual(p.nombre, "Proyecto A")

    def test_registro_horas_invalidas(self):
        with self.assertRaises(ValueError):
            RegistroTiempo(empleado_id=1, proyecto_id=1, horas_trabajadas=0,
                           descripcion_tarea="Trabajo")


if __name__ == "__main__":
    unittest.main()
