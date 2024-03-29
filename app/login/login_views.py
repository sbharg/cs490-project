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
    static_url_path='/login/static'
)

@login_bp.before_request
def before_request():
    g.user = None
    g.course = None
    #g.question = None
    #g.exam = None
    #g.submitted_exam = None

    if 'user_id' in session:
        g.user = help.find_user_by_user_id(db, session['user_id'])
    # Temporary hardcode while course enrollment feature is being worked on
    if 'course_id' in session:
        g.course = help.find_course_by_course_id(db, session['course_id'])
    '''
    if 'question_id' in session:
        g.question = help.find_question_by_question_id(db, session['question_id'])
    if 'exam_id' in session:
        g.exam = help.find_exam_by_exam_id(db, session['exam_id'])
    if 'submitted_exam' in session:
        g.submitted_exam = help.find_user_exam(db, session['submitted_exam'][0], session['submitted_exam'][1])
    '''


@login_bp.route('/adminlanding')
def adminlanding():
    if g.user == None or g.user.user_type != 'teacher':
        return redirect(url_for('login_bp.index'))
    return render_template('adminlanding.html', loggedperson = g.user.username)

@login_bp.route('/userlanding', methods = ['POST', 'GET'])
def userlanding():
    if g.user == None or g.user.user_type != 'student':
        return redirect(url_for('login_bp.index'))
    return render_template('userlanding.html', loggedperson = g.user.username)

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
            # Temporary hardcode while course enrollment feature is being worked on
            session['course_id'] = help.get_user_courses(user)[0].course_id

            if user.user_type == "teacher":
                return redirect(url_for('login_bp.adminlanding'))
            elif user.user_type == "student":
                return redirect(url_for('login_bp.userlanding'))
        else:
            return "Something went wrong"