from twilio.rest import Client
from dotenv import load_dotenv
import os

#Puts the environment variables from .env into os.environ
load_dotenv()

accountSID = os.environ.get('ACCOUNT_SID')
authToken = os.environ.get('AUTH_TOKEN')
client = Client(accountSID, authToken)

#Sends a test message
def sendMessage(msgString):
    message = client.messages.create(
        to = os.environ.get('PERSONAL_PHONE'),
        from_ = os.environ.get('TWILIO_PHONE'),
        body = msgString
    )

msgString = 'Hello!'
sendMessage(msgString)