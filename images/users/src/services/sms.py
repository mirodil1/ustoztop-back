import requests
import telebot
from flask import current_app as app

from src.cache import redis_db
from src.utils import generate_security_code

bot = telebot.TeleBot(
    "5393375054:AAFCLPFARn3GLIyZp_eI1c8YIWOvnpwda7s",
    parse_mode="HTML",
)


class SMSService:
    url: str = "https://notify.eskiz.uz"

    @staticmethod
    def send_code_by_telegram(phone_number: str):
        code = generate_security_code()
        redis_db.setex(phone_number, 60, str(code))
        bot.send_message(
            chat_id=-1001842149584,
            text=f"Используйте код <strong>{code}</strong> для авторизации",
        )

    @staticmethod
    def verify_code(phone_number: str, security_code: str):
        code = redis_db.get(phone_number)
        if code == security_code:
            return True
        return None

    @classmethod
    def _request(cls, path: str, data: dict):
        request_data = {
            "url": cls.url + path,
            "method": data.get("method"),
            "headers": data.get("headers"),
            "data": data.get("payload"),
        }
        try:
            response = requests.request(timeout=15, **request_data)
            if response.status_code == 200:
                response_data = response.json()
                response_data["error"] = False
        except Exception as err:
            response_data["error"] = True

        return response_data

    @classmethod
    def _authorize(cls):
        token = redis_db.get("eskiz_auth_token")
        if not token:
            data = {
                "method": "POST",
                "headers": {},
                "payload": {
                    "email": app.config["ESKIZ_EMAIL"],
                    "password": app.config["ESKIZ_PASSWORD"],
                },
            }

            response_data = cls._request(path="/api/auth/login", data=data)
            if not response_data["error"]:
                token = response_data["data"]["token"]
                redis_db.setex("eskiz_auth_token", 29 * 24 * 60 * 60, token)
        return token

    @classmethod
    def send_sms(cls, phone_number, message):
        token = cls._authorize()

        data = {
            "method": "POST",
            "headers": {"Authorization": f"Bearer {token}"},
            "payload": {
                "mobile_phone": phone_number,
                "message": message,
                "from": 4546,
                "callback_url": None,
            },
        }
        return cls._request(path="/api/message/sms/send", data=data)
