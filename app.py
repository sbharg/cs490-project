from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from models import User
import argparse
import helpers as help

app = Flask(__name__)

db = SQLAlchemy(app)

@app.route('/adminlanding')
def adminlanding():
    return render_template('adminlanding.html')

@app.route('/userlanding')
def userlanding():
    return render_template('userlanding.html')
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['POST'])
def login():
   if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      user = help.find_user(db, username)
      if user is None or not help.validate_user_password(password, user.password_hash):
          return "The username or password you enter does not match or is incorrect"
      elif help.validate_user_password(password, user.password_hash):
          if user.user_type == "admin":
              return redirect(url_for('adminlanding'))
          elif user.user_type == "user":
              return redirect(url_for('userlanding'))
      else:
          return "Something went wrong"

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