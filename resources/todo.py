from flask import Blueprint, jsonify, abort


from flask_restful import Api, Resource, reqparse, inputs, fields, marshal, marshal_with, url_for

import models

todo_fields = {
    'id': fields.Integer,
    'task_title': fields.String
}

def task_or_404(task_id):
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
            'task_title',
            required=True,
            help="Title for task required",
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        """returns list of Todo task when request method is GET """

        todos = [marshal(task, todo_fields)
                for task in models.Todo.select()]
        return {'todos': todos}

    def post(self):
        args = self.reqparse.parse_args()
        course = models.Todo.create(**args)
        return course



#create api/v1/todos/<int:id> to get specific todo task

class TodoTask(Resource):
    """Api that returns specific todo task"""

    @marshal_with(todo_fields)
    def get(self, id):
        """returns specific Todo task when request method is GET
           and task id is supplied
        """
        return task_or_404(id)

    @marshal_with(todo_fields)
    def put(self, id):
        """returns specific Todo task when request method is GET
           and task id is supplied
        """

        args = self.reqparse.parse_args()
        query = models.Todo.update(**args).where(models.Todo.id==id)
        query.execute()
        return (models.Todo.get(models.Todo.id==id), 200,
               {'Location': url_for('resources.todo.todotask', id=id)})  #confused by this .todotask? returning a header(body,status code, location)

    def delete(self, id):
        """returns specific Todo task when request method is GET
           and task id is supplied
        """
        query = models.Todo.delete().where(models.Todo.id==id)
        query.execute()
        return '', 204, {'Location': url_for('resources.todo.todo', id=id)}  #confused about where i am sending them to in resources.todo.todo



#make todo_api
todo_api = Blueprint('resource.todo', __name__)
api = Api(todo_api)
#add todo_api resource with api/v1/todos
api.add_resource(TodoList, '/api/v1/todos', endpoint='todos')
api.add_resource(TodoTask, '/api/v1/todos/<int:id>', endpoint="task")
