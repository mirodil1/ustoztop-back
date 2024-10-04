import random
import telebot

from src.utils import generate_security_code
from src.cache import redis_db

bot = telebot.TeleBot(
    "5393375054:AAFCLPFARn3GLIyZp_eI1c8YIWOvnpwda7s",
    parse_mode="HTML"
)


class SMSService:
    @staticmethod
    def send_code_by_telegram(phone_number: str = None):
        code = generate_security_code()
        redis_db.setex(phone_number, 60, code)

        bot.send_message(
            chat_id=-1001541588192,
            text=f"Используйте код <strong>132566<strong/> для авторизации",
        ) 
    @staticmethod
    def verify_code(phone_number: str):
        code = redis_db.get(phone_number)
        print(code)
