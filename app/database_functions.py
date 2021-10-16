from typing import Optional, Union

from app import db
from app.models import User



def create_new_user(nickname: str, password_hash: str) -> int: 
    ''' Creates new User and adds it to database. 
    
        Returns: 0 if everything ok and -1 if error happened. 
    '''
    try:
        new_user = User(nickname=nickname, password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return 0
    except:
        db.session.rollback()
        return -1


def get_user_by_id(user_id: int) -> Union[User, None, int]:
    ''' Returns User object from db by user_id, None if User not found or -1 if error happened. '''
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        return user
    except:
        return -1


def get_user_by_nickname(user_nickname: str) -> Union[User, None, int]:
    ''' Returns User object from db by user_nickname, None if User not found or -1 if error happened. '''
    try:
        user = User.query.filter_by(nickname=user_nickname).first()
        return user
    except:
        return -1