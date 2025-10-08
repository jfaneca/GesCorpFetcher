class Alert:
    def __init__(self, id, numero, numero_cdos, address, locality, data_hora_alerta, sado_latitude_gps, sado_longitude_gps,
                 classificacao, desc_classificacao, n_bombeiros, n_viaturas, estado, viaturas):
        self.id = id
        self.numero = numero
        self.numero_cdos = numero_cdos
        self.address = address
        self.locality = locality
        self.data_hora_alerta = data_hora_alerta
        self.sado_latitude_gps = sado_latitude_gps
        self.sado_longitude_gps = sado_longitude_gps
        self.desc_classificacao = desc_classificacao
        self.classificacao = classificacao
        self.n_bombeiros = n_bombeiros
        self.n_viaturas = n_viaturas
        self.estado = estado
        self.viaturas = viaturas