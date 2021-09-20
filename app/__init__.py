from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    db.init_app(app)

    with app.app_context():
        from . import routes
        
        app.register_blueprint(routes.login_bp)
        return app