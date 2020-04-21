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
        # Create a dict for logging
        extraInfo = {}
        # Get db config
        dbInfo = app.config.get("DB")
        # Get a database class from factory
        database = databaseFactory(dbInfo)
        # Connect to database
        database.connect()
        sql = f"INSERT INTO `test` (name, description)  VALUES ('{randomString()}', '{randomString(15)}')"
        # Insert sql-statment into dict.
        extraInfo.update({"sql": sql})
        # Execute the sql-statement
        database.execute(sql)
        # Commit the sql-statment
        database.commit()
        rowsInserted = f"{database.rowcount()} recorded inserted"
        # Insert rows inserted into dict
        extraInfo.update({"results": rowsInserted})
        # Log the dict.
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

# Randomnize a string
def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))