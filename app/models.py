from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, Integer, String

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True, nullable=False)
    password_hash = Column(String(), nullable=False)
    user_type = Column(String())

    # Many to many relation
    courses = relationship("UserCourse", back_populates="user")
    # One to many relation
    exams = relationship("GradedExamQuestion")

    def __init__(self, username, password_hash, user_type):
        self.username = username
        self.password_hash = password_hash
        self.user_type = user_type
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()

class Course(db.Model):
    __tablename__ = 'courses'
    course_id = Column(Integer, primary_key=True)
    course_name = Column(String(25), unique=True, nullable=False)
    course_password_hash = Column(String(), nullable=False)

    # Many to many relation
    users = relationship("UserCourse", back_populates="course")
    # One to many relation
    questions = relationship("Question")

    def __init__(self, class_name, class_password_hash):
        self.course_name = class_name    
        self.course_password_hash = class_password_hash
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()

    def add_student(self, student):
        self.users.append(student)

class UserCourse(db.Model):
    __tablename__ = 'user_courses'
    user_id = Column(ForeignKey('users.user_id'), primary_key=True)
    course_id = Column(ForeignKey('courses.course_id'), primary_key=True)

    user = relationship("User", back_populates="courses")
    course = relationship("Course", back_populates="users")

    def __init__(self, user_id, course_id):
        self.user_id = user_id    
        self.course_id = course_id
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()

'''
class QuestionCluster(db.Model):
    __tablename__ = 'question_clusters'
    cluster_id = Column(Integer, primary_key=True)
    course_id = Column(ForeignKey('courses.course_id'), nullable=False)
    category = Column(String())
    difficulty = Column(String())

    # One to Many relation
    questions = relationship("Question")
    # Many to Many relation
    exams = relationship("ExamQuestionCluster", back_populates="cluster")

    def __init__(self, course_id, category, difficulty):
        self.course_id = course_id
        self.category = category
        self.difficulty = difficulty
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()
'''

class Question(db.Model):
    __tablename__ = 'questions'
    question_id = Column(Integer, primary_key=True)
    question = Column(String(), nullable=False)
    course_id = Column(ForeignKey('courses.course_id'), nullable=False)
    func_name = Column(String(), nullable=False)

    testcases = relationship("Testcase")
    exams = relationship("ExamQuestions", back_populates="question")
    grades = relationship("GradedExamQuestion")

    def __init__(self, question, course_id, func_name):
        self.question = question
        self.course_id = course_id
        self.func_name = func_name
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()

class Testcase(db.Model):
    __tablename__ = 'testcases'
    testcase_id = Column(Integer, primary_key=True)
    question_id = Column(ForeignKey('questions.question_id'), nullable=False)
    case_input = Column(String(), nullable=False, unique=True)
    input_type = Column(String(), nullable=False)
    case_output = Column(String(), nullable=False, unique=True)
    output_type = Column(String(), nullable=False)

    def __init__(self, question_id, case_input, input_type, case_output, output_type):
        self.question_id = question_id
        self.case_input = case_input
        self.input_type = input_type
        self.case_output = case_output
        self.output_type = output_type
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()

class Exam(db.Model):
    __tablename__ = 'exams'
    exam_id = Column(Integer, primary_key=True)
    course_id = Column(ForeignKey('courses.course_id'), nullable=False)
    visible = Column(Boolean, nullable=False)

    # Many to Many relation
    questions = relationship("ExamQuestions", back_populates="exam")
    # One to Many relation
    graded_exams = relationship("GradedExamQuestion")

    def __init__(self, course_id, visible):
        self.course_id = course_id
        self.visible = visible
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()

class ExamQuestions(db.Model):
    __tablename__ = 'exam_questions'
    exam_id = Column(ForeignKey('exams.exam_id'), primary_key=True)
    question_id = Column(ForeignKey('questions.question_id'), primary_key=True)

    exam = relationship("Exam", back_populates="questions")
    question = relationship("Question", back_populates="exams")

    def __init__(self, exam_id, question_id):
        self.exam_id = exam_id
        self.question_id = question_id
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()

class GradedExamQuestion(db.Model):
    __tablename__ = 'graded_exam_questions'
    exam_id = Column(ForeignKey('exams.exam_id'), primary_key=True)
    question_id = Column(ForeignKey('questions.question_id'), primary_key=True)
    user_id = Column(ForeignKey('users.user_id'), primary_key=True)
    student_answer = Column(String(), nullable=False)
    question_grade = Column(Integer, nullable=False)
    comment = Column(String())

    def __init__(self, exam_id, question_id, user_id, student_answer, question_grade, comment):
        self.exam_id = exam_id
        self.question_id = question_id
        self.user_id = user_id
        self.question_grade = question_grade
        self.student_answer = student_answer
        self.comment = comment
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()
