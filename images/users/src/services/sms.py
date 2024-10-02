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
        print("SENDING")
        code = generate_security_code(6)
        redis_db.setex(phone_number, 60, code)

        bot.send_message(
            chat_id=-1001541588192,
            text=f"Используйте код {code} для авторизации",
        )
