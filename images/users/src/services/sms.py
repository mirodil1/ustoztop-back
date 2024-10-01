import telebot

bot = telebot.TeleBot(
    "5393375054:AAFCLPFARn3GLIyZp_eI1c8YIWOvnpwda7s",
    parse_mode="HTML"
)


class SMSService:
    @staticmethod
    def send_code_by_telegram(security_code):
        bot.send_message(
            chat_id=-1001541588192,
            text=f"Используйте код <strong>{security_code}</strong> для авторизации",
        )