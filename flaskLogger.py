from flask import current_app, request, jsonify, g
import logging
import logstash

class FlaskLogger(object):

    REQUIRED = (
        "LOG_HOST",
        "LOG_PORT",
        "LOG_APP_NAME"
    )

    def __init__(self, app=None):
        # Make sure that we got an app.
        if app is not None:
            self.initApp(app)

    def initApp(self, app):

        # Controll that the requried config settings exist.
        missing_requried = []
        for require in self.REQUIRED:
            if not app.config.get(require):
                missing_requried.append(require)
        
        if missing_requried:
            message = "FlaskLogger require following: "
            for missing in missing_requried[:-1]:
                message += f"{missing}, "
            else:
                message += f"{missing_requried[-1]} in config."
            raise Exception(message)

        # setup variables
        self.host = app.config.get("LOG_HOST")
        self.port = app.config.get("LOG_PORT")
        self.appName = app.config.get("LOG_APP_NAME")

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
