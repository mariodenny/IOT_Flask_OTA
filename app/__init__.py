import os
from flask import Flask
from config import Config
from flask_login import LoginManager
from app.db import get_db

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Config)

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    login_manager.init_app(app)

    # User loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        
        db = get_db(app)
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        db.close()

        if user_data:
            return User(str(user_data['id']), user_data['username'])
        return None

    # Register blueprints (routes)
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.lessons import bp as lessons_bp
    app.register_blueprint(lessons_bp)

    from app.firmware import bp as firmware_bp
    app.register_blueprint(firmware_bp)

    return app
