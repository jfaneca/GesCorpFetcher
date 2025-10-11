import os
import time

from android_sms_gateway import client, domain

from app.config import AppConfig
from app.logger import Logger

class SMSSender:
    def __init__(self, logger:Logger, api_url, user, password):
        self.logger = logger.get_logger()
        self.api_url = api_url
        self.user = user
        self.password = password

    def send(self, message, phone_numbers):
        message = domain.Message(
            message,
            phone_numbers
        )
        current_pid = os.getpid()

        with client.APIClient(
            self.user,
            self.password,
            base_url=self.api_url
        ) as c:
            state = c.send(message)
            #print(state)

            state = c.get_state(state.id)
            while state.state == 'Pending':
                self.logger.info(f"Pending, sleeping half a second. Message:{message}, pid:[{current_pid}]")
                time.sleep(0.5)
                state = c.get_state(state.id)

            if state.state == 'Failed':
                self.logger.error(f"Envio falhado. Message:{message}, pid:[{current_pid}]")
            else:
                self.logger.info(f"Envio efetuado com sucesso! Message:{message}, pid:[{current_pid}]")
                return True

        return False

if __name__ == "__main__":
    logger = Logger()
    app_config = AppConfig()
    sms_sender = SMSSender(logger=logger,api_url=app_config.sms_sender_url, user=app_config.sms_sender_usr,
                           password=app_config.sms_sender_pwd)
    sms_sender.send("teste",app_config.phone_numbers)