from flask import Flask
from app.models import *
from werkzeug.security import generate_password_hash
from app.helpers import *
import argparse

app = Flask(__name__)

def init_db(env): 
    if env == 'dev':
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.ProductionConfig')
    db.init_app(app)

    db.drop_all()
    db.create_all()
    
    user1 = add_user('admin', 'admin', 'teacher')
    user2 = add_user('user1', 'password', 'student')
    user3 = add_user('user2', 'password', 'student')
    user4 = add_user('user3', 'password', 'student')

    course1 = create_course('temp', 'asdf')

    q1_text = "Write a function called plus_six that takes an integer x as input and returns x+6"
    q1 = create_question(q1_text, course1, 10, "addition", "easy", "plus_six")

    q2_text = "Write a function called factorial that takes an integer x as input and returns x!"
    q2 = create_question(q2_text, course1, 10, "for loop", "easy", "factorial")

    t1_1 = create_testcase(q1, "1", "6")
    t2_1 = create_testcase(q1, "2", "7")
    t3_1 = create_testcase(q1, "3", "9")

    t1_2 = create_testcase(q2, "1", "1")
    t2_2 = create_testcase(q2, "2", "2")
    t3_2 = create_testcase(q2, "3", "6")

    add_user_to_course(user1, course1)
    add_user_to_course(user2, course1)
    add_user_to_course(user3, course1)
    add_user_to_course(user4, course1)

    e = create_exam(course1, True)
    eq1 = add_question_to_exam(q1, e)
    eq2 = add_question_to_exam(q2, e)

    sub_exam = create_user_exam(user2, e)
    ge1 = grade_exam_question(q1, sub_exam, "asdfasdfasdf", 8.9, "qwerty")
    ge2 = grade_exam_question(q2, sub_exam, "bababhdkbaf", 9.9, "masdf")

    sub_exam2 = create_user_exam(user3, e)
    ge1 = grade_exam_question(q1, sub_exam2, "bhbcbxzvuoi", 8.9, "mkmj")
    ge2 = grade_exam_question(q2, sub_exam2, "pokpkvzc", 9.9, "njn")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prod", action="store_true")
    parser.add_argument("-d", "--dev", action="store_true")
    args = parser.parse_args()

    if args.prod:
        env = 'prod'
    elif args.dev:
        env = 'dev'
    else:
        raise ValueError("Specify which environment to intialize the database on")
    
    with app.app_context():
        init_db(env)


'''
def plus_six(x):\r return x+6

def factorial(x):\r fact = 1\r for i in range(1, x+1):\r  fact*=i\r return fact
'''