from app.models import Testcase
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
from sqlalchemy.sql.functions import func
from sqlalchemy.exc import IntegrityError
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
    g.course = None
    g.question = None
    g.exam = None

    if 'user_id' in session:
        g.user = help.find_user_by_user_id(db, session['user_id'])
    # Temporary hardcode while course enrollment feature is being worked on
    if 'course_id' in session:
        g.course = help.find_course_by_course_id(db, session['course_id'])
    if 'question_id' in session:
        g.question = help.find_question_by_question_id(db, session['question_id'])
    if 'exam_id' in session:
        g.exam = help.find_exam_by_exam_id(db, session['exam_id'])

@login_bp.route('/adminlanding')
def adminlanding():
    if not g.user or g.user.user_type != 'teacher':
        return redirect(url_for('login_bp.index'))
    return render_template('adminlanding.html', loggedperson = g.user.username)

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
            # Temporary hardcode while course enrollment feature is being worked on
            session['course_id'] = help.get_user_courses(user)[0].course_id

            if user.user_type == "teacher":
                return redirect(url_for('login_bp.adminlanding'))
            elif user.user_type == "student":
                return redirect(url_for('login_bp.userlanding'))
        else:
            return "Something went wrong"

@login_bp.route('/questionbank', methods = ['POST', 'GET'])
def question_bank():
    try:
        questions = g.course.questions
    except:
        return render_template('qselector.html')

    if request.method == 'POST':
        session.pop("question_id", None)
        session['question_id'] = int(request.form["question"])
        # Redirect to question editor page
        return redirect(url_for('login_bp.question_editor', edit="update"))

    if len(questions) > 0:
        return render_template('qselector.html', questions = questions)
    else:
        return render_template('qselector.html')

@login_bp.route('/question-editor', methods = ['POST', 'GET'])
def question_editor():
    try:
        testcases = g.question.testcases
    except:
        return render_template('qeditor.html')

    if request.method == 'GET':
        if request.args.get('edit') == "new":
            session.pop("question_id", None)
            g.question = None
            return render_template('qeditor.html')
        else:
            if len(testcases) > 0:
                return render_template('qeditor.html', testcases = testcases, question = g.question)
            else:
                return render_template('qeditor.html', question = g.question)
    elif request.method == 'POST':
        return render_template("ERROR")

@login_bp.route('/submit-question', methods = ['POST'])
def submit_question():
    if request.method == 'POST':
        new_question = True if request.form['question_submit'] == "Add Question" else False
        q_text = request.form['tbox1']
        cat = request.form['category']
        diff = request.form['DifficultyType']
        points = int(request.form['points'])
        func_name = request.form['func_name']
        if new_question:
            question = help.create_question(q_text, g.course, points, cat, diff, func_name)
            session['question_id'] = question.question_id
            return render_template('qeditor.html', question = question)
        else:
            g.question.question = q_text
            g.question.func_name = func_name
            g.question.points = points
            g.question.category = cat
            g.question.difficulty = diff
            db.session.commit()

            return redirect(url_for('login_bp.question_bank'))

@login_bp.route('/add-testcase', methods = ['POST'])
def add_testcase():
    if request.method == 'POST':
        test_inputs = request.form['tbox2']
        test_output = request.form['tbox3']
        tcase = Testcase(g.question.question_id, test_inputs, test_output)
        try:
            tcase.insert()
        except IntegrityError:
            print("Invalid Testcase")

        return render_template('qeditor.html', testcases = g.question.testcases ,question = g.question)


@login_bp.route('/new-exam', methods = ['GET'])
def new_exam():
    '''
    try:
        examq = g.exam.questions
    except:
        return render_template('new_exam.html')
    '''
    if request.method == 'GET':
        exam = help.create_exam(g.course, False)
        session['exam_id'] = exam.exam_id
        # Create a g.exam thing like how we made g.question and g.course
        '''
        if request.args.get('edit') == "new":
            session.pop("exam_id", None)
            g.exam = None
            return render_template('new_exam.html')
        else:
            if len(examq) > 0:
                return render_template('new_exam.html', - , - )
            else:
                return render_template('new_exam.html', question_bank=g.course.questions)
    elif request.method == 'POST':
        return render_template("ERROR")
    '''
@login_bp.route('/add-question-to-exam', methods = ['POST'])
def add_question_to_exam():
    if request.method == 'POST':
        question_id = int(request.form["question"])
        q = help.find_question_by_question_id(db, question_id)
        help.add_question_to_exam(q, g.exam)
        eqs = help.get_questions_in_exam(g.exam)
        return render_template('new_exam.html', exam_questions = eqs, question_bank=g.course.questions)

@login_bp.route('/publish-exam', methods = ['POST'])
def publish_exam():
    if request.method == 'POST':
        g.exam.visible = True
        db.session.commit()
        return redirect(url_for('login_bp.adminlanding'))


#Exam editor not needed atm
'''
@login_bp.route('/exeditor', methods = ['POST', 'GET'])
def exam_edit():
    try:
        questions = g.course.questions
    except:
        return render_template('exampackeditoradmin.html')

    if request.method == 'POST':
        session.pop("question_id", None)
        session['question_id'] = int(request.form["question"])
        # Redirect to exam editor page
        return redirect(url_for('login_bp.exam_update', edit="update"))

    if len(questions) > 0:
        return render_template('exampackeditoradmin.html', questions = questions)
    else:
        return render_template('exampackeditoradmin.html')

@login_bp.route('/exam-edit', methods = ['POST'])
def exam_update():

    return render_template('exampackeditoradmin.html')
'''

#not used atm   
'''
@login_bp.route('/question', methods = ['POST'])
def question():
    if request.method == 'POST':
        courseid = session['course_id']
        cat = request.form['cat']
        diff = request.form['diff']

        cluster = help.create_question_cluster(courseid, cat, diff)

        text = request.form('text')
        func = request.form('func')
        numofQ = request.form('num')

        for x in numofQ:
            question = help.create_question(text, cluster, func)
            #cluster.questions.append(question)
'''