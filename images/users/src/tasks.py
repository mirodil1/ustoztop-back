from celery import shared_task

from src.services.sms import SMSService


@shared_task()
def send_security_code_task(phone_number: str, lang: str):
    message = {
        "uz": "Ustoztop platformasiga kirish uchun tasdiqlash kodingiz:",
        "ru": "Ваш код подтверждения для входа на платформу Ustoztop:",
    }
    SMSService.send_sms(message=message[lang], phone_number=phone_number)
