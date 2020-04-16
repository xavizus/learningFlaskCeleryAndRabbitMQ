from flask import current_app, request, jsonify, g
import logging
import logstash

class FlaskLogger(object):

    def __init__(self, app=None):
        if app is not None:
            self.initApp(app)

    def initApp(self, app):
        self.host = app.config.get("LOG_HOST")
        self.port = app.config.get("LOG_PORT")
        self.appName = app.config.get("LOG_APP_NAME")

        if not self.host or not self.port or not self.appName:
            raise Exception("Required LOG_HOST, LOG_PORT and LOG_APP_NAME in config")
        # Clear all handlers
        app.logger.handlers = []
        handlers = [
            self.consoleLoggingHandler(),
            self.logStashLoggingHandler(self.host, self.port, self.appName)
        ]

        for handler in handlers:
            app.logger.addHandler(handler)
        
        app.after_request(self.afterAppRequest)
        
    @staticmethod
    def logStashLoggingHandler(host, port, appName):
        handler = logstash.TCPLogstashHandler(host, port, version=1, message_type=appName)
        return handler

    @staticmethod
    def consoleLoggingHandler():
        formatter = logging.Formatter("%(asctime)-25s %(levelname)-8s %(message)s")

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        return handler

    def afterAppRequest(self, response):
        extraInfo = {
            "status_code": response.status_code,
            "route": request.endpoint,
            "input_data": request.values.to_dict(),
            "extra_info": g.get("extra", ""),
        }

        msg = f"{request.method} {request.url}"

        current_app.logger.info(f"{msg}", extra=extraInfo)

        return response
