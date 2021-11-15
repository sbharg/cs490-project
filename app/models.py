import re
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import user
from sqlalchemy.sql.schema import Column, ForeignKey, ForeignKeyConstraint
from sqlalchemy.sql.sqltypes import ARRAY, Boolean, FLOAT, Integer, String

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
    submitted_exams = relationship("UserExam", back_populates="user")

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
    exams = relationship("Exam")

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

class Question(db.Model):
    __tablename__ = 'questions'
    question_id = Column(Integer, primary_key=True)
    question = Column(String(), nullable=False)
    course_id = Column(ForeignKey('courses.course_id'), nullable=False)
    func_name = Column(String(), nullable=False)
    category = Column(String())
    difficulty = Column(String(4))

    for_flag = Column(Boolean, nullable=False)
    while_flag = Column(Boolean, nullable=False)
    rec_flag = Column(Boolean, nullable=False)

    testcases = relationship("Testcase")
    exams = relationship("ExamQuestion", back_populates="question")

    def __init__(self, question, course_id, category, difficulty, func_name, for_flag, while_flag, rec_flag):
        self.question = question
        self.course_id = course_id
        self.category = category
        self.difficulty = difficulty
        self.func_name = func_name
        self.for_flag = for_flag
        self.while_flag = while_flag
        self.rec_flag = rec_flag
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()

class Testcase(db.Model):
    __tablename__ = 'testcases'
    testcase_id = Column(Integer, primary_key=True)
    question_id = Column(ForeignKey('questions.question_id'), nullable=False)
    case_input = Column(String(), nullable=False)
    #input_type = Column(String(), nullable=False)
    case_output = Column(String(), nullable=False)
    #output_type = Column(String(), nullable=False)

    def __init__(self, question_id, case_input, case_output):
        self.question_id = question_id
        self.case_input = case_input
        #self.input_type = input_type
        self.case_output = case_output
        #self.output_type = output_type
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
    questions = relationship("ExamQuestion", back_populates="exam")
    submitted = relationship("UserExam", back_populates="exam")

    def __init__(self, course_id, visible):
        self.course_id = course_id
        self.visible = visible
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()

class ExamQuestion(db.Model):
    __tablename__ = 'exam_questions'
    exam_id = Column(ForeignKey('exams.exam_id'), primary_key=True)
    question_id = Column(ForeignKey('questions.question_id'), primary_key=True)
    points = Column(Integer, nullable=False)

    exam = relationship("Exam", back_populates="questions")
    question = relationship("Question", back_populates="exams")

    grades = relationship("GradedExamQuestion", viewonly=True, back_populates="exam_question")

    def __init__(self, exam_id, question_id, points):
        self.exam_id = exam_id
        self.question_id = question_id
        self.points = points
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()

class GradedExamQuestion(db.Model):
    __tablename__ = 'graded_exam_questions'
    exam_id = Column(Integer, primary_key=True)
    question_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, primary_key=True)

    student_answer = Column(String(), nullable=False)
    # Proportion of Testcases Passed
    grade = Column(FLOAT, nullable=False)
    man_grades = Column(ARRAY(FLOAT))
    comment = Column(String())

    __table_args__ = (ForeignKeyConstraint(['exam_id', 'question_id'], 
                                           ['exam_questions.exam_id', 'exam_questions.question_id']), 
                    ForeignKeyConstraint(['exam_id', 'user_id'], 
                                        ['user_exams.exam_id', 'user_exams.user_id']),
                    {})
    exam_question = relationship("ExamQuestion", back_populates="grades", uselist=False, viewonly=True)

    def __init__(self, exam_id, question_id, user_id, student_answer, grade, comment, man_grades=None):
        self.exam_id = exam_id
        self.question_id = question_id
        self.user_id = user_id
        self.grade = grade
        self.student_answer = student_answer
        self.comment = comment
        if man_grades != None:
            self.man_grades = man_grades
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()

class UserExam(db.Model):
    __tablename__ = 'user_exams'
    exam_id = Column(ForeignKey('exams.exam_id'), primary_key=True)
    user_id = Column(ForeignKey('users.user_id'), primary_key=True)
    visible = Column(Boolean, nullable=False)

    # One to many relation
    questions = relationship("GradedExamQuestion")

    user = relationship("User", back_populates="submitted_exams")
    exam = relationship("Exam", back_populates="submitted")
    
    def __init__(self, exam_id, user_id, visible):
        self.exam_id = exam_id
        self.user_id = user_id
        self.visible = visible
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()