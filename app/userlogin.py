from flask_login import UserMixin



class UserLogin(UserMixin):
    def __init__(self, user):
        self.__user = user

    def get_id(self):
        return str(self.__user.id)

    def is_active(self):
        return self.__user.active

    def get_user(self):
        return self.__user