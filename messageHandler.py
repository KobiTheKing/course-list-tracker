from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, redirect
from dotenv import load_dotenv
import os

#Puts the environment variables from .env into os.environ
load_dotenv()

#Setup the client for sending messages
accountSID = os.environ.get('ACCOUNT_SID')
authToken = os.environ.get('AUTH_TOKEN')
client = Client(accountSID, authToken)

#Create flask app
app = Flask(__name__)

#Sends a test message
def sendSMS(msgString):
    message = client.messages.create(
        to = os.environ.get('PERSONAL_PHONE'),
        from_ = os.environ.get('TWILIO_PHONE'),
        body = msgString
    )

#Message Recieving Web Hook. Created with Flask and accessed through ngrok.
@app.route('/sms', methods = ['GET', 'POST'])
def receiveSMS():
    #Retrieve message info
    senderNumber = request.form['From']
    senderMessage = request.form['Body']
    print(f'NUMBER: {senderNumber}, MESSAGE: {senderMessage}')
    resp = MessagingResponse()
    resp.message('BANANA')
    return str(resp)


#msgString = 'Hello!'
#sendSMS(msgString)

#Run the flask web hook
#Use 'ngrok http 5000' in terminal to setup the ngrok tunnel 
app.run(debug = True)