from flask import Blueprint, render_template, jsonify, current_app
from flask import jsonify, request, abort
from app.logging_config import setup_logging
import logging
from app.services.users_service import get_users_service, UsersService
import os, socket
from sqlalchemy import text

# Note 'current_app' stores a reference to the global application object.
# current_app is only valid inside a Flask request context.

bp = Blueprint('routes', __name__)
logger=setup_logging().getLogger(__name__)
logger=logging.getLogger(__name__)

# Decorator
def require_api_key_validation(func):

    def wrapper(*args, **kwargs):
        key = request.headers.get('X-API-KEY') or request.args.get('api_key')
        print (f"Key retrieved : {key}")
        logger.info(f"Key retrieved : {key} / os_env_key : {os.getenv('API_KEY')}")
        print(f"Key retrieved : {key} / os_env_key : {os.getenv('API_KEY')}")
        if key and key == os.getenv("API_KEY") :
            return func(*args, **kwargs)
        else:
            return jsonify({'error': 'Unauthorized'}), 401
    wrapper.__name__ = func.__name__
    return wrapper

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html', message=current_app.config['APP_MESSAGE'])

@bp.route('/health', methods=['GET'])
def health():
    return jsonify(status='healthy'), 200

@bp.route('/users', methods=['GET'])
def get_users():

    user_svc = get_users_service()
    headers = None
    try:
        headers = user_svc.get_headers()
        return render_template("users.html", users=user_svc.get_all_users(), headers=headers)
    except Exception as e:
        print ("Exception occured while fetching user details..")
        print (repr(e))

@bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id: int):

    user_svc = get_users_service()
    try:
        user=user_svc.get_user(user_id)
        if user :
            return ({'status': 'Ok', 'message': 'Success', 'id': repr(user.id), 'name': repr(user.name)}), 200
        else:
             return ({'status': 'Failed', 'message': 'Not found'}),200
    except Exception as e:
        print ("Exception occured while fetching user details..")
        print (repr(e))
        return ({'status': 'Failed', 'message': 'Processing issue'}),500

@bp.route('/user_delete/<int:user_id>', methods=['GET'])
def delete_user(user_id: int):

    user_svc = get_users_service()
    msg=""
    try:
        msg=user_svc.delete_user(user_id)
        return ({'status': f'{msg}'}), 200
    except Exception as e:
        print ("Exception occured while fetching user details..")
        msg="Exception occured while fetching user details."
        print (repr(e))
        return ({'status': f'{msg}'}), 500

@bp.route('/address_delete/<string:zip>', methods=['GET'])
def delete_address(zip: str):

    user_svc = get_users_service()
    msg=""
    try:
        msg=user_svc.delete_address(zip)
        return ({'status': f'{msg}'}), 200
    except Exception as e:
        print ("Exception occured while deleting address details..")
        msg="Exception occured while deleting address details"
        print (repr(e))
        return ({'status': f'{msg}'}), 500

@bp.route('/system', methods=['GET'])
@require_api_key_validation
def get_system():

    return ({'status':'healthy', 'host_name': socket.gethostname(), 'ip_address' : socket.gethostbyname(socket.gethostname())}), 200

@bp.route('/db')
def db_operation_pooling():

    user_svc = get_users_service

    # Simulate a database query
    result = user_svc().db.session.execute(text('SELECT 1')).fetchall()
    return jsonify(result=str(result))

# Simulate a slow endpoint
@bp.route('/slow')
def slow():
    import time
    time.sleep(20)  # to simulate a slow response
    return jsonify(message="This request was slow!")