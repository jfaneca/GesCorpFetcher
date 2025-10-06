import json

class AppConfig:
    def __init__(self):
        filename = ""
        try:
            filename = "config.json"
            with open(filename, 'r') as f:
                data = json.load(f)
            self.auth_url = data.get("auth_url")
            self.incidents_url = data.get("incidents_url")
            self.api_key = data.get("api_key")
            self.sms_sender_url = data.get("sms_sender_url")
            self.sms_sender_usr = data.get("sms_sender_usr")
            self.sms_sender_pwd = data.get("sms_sender_pwd")
            phone_numbers_from_file = data.get("phone_numbers")
            self.phone_numbers = []
            for elem in phone_numbers_from_file:
                self.phone_numbers.append(elem["phone_number"])
        except FileNotFoundError:
            print(f"File not found: {filename}")
        except Exception as e:
            print(f"Error while reading {filename} file. Error:{e}")