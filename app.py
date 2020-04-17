from flask import Flask, request, Response, jsonify, g
import config
from flaskLogger import FlaskLogger
import logging
import logstash
import sys
from dbFactory.dbFactory import databaseFactory

app = Flask(__name__)
app.config.from_object(config)

FlaskLogger(app)

@app.route('/')
def hello_world():
    try:
        dbInfo = app.config.get("DB")
        database = databaseFactory(dbInfo)
    except Exception as error:
        print(error)
    return "Hello"

@app.route('/hello/<string:name>', methods=['POST'])
def hello(name=None):
    try:
        requestBody = request.get_data()
        g.extra = requestBody.decode("utf-8")
        return f"Hello {name}!"
    except Exception as e:
        app.logger.warning(f"{e}")
    
