#!/usr/bin/env python
"""Flask server ofr counter application"""
import os
import socket
from datetime import datetime
from pymongo import MongoClient
from flask import Flask, request


app = Flask(__name__)

client = MongoClient("mongo:27017")
database = client["test_database"]
collection = database.collection

if not collection.count_documents({"value": 0}):
    counter_init_ = {"value": 0}
    collection.insert_one(counter_init_)

@app.route('/')
def hello_world():
    """ Return value of counter"""
    counter = collection.find().sort('value', -1)[0]
    result = str(counter["value"])
    return result

@app.route('/stat')
def increment():
    """Increase value of counter by 1, save user agent and current date"""
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
    next_value = current_counter["value"] + 1
    result = str(next_value) + ' -- ' + str(current_datetime) + ' -- ' + str(client_info)
    return result

@app.route('/about')
def hello():
    """Return name of creator and hostname"""
    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>"
    return html.format(name="Илья", hostname=socket.gethostname())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
