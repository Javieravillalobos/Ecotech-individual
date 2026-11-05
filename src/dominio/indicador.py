class Indicador:
    def __init__(self, fecha, valor, verificado_en=None, fuente="api_dolar_curso", id=None):
        self.id = id
        self.fecha = fecha
        self.valor = float(valor)
        self.fuente = fuente
        self.codigo = "dolar"
        self.unidad = "CLP/USD"
        self.verificado_en = verificado_en

    def __str__(self):
        return f"Indicador({self.codigo}): {self.valor} {self.unidad} - Fecha: {self.fecha} (Fuente: {self.fuente})"