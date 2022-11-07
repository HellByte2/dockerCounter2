#!/usr/bin/env python
import os

from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

client = MongoClient("mongo:27017")
database = client["test_database"]
collection = database.collection

counter_init_ = {"value": 0}
collection.insert_one(counter_init_)

@app.route('/')
def hello_world():
    counter = collection.find().sort('value', -1)[0]
    result = str(counter["value"])
    return result

@app.route('/stat')
def increment():
    current_counter = collection.find().sort('value', -1)[0]
    current_datetime = datetime.now()
    client_info = request.user_agent 
    
    collection.insert_one(
        {
        "value": current_counter["value"]+1,
        "datetime": current_datetime, 
        "client_info": str(client_info),
        }
    )
    
    result = str(current_counter["value"]+1) + ' -- ' + str(current_datetime) + ' -- ' + str(client_info)
    return result

@app.route('/about')
def hello():
    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>"
    return html.format(name="Илья", hostname=socket.gethostname())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)

