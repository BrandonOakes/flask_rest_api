import datetime

from argon2 import PasswordHasher
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
from peewee import *
from argon2 import PasswordHasher

import config


DATABASE = SqliteDatabase('todos.sqlite')
HASHER = PasswordHasher()

#create user model

class User(Model):
    """Creates and stores user in database to keep track of
       user specific task
    """
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()


    class Meta():
        """class Meta"""
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password, **kwargs):
        email = email.lower()
        try:
            cls.select().where((cls.email==email)|(cls.username**username)).get()
        except cls.DoesNotExist:
            user = cls(username=username, email=email)
            user.password = user.make_password(password)
            user.save()
            return user
        else:
            raise Exception("Username or email already exist")

    @staticmethod
    def make_password(password):
        return HASHER.hash(password)

    def verify_password(self, password):
        return HASHER.verify(self.password, password)


#create Todo task model

class Todo(Model):
    """Creates and stores todo task entered by a specific username
    """
    # user_id = ForeignKeyField(User)
    task_title = CharField()
    made_by = ForeignKeyField(User, related_name="topic_set")
    # completed = BooleanField(default=False)

    class Meta():
        """class Meta"""
        database= DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Todo], safe=True)
    DATABASE.close()
