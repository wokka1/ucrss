#!/usr/bin/python3
#
# needs updated
#
#

from flask import Flask, request, abort
import json 
import requests
import logging, sys
import sqlite3

bot_email = "ucrss@sparkbot.io"
bot_name = "UC RSS Feed"
bearer = "N2NlY2MyODUtMzJmMi00YTY2LWFhNmUtNTU3ZGFjNGRmM2Y3YjE2MWRjNGQtZTc5"
file1  = "http://i.imgur.com/8zesPd1.gifv" 
try:
	db = sqlite3.connect('ucrss.db')
	cursor = db.cursor()
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT, personId TEXT, personEmail TEXT, feed TEXT, active BOOLEAN, dateCreated INTEGER, dateModified INTEGER)
	''')
	db.commit()
except Exception as error:
	db.rollback()
	raise error
finally:
	db.close()

def insert():
	cursor = db.cursor()
	try:
		cursor.execute('''INSERT INTO users(name, personId, personEmail, feed, active, dateCreated, dateModified''')
	except Exception as error:
		db.rollback()
		raise error
	finally:
		db.close()
	
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
    contents = requests.post(url, data=json.dumps(msg), headers=header) 
    return contents.json

@app.route('/', methods =['GET', 'POST'])

def index():
    webhook = request.json
    response = sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))

    msg = None
    if webhook['data']['personEmail'] != bot_email:
        in_message = response.get('text', '').lower()
        in_message = in_message.replace(bot_name, '')
        if 'test' in in_message or "whoareyou" in in_message:
            msg = "test received"
        elif 'hello' in in_message:
            message = response.get('text').split('hello')[1].strip(" ")
            if len(message) > 0:
                msg = "Hello echo, '{0}'".format(message)
            else:
                msg = "all is quiet..."
        elif 'help' in in_message:
            print ("help message")
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook["data"]["roomId"], "files": file1})
        if msg != None:
            print (msg)
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook["data"]["roomId"], "text": msg})
    return "true"

if __name__ == "__main__":
    app.run(host='0.0.0.0' , port=8080, debug=True)

db.close()

