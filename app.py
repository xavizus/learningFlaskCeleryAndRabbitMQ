from flask import Flask, request, Response, jsonify, g
import json
import config
from flaskLogger import FlaskLogger
import logging
import logstash
import sys
from dbFactory.dbFactory import databaseFactory
import random
import string

app = Flask(__name__)
app.config.from_object(config)

FlaskLogger(app)

@app.route('/')
def hello_world():
    try:
        extraInfo = {}
        dbInfo = app.config.get("DB")
        database = databaseFactory(dbInfo)
        database.connect()
        sql = f"INSERT INTO `test` (name, description)  VALUES ('{randomString()}', '{randomString(15)}')"
        extraInfo.update({"sql": sql})
        database.execute(sql)
        database.commit()
        rowsInserted = f"{database.rowcount()} recorded inserted"
        extraInfo.update({"results": rowsInserted})
        g.extra = json.dumps(extraInfo)
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
    
def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))