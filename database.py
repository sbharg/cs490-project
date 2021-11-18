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
    user2 = add_user('user1', 'pass', 'student')
    user3 = add_user('user2', 'pass', 'student')
    user4 = add_user('user3', 'pass', 'student')

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
    q1 = create_question(q1_text.strip(), course1, "Conditionals", "medi", "operation", False, False, False)

    t1_1 = create_testcase(q1, "\"+\", 5, 3", "8")
    t1_2 = create_testcase(q1, "\"*\", 2, 2", "4")
    t1_3 = create_testcase(q1, "\"-\", 6, 3", "3")
    t1_4 = create_testcase(q1, "\"/\", 10, 5", "2.0")

    q2_text = '''
Write a function named largest that takes one argument:
    1)  lst, a list of numbers

Function largest should iterate through the given list and return the largest value found.

For example, largest([3,7,2,9,8,1]) should return 9.
    '''
    q2 = create_question(q2_text.strip(), course1, "For loops", "medi", "largest", False, False, False)

    t2_1 = create_testcase(q2, "[3,7,2,9,8,1]", "9")
    t2_2 = create_testcase(q2, "[1, 2, 3, 4, 5]", "5")
    t2_3 = create_testcase(q2, "[20, 34, 12, 67, 45, 9]", "67")
    t2_4 = create_testcase(q2, "[78, 32, -90, 100]", "100")

    q3_text = '''
Write a function named sayHello that takes two arguments:
    1)  name, a string
    2)  greeting, a string

Function sayHello should return the greeting and the name as a single string.

For example, sayHello("John", "Howdy") should return "Howdy, John"
    '''
    q3 = create_question(q3_text.strip(), course1, "Strings", "easy", "sayHello", False, False, False)
    t3_1 = create_testcase(q3, '"John", "Howdy"', '"Howdy, John"')
    t3_2 = create_testcase(q3, '"Sam", "Hello"', '"Hello, Sam"')
    t3_3 = create_testcase(q3, '"Ben", "Hi"', '"Hi, Ben"')
    t3_3 = create_testcase(q3, '"Adam", "Salutations"', '"Salutations, Adam"')

    q4_text = '''
Write a function named factorial that takes one argument:
    1) x, an int

Function factorial should return the value x!. Use a for loop in your solution. 

For example, factorial(3) should return 6    
    '''
    q4 = create_question(q4_text.strip(), course1, "For loops", "easy", "factorial", True, False, False)
    t4_1 = create_testcase(q4, "1", "1")
    t4_2 = create_testcase(q4, "2", "2")
    t4_3 = create_testcase(q4, "3", "6")
    t4_3 = create_testcase(q4, "4", "24")

    q5_text = '''
Write a function named fib that that takes one argument:
    1) n, an int greater than 0

Function fib should return the nth Fibonacci number. Use recursion in your solution

For example, fib(3) should return 2 and fib(1) should return 1
    '''
    q5 = create_question(q5_text.strip(), course1, "Recursion", "medi", "fib", False, False, True)
    t5_1 = create_testcase(q5, "1", "1")
    t5_2 = create_testcase(q5, "2", "1")
    t5_3 = create_testcase(q5, "3", "2")
    t5_3 = create_testcase(q5, "5", "5")

    q6_text = '''
Write a function named gcd that takes two arguments:
    1) a, an int
    2) b, an int

Function gcd should return the greatest common divisor of a and b. Use a while loop in your solution

For example, gcd(12, 10) should return 2
    '''
    q6 = create_question(q6_text.strip(), course1, "While Loop", "medi", "gcd", False, True, False)
    t6_1 = create_testcase(q6, "20, 12", "4")
    t6_2 = create_testcase(q6, "9, 5", "1")
    t6_3 = create_testcase(q6, "12, 36", "12")
    t6_3 = create_testcase(q6, "99, 55", "11")

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