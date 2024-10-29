# from celery import shared_task
from celery import shared_task

from src.services.sms import SMSService


@shared_task()
def send_security_code_task(phone_number: str):
    SMSService.send_code_by_telegram(phone_number)
