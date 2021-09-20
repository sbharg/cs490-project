from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from models import User
import argparse
import helpers

app = Flask(__name__)

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/adminlanding')
def adminlanding():
    return render_template('adminlanding.html')

@app.route('/userlanding')
def userlanding():
    return render_template('userlanding.html')

def configs(env):
    if env == 'dev':
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.ProductionConfig')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dev", action="store_true")
    args = parser.parse_args()
    env = 'dev' if args.dev else 'prod'

    configs(env)
    app.run()