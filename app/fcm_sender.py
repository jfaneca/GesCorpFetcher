import os
import firebase_admin
from firebase_admin import credentials, messaging
from app.config import AppConfig
from app.logger import Logger

class FCMSender:
    def __init__(self, logger:Logger, app_config:AppConfig):
        self.logger = logger
        self.app_config = app_config
        try:
            cred_path = os.environ.get('FIREBASE_CREDENTIALS', 'jf-firebase-cloud-messaging-credentials.json')
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            # Handle error, e.g., exit if credentials are not found or invalid
            exit()

    def send(self, msg, fcm_tokens):
        for fcm_token in fcm_tokens:
            print(f"fcm_token={fcm_token}")
            message = messaging.Message(
                notification=messaging.Notification(
                    title="Notificações GesCorp",
                    body=msg,
                ),
                # You can add custom data payload here if needed:
                # data={
                #     'key1': 'value1',
                #     'key2': 'value2',
                # },
                token=fcm_token,
            )
            try:
                # Send the message
                response = messaging.send(message)
                print(f'Successfully sent message: {response}')
                return response
            except Exception as e:
                print(f'Error sending message: {e}')
                return None

        return None

if __name__ == "__main__":
    logger = Logger()
    app_config = AppConfig()
    fcm_sender = FCMSender(logger, app_config)
    fcm_sender.send("foo", app_config.fcm_tokens)