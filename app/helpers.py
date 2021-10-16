from app.models import *
from werkzeug.security import generate_password_hash

def find_user_by_username(db, username):
    return db.session.query(User).filter(User.username == username).first()

def find_user_by_user_id(db, user_id):
    return db.session.query(User).filter(User.user_id == user_id).first()

def add_user(username, password, u_type='student'):
    password_hash = generate_password_hash(password)
    user = User(username, password_hash, u_type)
    user.insert()
    return user

def create_course(name, password):
    password_hash = generate_password_hash(password)
    course = Course(name, password_hash)
    course.insert()
    return course

def find_course_by_course_id(db, course_id):
    return db.session.query(Course).filter(Course.course_id == course_id).first()

def add_user_to_course(user: User, course: Course):
    user_course = UserCourse(user.user_id, course.course_id)
    user_course.insert()

def get_students_in_course(course: Course):
    '''
    Returns all students in a course
    
    Input: Course object
    Output: List of Student objects
    '''
    students = []
    for person in course.users:
        if person.user.user_type == "student":
            students.append(person.user)
    return students

def get_user_courses(user: User):
    '''
    Returns all courses a user is registered in
    
    Input: User object
    Output: List of Course objects
    '''
    courses = []
    for user_course in user.courses:
        courses.append(user_course.course)
    return courses

def create_question(question_text, course: Course, func_name):
    question = Question(question_text, course.course_id, func_name)
    question.insert()
    return question

def create_testcase(q: Question, case_input, input_type, case_output, output_type):
    testcase = Testcase(q.question_id, case_input, input_type, case_output, output_type)
    testcase.insert()
    return testcase

def create_exam(course_id, visible):
    exam = Exam(course_id, visible)
    exam.insert()
    return exam

def get_questions_in_exam(e: Exam):
    '''
    Returns all questions in an exam

    Input: Exam object
    Output: List of Questions objects
    '''
    questions = []
    for qs in e.questions:
        questions.append(qs.question)
    return questions
