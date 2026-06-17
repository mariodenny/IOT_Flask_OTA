import mysql.connector
from flask import current_app

def get_db(app_instance=None):
    """
    Returns a raw MySQL connection using mysql-connector-python.
    """
    app_config = app_instance.config if app_instance else current_app.config
    
    db = mysql.connector.connect(
        host=app_config['MYSQL_HOST'],
        user=app_config['MYSQL_USER'],
        password=app_config['MYSQL_PASSWORD'],
        database=app_config['MYSQL_DATABASE'],
        port=app_config['MYSQL_PORT']
    )
    return db
