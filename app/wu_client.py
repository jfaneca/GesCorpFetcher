import pywhatkit as kit
import time

from app.config import AppConfig
from app.logger import Logger

class WUClient:
    def __init__(self, logger:Logger, time_out):
        self.logger = logger.get_logger()
        self.time_out = time_out

    def send(self, phone_numbers, message):
        try:
            self.logger.info(f"Via whatsup, message to send: {message}")
            for phone_number in phone_numbers:
                if not phone_number.startswith("+351"):
                    phone_number = "+351" + phone_number
                # sendwhatmsg_instantly(phone_no, message, wait_time=15, tab_close=False, close_time=3)
                kit.sendwhatmsg_instantly(
                    phone_number,
                    message,
                    wait_time=self.time_out,
                    tab_close=True
                )
                self.logger.info(f"Sent message to {phone_number}")
            return True

        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            return False

if __name__ == "__main__":
    logger = Logger()
    app_config = AppConfig()
    wu_client = WUClient(logger=logger,time_out=15)
    wu_client.send(app_config.phone_numbers, "teste",)