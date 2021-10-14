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
    students = []
    for person in course.users:
        if person.user.user_type == "student":
            students.append(person.user)
    return students

def get_user_courses(user: User):
    courses = []
    for user_course in user.courses:
        courses.append(user_course.course)
    return courses

def create_question_cluster(course_id):
    cluster = QuestionCluster(course_id)
    cluster.insert()
    return cluster

def create_question(question_text, cluster: QuestionCluster):
    question = Question(question_text, cluster.cluster_id)
    question.insert()
    return question

def create_testcase(q: Question, case_input, case_output):
    testcase = Testcase(q.question_id, case_input, case_output)
    testcase.insert()
    return testcase
