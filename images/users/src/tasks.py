# from celery import shared_task
from src.services.sms import SMSService
from celery import shared_task

@shared_task()
def send_security_code_task(phone_number: str):
    print("TASK CAlled")
    SMSService.send_code_by_telegram(phone_number)
