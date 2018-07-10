# create api that can search task by user?
import json

from flask import abort, Blueprint, jsonify, make_response
from flask_restful import Api, fields, inputs, marshal, marshal_with, Resource, reqparse, url_for

import models

user_fields = {
        'username': fields.String,
}


class UserList(Resource):
    """API that returns list of users"""

    def __init__(self):
        """initiates UserList"""

        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help="username required",
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'email',
            required=True,
            help="email required",
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help="password required",
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'verify_password',
            required=True,
            help="password verification required",
            location=['form', 'json']
        )
        super().__init__()

    def post(self):
        """post request for User"""

        args = self.reqparse.parse_args()
        if args.get('password') == args.get('verify_password'):
            user = models.User.create_user(**args)
            return marshal(user, user_fields), 201
        return make_response(json.dumps({'error': 'Passwords must match'}), 400)

user_api = Blueprint('resources.user', __name__)
api = Api(user_api)
api.add_resource(UserList, '/api/v1/users', endpoint='users')
