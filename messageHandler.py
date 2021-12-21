from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

#TODO change to environment variables
accountSID = os.environ.get('ACCOUNT_SID')
authToken = os.environ.get('AUTH_TOKEN')
client = Client(accountSID, authToken)

#Create test message
msgString = 'This is a test message!'
message = client.messages.create(
    to = os.environ.get('PERSONAL_PHONE'),
    from_ = os.environ.get('TWILIO_PHONE'),
    body = msgString
)