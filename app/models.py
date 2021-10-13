from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True, nullable=False)
    password_hash = Column(String(), nullable=False)
    user_type = Column(String())

    def __init__(self, username, password_hash, user_type):
        self.username = username
        self.password_hash = password_hash
        self.user_type = user_type
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()