from re import sub
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, redirect
from dotenv import load_dotenv
from datamanager import trackCourse, untrackCourse
from scraper import checkValidity
import os



# Puts the environment variables from .env into os.environ
load_dotenv()

# Setup the client for sending messages
accountSID = os.environ.get('ACCOUNT_SID')
authToken = os.environ.get('AUTH_TOKEN')
client = Client(accountSID, authToken)

# Create flask app
app = Flask(__name__)

# Sets up the Twilio sms connection and the flask web hook
def setup():
    # Run the flask web hook
    # Use 'ngrok http 5000' in terminal to setup the ngrok tunnel. Then copy https url into 'A message comes in' webhook.
    app.run(debug = True)

# Sends a text message
# param phoneNums: a list of numbers to send the message to
# param msgString: the contents of the message
def sendSMS(phoneNums, msgString):
    for phoneNum in phoneNums:
        message = client.messages.create(
            to = phoneNum,
            from_ = os.environ.get("TWILIO_PHONE"),
            body = msgString
        )

        print(f"Sent Outbound Message: NUMBER: {phoneNum}, MESSAGE: {msgString}")

# Message Recieving Web Hook. Created with Flask and accessed through ngrok.
@app.route("/sms", methods = ["GET", "POST"])
def receiveSMS():
    # Retrieve message info
    senderNumber = request.form["From"]
    senderMessage = request.form["Body"]

    print(f"Recieved Inbound Message: NUMBER: {senderNumber}, MESSAGE: {senderMessage}")

    response = MessagingResponse()

    if senderMessage.split()[0].lower() == "track" and len(senderMessage.split()) == 3:
        # Command: 'track <CRN> <subject>'
        CRN = senderMessage.split()[1]
        subject = senderMessage.split()[2]

        try:
            if checkValidity(CRN, subject):
                # Both CRN and subject are good
                trackCourse(CRN, subject, senderNumber)
                response.message(f"Success: Course with CRN: {CRN}, subject: {subject} now being tracked.")
                return str(response)
            else:
                # The CRN is invalid but the subject is good
                response.message(f"Error: CRN: {CRN} is invalid!")
                return str(response)
        except Exception as e:
            # The subject is invalid
            response.message(f"Error: subject: {subject} is invalid!")
            return str(response)
    elif senderMessage.split()[0].lower() == "untrack" and len(senderMessage.split()) == 2:
        # Command: 'untrack <CRN>'
        CRN = senderMessage.split()[1]

        if untrackCourse(CRN, senderNumber):
            response.message(f"Success: Course with CRN: {CRN} no longer being tracked.")
            return str(response)
        else:
            response.message(f"Error: CRN: {CRN} is invalid")
            return str(response)

    response.message(f"Invalid command!")
    return str(response)
    #resp = MessagingResponse()
    #resp.message('BANANA')
    #return str(resp)


#msgString = 'Hello!'
#sendSMS(msgString)