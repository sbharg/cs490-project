from flask import (
    Blueprint, 
    render_template, 
    request,
    url_for, 
    redirect, 
    g, 
    session, 
    flash
)
from app import db
import app.helpers as help
from werkzeug.security import check_password_hash

# Blueprint Configuration
login_bp = Blueprint(
    'login_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static'
)

@login_bp.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        g.user = help.find_user_by_user_id(db, session['user_id'])

@login_bp.route('/adminlanding')
def adminlanding():
    if not g.user or g.user.user_type != 'teacher':
        return redirect(url_for('login_bp.index'))
    return render_template('adminlanding.html')

@login_bp.route('/userlanding')
def userlanding():
    if not g.user or g.user.user_type != 'student':
        return redirect(url_for('login_bp.index'))
    return render_template('userlanding.html')

@login_bp.route('/')
def index():
    return render_template('index.html')

@login_bp.route('/signup')
def signup():
    return render_template('signup.html')

@login_bp.route('/register', methods = ['POST'])
def register():
    if request.method == 'POST':
        who = request.form['options']
        username = request.form['username']
        password = request.form['password']
        user = help.find_user_by_username(db, username)

        if user is None:
            help.add_user(username, password, who)
            flash('You have successfully signed up!')
            return redirect(url_for('login_bp.index'))
        else:
            flash('Username already exists')
            return redirect(url_for('login_bp.signup'))

@login_bp.route('/login', methods = ['POST'])
def login():
    '''
    Post method to handle login requests    
    '''
    if request.method == 'POST':
        session.pop("user_id", None)

        username = request.form['username']
        password = request.form['password']
        user = help.find_user_by_username(db, username)

        if user is None or not check_password_hash(user.password_hash, password):
            flash("Incorrect Credentials")
            return redirect(url_for('login_bp.index'))
        elif check_password_hash(user.password_hash, password):
            session.pop('_flashes', None)
            session['user_id'] = user.user_id
            if user.user_type == "teacher":
                return redirect(url_for('login_bp.adminlanding'))
            elif user.user_type == "student":
                return redirect(url_for('login_bp.userlanding'))
        else:
            return "Something went wrong"
