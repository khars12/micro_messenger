from typing import Union
import flask_sqlalchemy
from sqlalchemy.orm.collections import InstrumentedSet

from app import db
from app.models import User, Chat, Message



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


# TODO def delete_user(id:int) -> int:
#    ''' Deletes user by id. 
#    
#        Returns: 0 if everything ok and -1 if error happened. 
#    '''
#    try:
#        User.query.filter_by(id=id).delete()
#       db.session.commit()
#        return 0
#    except:
#        db.session.rollback()
#        return -1


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
        user = User.query.filter(User.nickname.lower() == user_nickname.lower()).first()
        return user
    except:
        return -1


def get_users_by_nickname_query(user_nickname_query:str, offset:int=0, limit:int=-1, order_by_nickname:bool=False) -> Union[flask_sqlalchemy.BaseQuery, int]:
    ''' 
    Returns flask_sqlalchemy.BaseQuery of User objects which nicknames starts with user_nickname_query or -1 if error happened. 
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
    
        Returns: Chat object if everything ok and -1 if error happened. 
    '''
    try:
        new_chat = Chat()
        new_chat.users.append(user1)
        new_chat.users.append(user2)
        db.session.add(new_chat)
        db.session.commit()
        return new_chat
    except:
        db.session.rollback()
        return -1


def get_chat_by_users_id(user1:User, user2:User) -> Union[Chat, None, int]:
    ''' Returns Chat object from db by two User objects, None if Chat not found or -1 if error happened. '''
    try:
        if user1.id == user2.id:
            for chat in user1.chats:
                if chat.users.count() == 1:
                    return chat
            return None

        chats_for_users = list(InstrumentedSet(user1.chats).intersection(InstrumentedSet(user2.chats)))
        if len(chats_for_users) == 0:
            return None
        return chats_for_users[0]
    except:
        return -1


def create_new_message(from_id:int, chat_id:int, text:str) -> Union[Message, int]:
    ''' Creates new Message and adds it to database. 
    
        Returns: Message object if everything ok and -1 if error happened. 
    '''
    try:
        new_message = Message(from_id=from_id, chat_id=chat_id, text=text)
        db.session.add(new_message)
        db.session.commit()
        return new_message
    except:
        db.session.rollback()
        return -1


def get_messages_by_chat(chat:Chat, offset:int=0, limit:int=-1) -> Union[flask_sqlalchemy.BaseQuery, None, int]:
    ''' Returns Chat object from db by two User objects, None if Chat not found or -1 if error happened. '''
    try:
        chat_messages = Message.query.filter(Message.chat_id == chat.id).order_by(Message.datetime)
        if limit != -1:
            chat_messages = chat_messages.limit(limit)
        if offset:
            chat_messages = chat_messages.offset(offset)

        return chat_messages
    except:
        return -1
