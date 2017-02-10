#!/usr/bin/python3

from flask import Flask, request, abort
import json 
import requests
import hmac
import hashlib
import codecs
import logging, sys

bot_email = "ucrss@sparkbot.io"
bot_name = "UC RSS Feed"
bearer = "N2NlY2MyODUtMzJmMi00YTY2LWFhNmUtNTU3ZGFjNGRmM2Y3YjE2MWRjNGQtZTc5"
bat_signal  = "https://upload.wikimedia.org/wikipedia/en/c/c6/Bat-signal_1989_film.jpg"

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
app = Flask(__name__)

def setHeaders():         
 accessToken_hdr = 'Bearer ' + bearer
 spark_header = {'Authorization': accessToken_hdr, 'Content-Type': 'application/json; charset=utf-8'}
 return spark_header

def sendSparkGET(url):
    header = setHeaders()
    contents = requests.get(url, headers=header)
    return contents.json()
   
def sendSparkPOST(url, msg):
    header = setHeaders()

    print ()
    print ('url : ',url)
    print ('msg : ',msg)
    print ('header : ',header)
    print ()
    contents = requests.post(url, data=msg, headers=header) 
    print('status : ',contents.status_code)
    print('status : ',contents.raise_for_status())
    print ()
    return contents.json
            # sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})

@app.route('/', methods =['GET', 'POST'])

def index():
    webhook = request.json
    response = sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))

    print ()
    print ('Response : ',response)
    print ()

    #result = json.loads(responseGET)
#    print (json.dumps(response))

#    in_message = response['personEmail']  ### 'text', '').lower()

#    print ()
#    print ('in_message: ',in_message)
#    print ()
    msg = None
    if webhook['data']['personEmail'] != bot_email:
        in_message = response.get('text', '').lower()
        in_message = in_message.replace(bot_name, '')
        if 'test' in in_message or "whoareyou" in in_message:
            msg = "test received"
#            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
        elif 'hello' in in_message:
            message = response.get('text').split('hello')[1].strip(" ")
            if len(message) > 0:
                msg = "Hello echo, '{0}'".format(message)
            else:
                msg = "all is quiet..."
        elif 'help' in in_message:
            print ("help message")
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook["data"]["roomId"], "files": bat_signal})
        if msg != None:
            print ()
            print (msg)
            print ('marker')
            print ()
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook["data"]["roomId"], "text": msg})
    return "true"

if __name__ == "__main__":
    app.run(host='0.0.0.0' , port=8080, debug=True)

