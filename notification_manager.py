from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()


class NotificationManager:


    def __init__(self):
        self.account_sid = os.environ["account_sid"]
        self.auth_token = os.environ["auth_token"]
        self.client = Client(self.account_sid, self.auth_token)
        self.whatsapp_from = 'whatsapp:+14155238886'
        self.whatsapp_to = 'whatsapp:+46761101792'

    def send_message(self, data):

        message_body = "🔥🔥 Flight Deals Found! 🔥🔥\n\n"

        for price in data["prices"]:
            message_body += (
                f"City: {price['city']}\n"
                f"IATA Code: {price['iataCode']}\n"
                f"Lowest Price: ${price['lowestPrice']}\n"
                f"-------------------\n"
            )


        self.client.messages.create(
            from_=self.whatsapp_from,
            body=message_body,
            to=self.whatsapp_to
        )