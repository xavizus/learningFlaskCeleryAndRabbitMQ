from flask import current_app, request, jsonify, g
import logging
import logstash

class FlaskLogger(object):

    def __init__(self, app=None):
        # Make sure that we got an app.
        if app is not None:
            self.initApp(app)

    def initApp(self, app):
        # setup variables
        self.host = app.config.get("LOG_HOST")
        self.port = app.config.get("LOG_PORT")
        self.appName = app.config.get("LOG_APP_NAME")

        # Check if we are missing any config.
        if not self.host or not self.port or not self.appName:
            raise Exception("Required LOG_HOST, LOG_PORT and LOG_APP_NAME in config")
        
        # Clear all current handlers
        app.logger.handlers = []
        # Temporary holder of handlers
        handlers = [
            self.consoleLoggingHandler(),
            self.logStashLoggingHandler(self.host, self.port, self.appName)
        ]

        # Add handlers
        for handler in handlers:
            app.logger.addHandler(handler)
        
        # add callback function when event after_request is called.
        app.after_request(self.afterAppRequest)
        
    @staticmethod
    def logStashLoggingHandler(host, port, appName):
        # adds a TCP Logstash handler.
        handler = logstash.TCPLogstashHandler(host, port, version=1, message_type=appName)
        return handler

    @staticmethod
    def consoleLoggingHandler():
        formatter = logging.Formatter("%(asctime)-25s %(levelname)-8s %(message)s")

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        return handler

    def afterAppRequest(self, response):
        # logging extra info
        extraInfo = {
            "status_code": response.status_code,
            "route": request.endpoint,
            "input_data": request.values.to_dict(),
            "extra_info": g.get("extra", ""),
        }

        # Add message
        msg = f"{request.method} {request.url}"

        # Sen the log
        current_app.logger.info(f"{msg}", extra=extraInfo)

        return response
