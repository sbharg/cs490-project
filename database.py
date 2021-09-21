from flask import Flask
from app.models import *
from werkzeug.security import generate_password_hash
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

    admin1 = User('admin', generate_password_hash('admin'), 'admin')
    reg_user = User('user1', generate_password_hash('password'), 'user')
    reg_user2 = User('user2', generate_password_hash('password'), 'user')
    admin1.insert()
    reg_user2.insert()
    reg_user.insert()

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