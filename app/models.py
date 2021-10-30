from app import db
from datetime import datetime



# Many-to-many relationship tables
users_chats = db.Table('users_chats', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'), primary_key=True),
    db.Column('last_read_datetime', db.DateTime)
)


# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(500), nullable=False)

    chats = db.relationship('Chat', secondary=users_chats, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'<User {self.nickname}>'


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    def __repr__(self):
        return f'<Chat {self.id}>'


class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    datetime = db.Column(db.DateTime, default=datetime.now())
    from_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    text = db.Column(db.Text)

    def __repr__(self):
        return f'<Message {self.id} text: {self.text}>'