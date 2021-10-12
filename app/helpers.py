from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash

def find_user(db, username):
    return db.session.query(User).filter(User.username == username).first()

## required later. please make add_user() or something that adds new user.
## even better when there is two functions for new teacher and student

def add_user(username, password, u_type='user'):
    password_hash = generate_password_hash(password)
    user = User(username, password_hash, u_type)
    user.insert()