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

    q_cluster = create_question_cluster(course1.course_id)
    q = create_question("Sample Question", q_cluster)
    t = create_testcase(q, "input", "output")
    t = create_testcase(q, "input2", "output2")

    add_user_to_course(user3, course1)
    add_user_to_course(user3, course2)
    add_user_to_course(user4, course1)

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