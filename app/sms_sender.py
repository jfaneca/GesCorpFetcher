import time

from android_sms_gateway import client, domain
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

        with client.APIClient(
            self.username,
            self.password,
            base_url=self.api_url
        ) as c:
            state = c.send(message)
            #print(state)

            state = c.get_state(state.id)
            while state.state == 'Pending':
                time.sleep(0.5)
                state = c.get_state(state.id)

            if state.state == 'Failed':
                self.logger.info(f"Envio falhado")
            else:
                self.logger.info(f"Envio efetuado com sucesso!")

