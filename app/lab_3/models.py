from flask_login import UserMixin


class User(UserMixin):
    users = {'user': {'password': 'qwerty'},
             'user1': {'password': 'pass1'},
             'user2': {'password': 'pass2'},
             'user3': {'password': 'pass3'},
             'user4': {'password': 'pass4'},
             'user5': {'password': 'pass5'},
             }

    def __init__(self, username):
        self.id = username

    @classmethod
    def validate(cls, username, password):
        user = cls.users.get(username)
        return user and user['password'] == password
