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

    add_user_to_course(user1, course1)
    add_user_to_course(user2, course1)
    add_user_to_course(user3, course1)
    add_user_to_course(user4, course1)

    q1_text = '''
Write a function named operation that takes three arguments:
    1)  op, a string, e.g., "+","-","*","/"
    2)  a & b, two ints

Function operation should perform the operation specified by op on the two operands a and b and return the correct result.

For example, operation("+", 5, 3) should return 8.
    '''
    q1 = create_question(q1_text.strip(), course1, "Conditionals", "medi", "operation")

    q2_text = '''
Write a function named largest that takes one argument:
    1)  lst, a list of numbers

Function largest should iterate through the given list and return the largest value found.

For example, largest([3,7,2,9,8,1]) should return 9.
    '''
    q2 = create_question(q2_text.strip(), course1, "For loops", "medi", "largest")

    q3_text = '''
Write a function named sayHello that takes two arguments:
    1)  name, a string
    2)  greeting, a string

Function sayHello should return the greeting and the name as a single string.

For example, sayHello("John", "Howdy") should return "Howdy, John"
    '''
    q3 = create_question(q3_text.strip(), course1, "Strings", "easy", "sayHello")

    '''
    q1_text = "Write a function called plus_six that takes an integer x as input and returns x+6"
    q1 = create_question(q1_text, course1, "math", "easy", "plus_six")

    q2_text = "Write a function called factorial that takes an integer x as input and returns x!"
    q2 = create_question(q2_text, course1, "for loop", "easy", "factorial")
    
    q3_text = "Write a function called sub_five that takes an integer x as input and returns x-5"
    q3 = create_question(q3_text, course1, "math", "easy", "sub_five")

    t1_1 = create_testcase(q1, "1", "7")
    t2_1 = create_testcase(q1, "2", "8")
    t3_1 = create_testcase(q1, "3", "9")

    t1_2 = create_testcase(q2, "1", "1")
    #t2_2 = create_testcase(q2, "2", "2")
    t3_2 = create_testcase(q2, "3", "6")

    t1_3 = create_testcase(q3, "10", "5")
    t2_3 = create_testcase(q3, "8", "3")
    t3_3 = create_testcase(q3, "15", "10")

    e = create_exam(course1, True)
    eq1 = add_question_to_exam(q1, e)
    eq2 = add_question_to_exam(q2, e)

    sub_exam = create_user_exam(user2, e)
    ge1 = grade_exam_question(q1, sub_exam, "def plus_six(x):\r return x+6", 0, "")
    ge2 = grade_exam_question(q2, sub_exam, "def factorial(x):\r fact = 1\r for i in range(1, x+1):\r  fact*=i\r return fact", 0, "")

    sub_exam2 = create_user_exam(user3, e)
    ge1 = grade_exam_question(q1, sub_exam2, "bhbcbxzvuoi", 0, "mkmj")
    ge2 = grade_exam_question(q2, sub_exam2, "pokpkvzc", 0, "njn")
    '''

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