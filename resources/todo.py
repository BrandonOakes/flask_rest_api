import json

from flask import abort, Blueprint, g, jsonify, make_response
from flask_restful import Api, fields, inputs, marshal, marshal_with, Resource, reqparse, url_for

import models
from auth import auth

todo_fields = {
    'name': fields.String,
    'id': fields.Integer}

def task_or_404(task_id):
    """returns task or 404"""

    try:
        task = models.Todo.get(models.Todo.id==task_id)
    except models.Todo.DoesNotExist:
        abort(404)
    else:
        return task

#create api/v1/todos to get todolist

class TodoList(Resource):
    """API that returns list of Todo task"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help="Name for task required",
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        """returns list of Todo task when request method is GET """

        todos = [marshal(task, todo_fields)
                for task in models.Todo.select()]
        return {'todos': todos} ######## todos


    @marshal_with(todo_fields)
    @auth.login_required
    def post(self):
        """post new task to task list"""

        args = self.reqparse.parse_args()
        todo = models.Todo.create(made_by=g.user,**args)
        return (todo, 201, {'Location': url_for('resources.todos.todo', id=todo.id)})   ######## resources.todos.todo



#create api/v1/todos/<int:id> to get specific todo task

class TodoTask(Resource):
    """Api that returns specific todo task"""

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help="Name for task required",
            location=['form', 'json'])

    @marshal_with(todo_fields)
    def get(self, id):
        """returns specific Todo task when request method is GET
           and task id is supplied
        """
        return task_or_404(id)

    @marshal_with(todo_fields)
    @auth.login_required
    def put(self, id):
        """updates existing todo task"""
        
        args = self.reqparse.parse_args()
        try:
            todo = models.Todo.select().where(models.Todo.made_by==g.user,
                   models.Todo.id==id).get()  #might not work cause ID issue
        except models.Todo.DoesNotExist:
            return make_response(json.dumps({'error':'Task can not be edited'}), 403)
        todo = task_or_404(id)           #might not work cause ID issue
        query = todo.update(**args)
        query.execute()
        return (models.Todo.get(models.Todo.id==id), 200,
               {'Location': url_for('resources.todos.todo', id=id)})  #confused by this .todotask? returning a header(body,status code, location)

    @auth.login_required
    def delete(self, id):
        """returns specific Todo task when request method is GET
           and task id is supplied
        """
        try:
            todo = models.Todo.select().where(models.Todo.made_by==g.user,
                   models.Todo.id==id).get()  #might not work cause ID issue
        except models.Todo.DoesNotExist:
            return make_response(json.dumps({'error':'Task can not be edited'}), 403)
        query = models.Todo.delete().where(models.Todo.id==id)
        query.execute()
        return ('', 204, {'Location': url_for('resources.todos.todo', id=id)})  #confused about where i am sending them to in resources.todo.todo



#make todo_api
todo_api = Blueprint('resource.todo', __name__)
api = Api(todo_api)
#add todo_api resource with api/v1/todos
api.add_resource(TodoList, '/api/v1/todos', endpoint='todos')
api.add_resource(TodoTask, '/api/v1/todos/<int:id>', endpoint="todo")
