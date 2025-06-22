from flask import request, jsonify, Flask
from app import create_app
#import logging
from app import logging_config
import os,json

# https://www.baeldung.com/ops/gunicorn-server-docker

fapp= create_app()

#logger = logging.getLogger(__name__)
logger = logging_config.setup_logging().getLogger(__name__)
api_pass = os.getenv("API_PASSWORD") # From Docker-compose setting
api_key = os.getenv("API_KEY")
print(f"API-Password: {api_pass}, API Key: {api_key}")

logger.info('Flask app to be started with below details : \n')
logger.info(f"HOST_IP : {fapp.config['host']}")
logger.info(f"PORT : {fapp.config['port']}")

logger.info(repr(fapp.config['port']))
default_message = "Hello Home, this is a Flask app running on Gunicorn inside Docker!"
print(f"default_message : {default_message}")
@fapp.route('/home', methods=['GET'])
def home():

    return jsonify({"message": default_message})

@fapp.before_request
def log_request_info():
    fapp.logger.info('Headers: %s', request.headers)
    fapp.logger.info('Body: %s', request.get_data())
    print('Body: %s', request.get_data())

@fapp.after_request
def after_request_func(response):
    fapp.logger.info("after_request executing!")
    print("after_request executing!")
    return response

if __name__ == "__main__":
    fapp.run(debug=True, host=fapp.config['host'], port=int(fapp.config['port']))

