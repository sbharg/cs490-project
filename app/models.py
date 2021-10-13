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
    #exams = relationship("GradedExamQuestion")

    def __init__(self, username, password_hash, user_type):
        self.username = username
        self.password_hash = password_hash
        self.user_type = user_type
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def update(self):
        db.session.commit()

    def add_course(self, course):
        self.courses.append(course)

class Course(db.Model):
    __tablename__ = 'courses'
    course_id = Column(Integer, primary_key=True)
    course_name = Column(String(25), unique=True, nullable=False)
    course_password_hash = Column(String(), nullable=False)

    # Many to many relation
    users = relationship("UserCourse", back_populates="course")

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