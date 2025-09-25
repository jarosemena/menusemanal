import datetime


class InformacionFecha:

    def __init__(self,
                 fecha_del_dia: datetime = None,
                 numero_de_la_semana: int = None,
                 numero_del_dia_en_la_semana: int = None,
                 fecha_del_siguiente_lunes: datetime = None,
                 codigo_de_semana: str = None,
                 codigosemanaanterior: str = None):
        """
        Objeto flexible que puede ser llenado manualmente o automáticamente.
        """
        self.fecha_del_dia = fecha_del_dia
        self.numero_de_la_semana = numero_de_la_semana
        self.numero_del_dia_en_la_semana = numero_del_dia_en_la_semana
        self.fecha_del_siguiente_lunes = fecha_del_siguiente_lunes
        self.codigo_de_semana = codigo_de_semana
        self.codigosemanaanterior = codigosemanaanterior
        self.desde_fecha()

    def desde_fecha(self, fecha_referencia=None):
        fecha_actual = fecha_referencia or datetime.datetime.now()
        # Obtener el número de la semana y el año (igual que tu función)
        año, numero_semana, numero_dia_semana = fecha_actual.isocalendar()
        # Calcular el código de la semana anterior (igual que tu función)
        if numero_semana == 1:
            año_anterior = año - 1
            ultimo_dia_año_anterior = datetime.date(año_anterior, 12, 31)
            numero_semana_anterior = ultimo_dia_año_anterior.isocalendar()[1]
        else:
            # Restar 1 a la semana actual
            año_anterior = año
            numero_semana_anterior = numero_semana - 1
        # Calcular la fecha del siguiente lunes (igual que tu función)
        dias_para_siguiente_lunes = (7 - numero_dia_semana) + 1
        siguiente_lunes = fecha_actual + datetime.timedelta(days=dias_para_siguiente_lunes)
        # Crear códigos de semana (igual que tu función)
        codigosemana = f"{año}-{numero_semana:02d}"  # Formato: AAAA-SS
        codigosemanaanterior = f"{año_anterior}-{numero_semana_anterior:02d}"

        self.fecha_del_dia = fecha_actual.date()
        self.numero_de_la_semana = numero_semana
        self.numero_del_dia_en_la_semana = numero_dia_semana
        self.fecha_del_siguiente_lunes = siguiente_lunes.date()
        self.codigo_de_semana = codigosemana
        self.codigosemanaanterior = codigosemanaanterior

    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            "Fecha del día": self.fecha_del_dia,
            "Número de la semana": self.numero_de_la_semana,
            "Número del día en la semana": self.numero_del_dia_en_la_semana,
            "Fecha del siguiente lunes": self.fecha_del_siguiente_lunes,
            "Código de semana": self.codigo_de_semana,
            "codigosemanaanterior": self.codigosemanaanterior
        }

    def __repr__(self):
        return f"""InformacionFechaFlexible(
    fecha_del_dia='{self.fecha_del_dia}',
    numero_de_la_semana={self.numero_de_la_semana},
    numero_del_dia_en_la_semana={self.numero_del_dia_en_la_semana},
    fecha_del_siguiente_lunes='{self.fecha_del_siguiente_lunes}',
    codigo_de_semana='{self.codigo_de_semana}',
    codigosemanaanterior='{self.codigosemanaanterior}'
)"""
