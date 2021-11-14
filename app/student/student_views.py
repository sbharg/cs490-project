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

student_bp = Blueprint(
    'student_bp', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static'
)

@student_bp.before_request
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

@student_bp.route('/begin-exam', methods = ['POST'])
def begin_exam():
    if request.method == 'POST':
        session.pop("exam_id", None)
        session['exam_id'] = request.form['exam-selection']
        return redirect(url_for('student_bp.exam', exam=session['exam_id']))

@student_bp.route('/exam', methods = ['POST', 'GET'])
def exam():
    if request.method == 'GET':
        for q in g.exam.questions:
            print(q.question)
        return render_template('questionselectorclient.html', exam_id=g.exam.exam_id, questions=g.exam.questions)

@student_bp.route('/submit-answers', methods = ['POST'])
def submit_answers():
    if request.method == 'POST':
        ue = help.create_user_exam(g.user, g.exam)
        for key, val in request.form.items():
            if key.startswith("q_answ"):
                question_id = int(key[6:])
                q_exam = help.find_question_by_exam_id(db, question_id, g.exam.exam_id)
                q = help.find_question_by_question_id(db, question_id)
                ct = CodeTester(val, q.func_name)
                man_grades = []
                num_items = ct.get_total_items(q)
                total_points = q_exam.points
                prop_tpoints_per_item = total_points/num_items
                
                if q.for_flag:
                    proportion, mask = ct.auto_grade(q.testcases, "for")
                elif q.while_flag:
                    proportion, mask = ct.auto_grade(q.testcases, "while")
                elif q.rec_flag:
                    proportion, mask = ct.auto_grade(q.testcases, "recursion")
                else:
                    proportion, mask = ct.auto_grade(q.testcases)

                man_grades = [prop_tpoints_per_item * x for x in mask]
        
                # The grade of the geq should be (prop of testcases passed) * question_points
                geq = help.grade_exam_question(q, ue, val, proportion*total_points)
                geq.man_grades = man_grades
                db.session.commit()

        return redirect(url_for('login_bp.userlanding'))

@student_bp.route('/available-exams', methods = ['GET'])
def available_exams():
    if request.method == 'GET':
        return render_template('user_available_exams_selector.html', exams = help.get_visible_course_exams(g.course))

@student_bp.route('/exam-grades', methods = ['GET'])
def exam_results():
    if request.method == 'GET':
        return render_template('user_exam_result_selector.html', exams = help.get_visible_user_exams(g.user))

@student_bp.route('/view-exam-result', methods = ['POST'])
def view_exam_result():
    if request.method == 'POST':
        examid = int(request.form['exam-selection'])
        session.pop('submitted_exam', None)
        session['submitted_exam'] = [g.user.user_id, examid]
        return redirect(url_for('student_bp.exam_result', exam=examid))

@student_bp.route('/exam_result', methods = ['GET']) #user view exam result
def exam_result():
    if request.method == 'GET':
        return render_template('user_view_exam_result.html', user_exam = g.submitted_exam, 
                                gradedexamquestions = g.submitted_exam.questions, CodeTester = CodeTester)