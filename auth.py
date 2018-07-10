from flask import g

from flask_httpauth import HTTPBasicAuth

import models

basic_auth = HTTPBasicAuth()
auth = basic_auth

@basic_auth.verify_password
def verify_password(username_or_email, password):
    """verifies that user has not already been created and verifies password"""
    try:
        user = models.User.get((models.User.username == username_or_email) |
                           (models.User.email == username_or_email) )
        if not user.verify_password(password):
            return False
    except models.User.DoesNotExist:
        return False
    else:
        g.user = user
        return True
