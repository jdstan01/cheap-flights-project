import os
from twilio.rest import Client
import requests

from flight_data import FlightData
TWILIO_NUMBER = "+16628633224"
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_TOKEN = os.environ.get("TWILIO_TOKEN")


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_TOKEN)

    def check_price(self, price, lowest_price):
        if price < lowest_price:
            return True

    def send_sms(self, text):
        # message = self.client.messages \
        #     .create(
        #     body=text,
        #     from_=TWILIO_NUMBER,
        #     to='+639063510863'
        # )
        print(text)


    def send_email(self, emails, message, google_flight_link):
        import smtplib
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user="derickpython@gmail.com", password="qpreufsvczbqdtaq")
            for email in emails:
                connection.sendmail(
                    from_addr="derickpython@gmail.com",
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message},\n{google_flight_link}".encode("utf-8")
                )

