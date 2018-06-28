import datetime

from argon2 import PasswordHasher
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
from peewee import *

import config


DATABASE = SqliteDatabase('todos.sqlite')

#create user model

class User(Model):
    """Creates and stores user in database to keep track of
       user specific task
    """
    username = CharField(unique=True)
    password = CharField()


    class Meta():
        """class Meta"""
        database = DATABASE


#create Todo task model

class Todo(Model):
    """Creates and stores todo task entered by a specific username
    """
    user_id = ForeignKeyField(User)
    task_title = CharField()
    completed = BooleanField(default=False)

    class Meta():
        """class Meta"""
        database= DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Todo], safe=True)
    DATABASE.close()
