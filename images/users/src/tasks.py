# from celery import shared_task
from src.services.sms import SMSService
from ..celery_app import celery

@celery.task(name="send_security_code_task")
def send_security_code_task(phone_number: str):
    SMSService.send_code_by_telegram(phone_number)
