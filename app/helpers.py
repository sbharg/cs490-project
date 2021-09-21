from app.models import *
from werkzeug.security import check_password_hash

def find_user(db, username):
    return db.session.query(User).filter(User.username == username).first()
