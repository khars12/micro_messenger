from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import User



def create_new_user(nickname, password):
    ''' Creates new User and adds it to database. '''
    try:
        password_hash = generate_password_hash(password)
        new_user = User(nickname=nickname, password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return 0
    except:
        db.session.rollback()
        return -1
        