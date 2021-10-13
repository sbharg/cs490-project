from flask import Flask
from app.models import *
from werkzeug.security import generate_password_hash
from app.helpers import add_user
import argparse

app = Flask(__name__)

def init_db(env): 
    if env == 'dev':
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.ProductionConfig')
    db.init_app(app)

    db.drop_all()
    db.create_all()
    
    add_user('admin', 'admin', 'teacher')
    add_user('teacher2', 'admin', 'teacher')
    add_user('user1', 'password', 'student')
    add_user('user2', 'password', 'student')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prod", action="store_true")
    parser.add_argument("-d", "--dev", action="store_true")
    args = parser.parse_args()

    if args.prod:
        env = 'prod'
    elif args.dev:
        env = 'dev'
    else:
        raise ValueError("Specify which environment to intialize the database on")
    
    with app.app_context():
        init_db(env)