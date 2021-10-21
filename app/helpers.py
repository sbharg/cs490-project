from app.models import *
from werkzeug.security import generate_password_hash

def find_user_by_username(db, username):
    return db.session.query(User).filter(User.username == username).first()

def find_user_by_user_id(db, user_id):
    return db.session.query(User).filter(User.user_id == user_id).first()

def add_user(username, password, u_type='student'):
    '''
    Creates a new user

    Input:  A string represnting the username of the user, a string representing the 
            plaintext password of the user, and the user type
    Output: A User object
    '''
    password_hash = generate_password_hash(password)
    user = User(username, password_hash, u_type)
    user.insert()
    return user

def create_course(name: str, password: str):
    '''
    Creates a new course

    Input:  A string represnting the name of the course, and a string representing the 
            plaintext password of the course
    Output: A Course object
    '''
    password_hash = generate_password_hash(password)
    course = Course(name, password_hash)
    course.insert()
    return course

def find_course_by_course_id(db, course_id):
    return db.session.query(Course).filter(Course.course_id == course_id).first()

def add_user_to_course(u: User, c: Course):
    '''
    Adds a user to a course

    Input:  A User object and a Course object
    Output: A UserCourse object
    '''
    user_course = UserCourse(u.user_id, c.course_id)
    user_course.insert()
    return user_course

def get_students_in_course(course: Course):
    '''
    Returns all students in a course
    
    Input:  Course object
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
    
    Input:  User object
    Output: List of Course objects
    '''
    courses = []
    for user_course in user.courses:
        courses.append(user_course.course)
    return courses

def create_question(question_text, c: Course, points: int, category: str, difficulty: str, func_name: str):
    '''
    Creates a question

    Input:  A string representing the question, a Course object, an int representing the number
            of points for the question, a string representing the category of the question,
            a string representing the difficulty of the question, and a string representing
            the intended function name
    Output: A Question object
    '''
    question = Question(question_text, c.course_id, points, category, difficulty, func_name)
    question.insert()
    return question

def find_question_by_question_id(db, question_id):
    return db.session.query(Question).filter(Question.question_id == question_id).first()

def create_testcase(q: Question, case_input: str, case_output: str):
    '''
    Creates a testcase for a question
    
    Input:  A Question object, a string represnting the case input, and a string representing the case output
            Case inputs can have the form "x1, x2, x3, ..." if the function has multiple parameters
    Output: A Testcase Object
    '''
    testcase = Testcase(q.question_id, case_input, case_output)
    testcase.insert()
    return testcase

def create_exam(c: Course, visible):
    '''
    Creates an exam for a course

    Input:  A Course object, and a boolean flag to determine if the exam is visible to students
    Output: An Exam object
    '''
    exam = Exam(c.course_id, visible)
    exam.insert()
    return exam

def find_exam_by_exam_id(db, exam_id):
    return db.session.query(Exam).filter(Exam.exam_id == exam_id).first()

def add_question_to_exam(q: Question, e: Exam):
    '''
    Adds a question to an exam

    Input:  A Question object, and an Exam object
    Output: An ExamQuestion object
    '''
    exam_question = ExamQuestion(e.exam_id, q.question_id)
    exam_question.insert()
    return exam_question

def get_questions_in_exam(e: Exam):
    '''
    Returns all questions in an exam

    Input:  Exam object
    Output: List of Questions objects
    '''
    questions = []
    for qs in e.questions:
        questions.append(qs.question)
    return questions

def get_graded_exam(e: Exam, u: User):
    graded_questions = []
    for graded_q in u.exams:
        if graded_q.exam_id == e.exam_id:
            graded_questions.append(graded_q)
    return graded_questions
 
def grade_exam_question(q: Question, ue: UserExam, ans: str, grade: float, comment=""):
    '''
    Grades an exam question for a specified user

    Input:  ExamQuestion object, User object, user answer, grade, and optional comment
            The user answer is expected to be a string, while the grade is expected to be a float
    Output: A GradedExamQuestion object
    '''
    exam_question_grade = GradedExamQuestion(ue.exam_id, q.question_id, ue.user_id, ans, grade, comment)
    exam_question_grade.insert()
    return exam_question_grade

def find_graded_exam_question(db, u_id, q_id, e_id):
    return db.session.query(GradedExamQuestion).filter(GradedExamQuestion.user_id == u_id, 
            GradedExamQuestion.exam_id == e_id, 
            GradedExamQuestion.question_id == q_id).first()

def update_grade(geq: GradedExamQuestion, new_grade: float):
    '''
    Updates the grade for an exam question for a specified user

    Input:  A GradedExamQuestion object and a float for a grade
    Output: Updates the grade in the database
    '''
    geq.grade = new_grade
    db.session.commit()

def update_comment(geq: GradedExamQuestion, new_comment: str):
    '''
    Updates the grade for an exam question for a specified user

    Input:  A GradedExamQuestion object and a string for a comment
    Output: Updates the comment in the database
    '''
    geq.comment = new_comment
    db.session.commit()

def get_user_grade_on_question(u: User, eq: ExamQuestion):
    '''
    Gets a specified user's grade on an exam question

    Input:  A User object and an ExamQuestion object
    Output: A float with the user's grade if it exists, None otherwise 
    '''
    for geq in eq.grades:
        if geq.user_id == u.user_id:
            return geq.grade
        else:
            return None 

def get_submitted_exams(c: Course):
    submitted_exams = []
    for e in c.exams:
        for sub in e.submitted:
            submitted_exams.append(sub)
    return submitted_exams

def find_user_exam(db, u_id, e_id):
    return db.session.query(UserExam).filter(UserExam.user_id == u_id, UserExam.exam_id == e_id).first()

def create_user_exam(u: User, e: Exam, visible=False):
    ue = UserExam(e.exam_id, u.user_id, visible)
    ue.insert()
    return ue

def get_visible_course_exams(c: Course):
    visibleExams = [e for e in c.exams if e.visible == True]
    return visibleExams

def get_visible_user_exams(u: User):
    exams = [e.exam for e in u.submitted_exams if e.visible == True]
    return exams
