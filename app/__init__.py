from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    db.init_app(app)

    with app.app_context():
        #from . import routes
        from .login.login_views import login_bp
        from .student.student_views import student_bp
        from .teacher.teacher_views import teacher_bp
        
        #app.register_blueprint(routes.login_bp)
        app.register_blueprint(login_bp)
        app.register_blueprint(student_bp)
        app.register_blueprint(teacher_bp)
        return app