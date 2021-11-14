from flask import (
    Blueprint, 
    render_template, 
    request,
    url_for, 
    redirect, 
    g, 
    session, 
)
from app import db
import app.helpers as help
from app.code_tester import CodeTester
from sqlalchemy.exc import IntegrityError
from app.models import Testcase


teacher_bp = Blueprint(
    'teacher_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static'
)

@teacher_bp.before_request
def before_request():
    g.user = None
    g.course = None
    g.question = None
    g.exam = None
    g.submitted_exam = None

    if 'user_id' in session:
        g.user = help.find_user_by_user_id(db, session['user_id'])
    # Temporary hardcode while course enrollment feature is being worked on
    if 'course_id' in session:
        g.course = help.find_course_by_course_id(db, session['course_id'])
    if 'question_id' in session:
        g.question = help.find_question_by_question_id(db, session['question_id'])
    if 'exam_id' in session:
        g.exam = help.find_exam_by_exam_id(db, session['exam_id'])
    if 'submitted_exam' in session:
        g.submitted_exam = help.find_user_exam(db, session['submitted_exam'][0], session['submitted_exam'][1])


@teacher_bp.route('/qbank', methods=['POST', 'GET'])
def qbank_full():
    if g.user == None:
        return redirect(url_for('login_bp.index'))
    return render_template('qeditor_withbank.html')

@teacher_bp.route('/qbank-display', methods=['POST', 'GET'])
def qbank_display():

    try:
        questions = g.course.questions
        questions.sort(key=lambda question: question.question_id)
    except:
        return render_template('qbank.html')

    if len(questions) > 0:
        return render_template('qbank.html', questions = questions)
    else:
        return render_template('qbank.html')

@teacher_bp.route('/filter-questions', methods=['POST'])
def qbank_display_filterd():

    cat = request.form['category']
    diff = request.form['difficulty']
    questions = help.find_questions_by_cat_and_diff(g.course, cat, diff)
    questions.sort(key=lambda question: question.question_id)

    if len(questions) > 0:
        return render_template('qbank.html', questions = questions)
    else:
        return render_template('qbank.html')

@teacher_bp.route('/qbank-edit', methods=['POST'])
def qbank_edit():
    if request.method == 'POST':
        session.pop("question_id", None)
        session['question_id'] = int(request.form["question"])
        # Redirect to question editor page
        return redirect(url_for('teacher_bp.qedit', edit="update"))

@teacher_bp.route('/qedit-new', methods=['GET'])
def qedit_new():
    return render_template('qnew.html')

@teacher_bp.route('/qedit', methods=['POST', 'GET'])
def qedit():
    try:
        testcases = g.question.testcases
    except:
        return render_template('qedit.html')

    if request.method == 'GET':
        if request.args.get('edit') == "new":

            session.pop("question_id", None)
            g.question = None
            return render_template('qedit.html')

        elif request.args.get('edit') == "update":
            if len(testcases) > 0:
                return render_template('qedit.html', testcases = testcases, question = g.question)
            else:
                return render_template('qedit.html', question = g.question)

        else:
            return render_template('qedit.html')

@teacher_bp.route('/submit-question', methods = ['POST'])
def submit_question():
    if request.method == 'POST':
        new_question = True if request.form['question_submit'] == "Add Question" else False
        q_text = request.form['tbox1']
        cat = request.form['category']
        diff = request.form['DifficultyType']
        #points = int(request.form['points'])
        func_name = request.form['func_name']
        constraint = request.form['constraint']
        for_flag = True if constraint == "for_constraint" else False
        while_flag = True if constraint == "while_constraint" else False
        rec_flag = True if constraint == "rec_constraint" else False
        if new_question:
            question = help.create_question(q_text, g.course, cat, diff, func_name, for_flag, while_flag, rec_flag)
            session['question_id'] = question.question_id
            return redirect(url_for('teacher_bp.qedit', edit="update"))
        else:
            g.question.question = q_text
            g.question.func_name = func_name
            g.question.category = cat
            g.question.difficulty = diff
            g.question.for_flag = for_flag
            g.question.while_flag = while_flag
            g.question.rec_flag = rec_flag
            db.session.commit()

            return redirect(url_for('teacher_bp.qbank_display'))

@teacher_bp.route('/add-testcase', methods = ['POST'])
def add_testcase():
    if request.method == 'POST':
        test_inputs = request.form['tbox2']
        test_output = request.form['tbox3']
        tcase = Testcase(g.question.question_id, test_inputs, test_output)
        try:
            tcase.insert()
        except IntegrityError:
            print("Invalid Testcase")

        return render_template('qedit.html', testcases = g.question.testcases, question = g.question)

@teacher_bp.route('/new-exam', methods = ['GET'])
def new_exam():
    if g.user == None:
        return redirect(url_for('login_bp.index'))

    if request.method == 'GET':
        exam = help.create_exam(g.course, False)
        session['exam_id'] = exam.exam_id
        questions = g.course.questions
        questions.sort(key=lambda question: question.question_id)
        return render_template('new_exam.html', question_bank=questions)

@teacher_bp.route('/add-question-to-exam', methods = ['POST'])
def add_question_to_exam():
    if request.method == 'POST':
        question_id = int(request.form["question"])
        q = help.find_question_by_question_id(db, question_id)
        points = request.form['points']
        help.add_question_to_exam(q, g.exam, int(points))
        eqs = help.get_questions_in_exam(g.exam)
        questions = g.course.questions
        questions.sort(key=lambda question: question.question_id)
        return render_template('new_exam.html', exam_questions = g.exam.questions, question_bank=questions)

@teacher_bp.route('/publish-exam', methods = ['POST'])
def publish_exam():
    if request.method == 'POST':
        g.exam.visible = True
        db.session.commit()
        return redirect(url_for('login_bp.adminlanding'))

@teacher_bp.route('/submitted-exams', methods = ['GET'])
def submitted_exams():
    if request.method == 'GET':
        submitted_exams = help.get_submitted_exams(g.course)
        return render_template('submitted_exams.html', submitted_exams=submitted_exams)

@teacher_bp.route('/edit-submission', methods = ['POST'])
def edit_submission():
    if request.method == 'POST':
        session.pop("submitted_exam", None)
        val = request.form["exam"]
        e_id, _, u_id = val.partition(',')
        session['submitted_exam'] = [int(u_id), int(e_id)]
        return redirect(url_for('teacher_bp.exam_review'))

@teacher_bp.route('/exam-review', methods = ['GET'])
def exam_review():
    if request.method == 'GET':
        return render_template('admin_exam_submission_review.html', user_exam = g.submitted_exam, 
                                gradedexamquestions = g.submitted_exam.questions, CodeTester = CodeTester)

@teacher_bp.route('/release_exam', methods = ['POST'])
def release_exam():
    if request.method == 'POST':
        g.submitted_exam.visible = True
        db.session.commit()

        for key, val in request.form.items():
            if key.startswith("student_ans"):
                question_id = int(key[len("student_ans"):])
                geq = help.find_graded_exam_question(db, g.submitted_exam.user_id, question_id, g.submitted_exam.exam_id)
                man_grades = []  
                print(request.form.getlist("man_grade" + str(question_id)))
                for man_grade in request.form.getlist("man_grade" + str(question_id)):
                    man_grades.append(float(man_grade))

                new_com = request.form["teacher_com" + str(question_id)]
                geq.grade = sum(man_grades)
                geq.man_grades = man_grades
                geq.comment = new_com
                db.session.commit()
        return redirect(url_for('login_bp.adminlanding'))