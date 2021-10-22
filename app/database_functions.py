from typing import Optional, Union
import flask_sqlalchemy

from app import db
from app.models import User, Chat



def create_new_user(nickname:str, password_hash:str) -> int: 
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


def get_user_by_id(user_id:int) -> Union[User, None, int]:
    ''' Returns User object from db by user_id, None if User not found or -1 if error happened. '''
    try:
        user = User.query.get(user_id)
        return user
    except:
        return -1


def get_user_by_nickname(user_nickname:str) -> Union[User, None, int]:
    ''' Returns User object from db by user_nickname, None if User not found or -1 if error happened. '''
    try:
        user = User.query.filter_by(nickname=user_nickname).first()
        return user
    except:
        return -1


def get_users_by_nickname_query(user_nickname_query:str, offset:int=0, limit:int=-1, order_by_nickname:bool=False) -> Union[flask_sqlalchemy.BaseQuery, int]:
    ''' 
    Returns list of User objects which nicknames starts with user_nickname_query or -1 if error happened. 
    Received list limited by limit parameter. 
    '''
    try:
        found_users = User.query.filter(User.nickname.startswith(user_nickname_query))
        if order_by_nickname:
            found_users = found_users.order_by(User.nickname)
        if limit != -1:
            found_users = found_users.limit(limit)
        if offset:
            found_users = found_users.offset(offset)

        return found_users
    except:

        return -1


def create_new_chat(user1:User, user2:User) -> Union[Chat, int]:
    ''' Creates new Chat and adds it to database. 
    
        Returns: 0 if everything ok and -1 if error happened. 
    '''
    try:
        new_chat = Chat()
        new_chat.users.append(user1)
        new_chat.users.append(user2)
        db.session.add(new_chat)
        db.session.commit()
        return 0
    except:
        db.session.rollback()
        return -1


#def get_chat_by_users_id(user1_id:int, user2_id:int) -> Union[Chat, None, int]:
#    ''' Returns Chat object from db by users ids, None if Chat not found or -1 if error happened. '''
#    try:
#        user = User.query.get(user_id)
#        return user
#    except:
#        return -1
