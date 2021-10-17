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
    user2 = add_user('teacher2', 'admin', 'teacher')
    user3 = add_user('user1', 'password', 'student')
    user4 = add_user('user2', 'password', 'student')

    course1 = create_course('temp', 'asdf')
    course2 = create_course('temp2', 'asdf')

    #q_cluster = create_question_cluster(course1.course_id, 'temp', 'easy')
    q1 = create_question("Sample Question 1", course1, 10, "arithmetic", "easy")
    q2 = create_question("Sample Question 2", course1, 10, "arithmetic", "easy")
    
    t1 = create_testcase(q1, "1", "6")
    t2 = create_testcase(q1, "3", "8")
    t3 = create_testcase(q1, "4", "9")

    add_user_to_course(user1, course1)
    add_user_to_course(user3, course1)
    add_user_to_course(user4, course1)
    add_user_to_course(user3, course2)

    #print(get_students_in_course(course1))
    #print(get_user_courses(user3))

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