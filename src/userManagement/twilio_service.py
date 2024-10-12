from twilio.rest import Client
import os
from django.conf import settings

def send_trip_sms(driver_phone_number, message):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token =  settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=message,
        from_= settings.TWILIO_PHONE_NUMBER,
        to=driver_phone_number
    )