from app.config import AppConfig
from app.db_client import DBClient
from app.gescorp_client import GescorpClient
from app.logger import Logger
from app.sms_sender import SMSSender


def get_alerts_missing_at_the_db(gc_alerts, db_alerts):
    missing_alerts = []
    for gc_alert in gc_alerts:
        found = False
        for db_alert in db_alerts:
            if gc_alert.id == str(db_alert[0]):
                found = True
                break
        if not found:
            missing_alerts.append(gc_alert)
    return missing_alerts

class Orchestrator:
    def __init__(self, logger:Logger, app_config:AppConfig, gescorp_client:GescorpClient, db_client:DBClient, sms_sender:SMSSender):
        self.app_config = app_config
        self.gescorp_client = gescorp_client
        self.db_client = db_client
        self.logger = logger.get_logger()
        self.sms_sender = sms_sender

    def notify_new_alerts(self):
        gc_alerts = self.gescorp_client.get_alerts()
        db_alerts = self.db_client.get_all_alerts()
        new_alerts = get_alerts_missing_at_the_db(gc_alerts, db_alerts)
        if new_alerts:
            for new_alert in new_alerts:
                self.logger.info(f"id:{new_alert.id}, hora:{new_alert.data_hora_alerta}")
                viaturas_str = " "
                if new_alert.viaturas:
                    flattened_viaturas = [item for sublist in new_alert.viaturas for item in sublist]
                    viaturas_str = " ".join(flattened_viaturas)
                message = f"Morada:{new_alert.address}, loc:{new_alert.locality}, class:{new_alert.classificacao}, desc_class:{new_alert.desc_classificacao}, n_viaturas:{new_alert.n_viaturas}, n_bombeiros:{new_alert.n_bombeiros}, viaturas:{viaturas_str}, estado:{new_alert.estado}, {new_alert.data_hora_alerta}"
                phone_numbers = self.app_config.phone_numbers
                self.sms_sender.send(message=message, phone_numbers=phone_numbers)
                self.db_client.insert_record(new_alert.id)

if __name__ == "__main__":
    logger = Logger()
    app_config = AppConfig()
    gescorp_client = GescorpClient(logger, app_config)
    db_client = DBClient(logger)
    sms_sender = SMSSender(logger=logger, api_url=app_config.sms_sender_url, user=app_config.sms_sender_usr, password=app_config.sms_sender_pwd)
    orchestrator = Orchestrator(logger, app_config, gescorp_client, db_client, sms_sender)
    orchestrator.notify_new_alerts()
