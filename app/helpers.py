from app.models import *
from werkzeug.security import check_password_hash

def find_user(db, username):
    return db.session.query(User).filter(User.username == username).first()

## required later. please make add_user() or something that adds new user.
## even better when there is two functions for new teacher and student

