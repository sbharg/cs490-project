from flask import Blueprint, render_template, request, url_for, redirect
from app import db
import app.helpers as help

# Blueprint Configuration
login_bp = Blueprint(
    'login_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@login_bp.route('/adminlanding')
def adminlanding():
    return render_template('adminlanding.html')

@login_bp.route('/userlanding')
def userlanding():
    return render_template('userlanding.html')

@login_bp.route('/')
def index():
    return render_template('index.html')

@login_bp.route('/login', methods = ['POST'])
def login():
   if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      user = help.find_user(db, username)
      if user is None or not help.validate_user_password(password, user.password_hash):
          return "The username or password you enter does not match or is incorrect"
      elif help.validate_user_password(password, user.password_hash):
          if user.user_type == "admin":
              return redirect(url_for('login_bp.adminlanding'))
          elif user.user_type == "user":
              return redirect(url_for('login_bp.userlanding'))
      else:
          return "Something went wrong"