from flask import Flask
from logging.config import dictConfig
import yaml
import logging
from app.logging_config import setup_logging
from flask_sqlalchemy import SQLAlchemy
import os,json,glob

from app.routes import bp as routes_bp
from app.services.users_service import get_users_service, UsersService
from app.models.address_schema import *

# Ref-1 : # https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy
# Ref-2 : # https://www.digitalocean.com/community/tutorials/how-to-optimize-flask-performance

# Initialize SQLAlchemy
#db = SQLAlchemy()
logger=None

def create_app(config_path='configuration/config.yaml'):

    mylog=setup_logging()
    #mylog=logging.getLogger(__name__)
    app = Flask(__name__) # Initialize Flask
    logger=mylog.getLogger(__name__)
    logger.setLevel(logging.INFO)

    app_base = os.path.abspath(os.path.dirname(__file__))
    logger.info ('Under init // ' + app_base)

    with open(config_path) as f:
        logger.info(f'About to load config file {config_path}')
        config = yaml.safe_load(f)
        import time
        time.sleep(5)  # to simulate a slow response
        app.config.update(config['flask'])
        app.config['APP_TITLE'] =                       config['app']['title']
        app.config['APP_MESSAGE'] =                     config['app']['message']
        if os.getenv('DB_FILE_LOCATION'):
            db_file_path=os.getenv('DB_FILE_LOCATION')
            if os.path.exists(db_file_path):
                files = glob.glob(os.path.join(f"{db_file_path}/*"))
                for file in files:
                    os.remove(logger.info)
                    logger.info(f"✅ Database file : {f} wiped!")

        app.config['SQLALCHEMY_DATABASE_URI'] =     config['db']['sql_db_uri_memory']
        print (config['db']['sql_db_uri_memory'])
        print (type(app.config['SQLALCHEMY_DATABASE_URI']))
        if 'sql_db_uri_file_global' in config['db']:

            if config['db']['sql_db_uri_file_global'] is not None:
                app.config['SQLALCHEMY_DATABASE_URI'] =     config['db']['sql_db_uri_file_global']
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False
        app.config['DB_DETAILS_JSON'] =                 config['db']['db_details_json']
        #os.environ['SQLALCHEMY_DATABASE_URI'] =         str(app.config['SQLALCHEMY_DATABASE_URI'])
        os.environ['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:" 
        print(str(app.config['SQLALCHEMY_DATABASE_URI']))
        if os.getenv('DB_DETAILS_JSON_FULL_PATH') is not None:
            app.config['DB_DETAILS_JSON_FULL_PATH'] =   os.getenv('DB_DETAILS_JSON_FULL_PATH')
        else:
            app.config['DB_DETAILS_JSON_FULL_PATH'] =   os.path.join('configuration' , app.config['DB_DETAILS_JSON'])

        # Connection pooling allows the application to reuse existing database connections instead of creating new ones for each request. 
        # This reduces the overhead of establishing new connections,
        app.config['SQLALCHEMY_POOL_SIZE'] =            5  # Connection pool size

        logger.info(repr(app.config))
        
    # Initialize SQLAlchemy with flask-app
    #db.init_app(app)

    # Create database tables under 'app' context
    #with app.app_context():
    #    db.create_all()

    # DB popultaion from .json file
    if app.config['DB_DETAILS_JSON_FULL_PATH'] is not None and  os.path.isfile(app.config['DB_DETAILS_JSON_FULL_PATH']):

        with open (app.config['DB_DETAILS_JSON_FULL_PATH']) as f:

            users_data_with_addresses = json.load(f)
            svc=get_users_service()
            try:
                final_list=svc.insert_users(users_data_with_addresses) # Insert all users at once
                if final_list is not None and len(final_list) > 0:
                    logger.info(f"SUCCESS: Loaded from config_file with no of users: {str(len(final_list))}")
                else:
                    logger.warning(f"WARN: in loading user details..")
            except:
                logger.error('Error in loading user details..')
            time.sleep(5)  # to simulate a slow loading

    # Register blueprints / end-points
    app.register_blueprint(routes_bp)
    logger.info("SUCCESS: blueprints end-points registered..")
    return app