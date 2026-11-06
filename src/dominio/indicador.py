"""Entidad del dominio para representar un indicador económico."""
import math


class Indicador:
    def __init__(
        self,
        fecha,
        valor,
        verificado_en=None,
        fuente="api_dolar_curso",
        id=None,
    ):
        # Validar que la fecha no venga vacía
        if not isinstance(fecha, str) or not fecha.strip():
            raise ValueError("La fecha del indicador debe ser un texto válido.")

        # Validar que el valor sea un número positivo y finito (exigido en la pauta)
        if (
            type(valor) not in (int, float)
            or not math.isfinite(valor)
            or valor <= 0
        ):
            raise ValueError("El valor del indicador debe ser un número positivo y finito.")

        self.id = id
        self.fecha = fecha.strip()
        self.valor = float(valor)
        self.fuente = fuente
        self.codigo = "dolar"
        self.unidad = "CLP/USD"
        self.verificado_en = verificado_en

    def __str__(self):
        return f"{self.codigo.upper()} ({self.fecha}): ${self.valor:.2f} {self.unidad} | Fuente: {self.fuente}"