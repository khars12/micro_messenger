from typing import Union
from datetime import datetime

import flask_sqlalchemy
from sqlalchemy import func
from sqlalchemy.orm.collections import InstrumentedSet

from app import db
from app.models import User, Chat, Message, users_chats



### Database functions region

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
        user = User.query.filter(func.lower(User.nickname) == func.lower(user_nickname.lower())).first()
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


def get_chat_by_id(chat_id:int) -> Union[Chat, None, int]:
    ''' Returns Chat object from db by chat_id, None if Chat not found or -1 if error happened. '''
    try:
        chat = Chat.query.get(chat_id)
        return chat
    except:
        return -1


def get_chat_by_users(user1:User, user2:User) -> Union[Chat, None, int]:
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


def get_user_chats(user:Union[User, str, int], offset:int=0, limit:int=100) -> Union[list, int]:
    ''' Returns list of dicts with keys 'chat_id', 'last_msg_datetime' for user (user argument may be user id) or -1 if error happened. '''
    try:
        if isinstance(user, (int, str)):
            user = get_user_by_id(int(user))

        request = f'select uc.chat_id, max(m.datetime), uc.has_new_msg, m.id from User u left join users_chats uc on u.id=uc.user_id left join Message m on uc.chat_id=m.chat_id where u.id={user.id} group by uc.chat_id order by max(m.datetime) desc'

        request += f' limit {limit}'
        
        request += f' offset {offset}'

        chats = []

        for row in db.engine.execute(request):
            if not row[1]:
                break

            chat_id = str(row[0])
            has_new_msg = row[2]

            last_message_data = get_message_data(Message.query.get(row[3]))

            chats.append({
                'chat_name': make_chat_name(user, get_chat_by_id(chat_id)),
                'chat_id': chat_id,
                'has_new_msg': has_new_msg,
                **last_message_data
            })

        return chats
    except:
        return -1


def get_message_data(message:Message):
    days_have_passed = datetime.now().toordinal() - message.datetime.toordinal()

    if days_have_passed == 0:
        date = 'today'
    elif days_have_passed == 1:
        date = 'yesterday'
    else:
        date = f"{message.datetime.day}.{message.datetime.month}.{message.datetime.year}"

    time = f'{str(message.datetime.hour).zfill(2)}:{str(message.datetime.minute).zfill(2)}'

    return {
        'from_id': message.from_id,
        'text': message.text,
        'date': date,
        'time': time,
    }


def create_new_message(from_id:int, chat_id:int, text:str) -> Union[Message, int]:
    ''' Creates new Message and adds it to database. 
    
        Returns: Message object if everything ok and -1 if error happened. 
    '''
    try:
        
        new_message = Message(from_id=from_id, chat_id=chat_id, text=text)
        db.session.add(new_message)
        db.session.commit()

        db.engine.execute(users_chats.update().where(users_chats.c.chat_id==chat_id).where(users_chats.c.user_id!=from_id).values(has_new_msg=True))

        return new_message
    except:
        db.session.rollback()
        return -1


def get_messages_by_chat(chat:Chat, offset:int=0, limit:int=-1, update_has_new_msg=True) -> Union[flask_sqlalchemy.BaseQuery, None, int]:
    ''' Returns flask_sqlalchemy.BaseQuery of Message objects which nicknames starts with user_nickname_query or -1 if error happened.  '''
    try:
        chat_messages = Message.query.filter(Message.chat_id == chat.id).order_by(Message.datetime)
        if limit != -1:
            chat_messages = chat_messages.limit(limit)
        if offset:
            chat_messages = chat_messages.offset(offset)

        if offset == 0 and update_has_new_msg:
            db.engine.execute(users_chats.update().where(users_chats.c.chat_id==chat.id).values(has_new_msg=False))

        return chat_messages
    except:
        return -1



### Other functions region

def make_chat_name(current_user:User, chat:Chat) -> str:
    chat_users = chat.users.all()

    if len(chat_users) == 1:
        return chat_users[0].nickname
    
    chat_users.remove(current_user)

    return ', '.join(user.nickname for user in chat_users) 