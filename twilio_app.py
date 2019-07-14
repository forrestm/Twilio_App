# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
from twilio.rest import Client
from Budget import Budget

app = Flask(__name__)

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

fmo = os.environ['NUMBER']
kmo = os.environ['KNUMBER']
twilio_number = os.environ['TWILIO_NUMBER']

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    bud = Budget(body)
    # Start our TwiML response
    resp = MessagingResponse()
    from_number = request.values.get('From')
    if from_number == fmo:
        to_number = fmo
        name = 'Forrest'
    elif from_number == kmo:
        to_number = kmo
        name = 'K'
    else:
        resp.message("New phone, who dis?")
        return "Finished"

    if body in ['Yes', 'YES', 'Yeah', 'yeah', 'y', 'yes']:
        chase_resp = bud.Groceries_Yes()
        client.messages.create(body=chase_resp,from_=twilio_number, to=to_number)
        
    elif body in ['Undo', 'undo']:
        chase_resp = bud.Undo()
        client.messages.create(body=chase_resp,from_=twilio_number, to=to_number)
        
    elif body in ['g?', 'G?']:
        chase_resp = bud.Current_Amounts(True)
        client.messages.create(body=chase_resp,from_=twilio_number, to=to_number)
        
    elif body in ['H?', 'h?']:
        chase_resp = bud.Help(name)
        client.messages.create(body=chase_resp,from_=twilio_number, to=to_number)
        
    elif " ".join(body.split()[0:2]) == "Chase account":
        chase_resp = bud.Received_Bank_text()
        client.messages.create(body=chase_resp,from_=twilio_number, to=to_number)

    elif " ".join(body.split()[0][0]) == "$":
        chase_resp = bud.Manual_Entry()
        client.messages.create(body=chase_resp,from_=twilio_number, to=to_number)

    else:
        chase_resp = bud.Current_Amounts(False)
        client.messages.create(body=chase_resp,from_=twilio_number, to=to_number)

    return "Finished"

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

##############################################################



# Cronjob to run a python script that will append a Yaml entry with the weeks setup