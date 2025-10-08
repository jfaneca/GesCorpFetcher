from datetime import datetime, timedelta
import requests

from app.alert import Alert
from app.config import AppConfig
from app.logger import Logger


class GescorpClient:
    def __init__(self, logger:Logger, app_config:AppConfig):
        self.logger = logger.get_logger()
        self.api_key = app_config.api_key
        self.auth_url = app_config.auth_url
        self.incidents_url = app_config.incidents_url
        self.access_key, self.expiration_date = self.get_auth_token()

    def get_auth_token(self):
        AUTH_HEADERS = {
            "apikey": self.api_key,  # A common format for API keys
            # "Authorization": f"Bearer {API_KEY}", # Another common format, if the API uses 'Bearer' tokens
            "Accept": "application/json"  # Optional: good practice to specify expected response type
        }
        response = requests.get(self.auth_url, headers=AUTH_HEADERS)
        self.logger.info("Got a response when requesting a new auth token")

        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            access_key = data['authentication']['access_key']
            expiration_date_str = data['authentication']['expiration_date']
            date_format = "%Y-%m-%d %H:%M:%S"
            expiration_date = datetime.strptime(expiration_date_str, date_format)

            return access_key, expiration_date

        return None

    def get_alerts(self):
        alerts = []
        self.renew_access_if_required()
        REQ_HEADERS = {
            "apikey": self.api_key,
            "Accept": "application/json",  # Optional: good practice to specify expected response type
            "X-AccessKey": self.access_key
        }
        response = requests.get(self.incidents_url, headers=REQ_HEADERS)
        # Raise an exception for bad status codes (4xx or 5xx)
        #response.raise_for_status()

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            incidents_data = data.get("incident", [])  # Safely get the "incident" list
            if incidents_data:
                self.logger.info(f"#incidents at gescorp={len(incidents_data)}")
            for incident in incidents_data:
                estado = incident.get("estado")
                if estado == "Alerta" or estado == "Em Curso":
                #if incident.get("estado") == "Alerta":
                    id = incident.get("id")
                    numero = incident.get("numero")
                    numero_cdos = incident.get("numero_cdos")
                    address = incident.get("morada")
                    locality = incident.get("localidade_morada")
                    data_hora_alerta = incident.get("data_hora_alerta")
                    sado_latitude_gps = incident.get("sado_latitude_gps")
                    sado_longitude_gps = incident.get("sado_longitude_gps")
                    classificacao = incident.get("classificacao")
                    desc_classificacao = incident.get("desc_classificacao")
                    n_bombeiros = incident.get("n_bombeiros")
                    n_viaturas = incident.get("n_viaturas")
                    viaturas = incident.get("viaturas")
                    alert = Alert(id=id, numero=numero,numero_cdos=numero_cdos,address=address, locality=locality,
                                  data_hora_alerta=data_hora_alerta, sado_latitude_gps=sado_latitude_gps,
                                  sado_longitude_gps=sado_longitude_gps, classificacao=classificacao, desc_classificacao=desc_classificacao,
                                  n_bombeiros=n_bombeiros, n_viaturas=n_viaturas, estado=estado, viaturas=viaturas)
                    self.logger.info(f"Alerta data_hora:{data_hora_alerta}")
                    alerts.append(alert)

        return alerts

    def renew_access_if_required(self):
        now = datetime.now()
        time_difference = now - self.expiration_date
        absolute_difference = abs(time_difference)
        target_difference = timedelta(minutes=15)
        if absolute_difference <= target_difference:
            self.logger.info(f"New access_key generated, target_difference='{target_difference}' , absolute_difference='{absolute_difference}'")
            self.access_key, self.expiration_date = self.get_auth_token()