from flask import Flask, g, jsonify, render_template

import config
import models
from resources.todo import todo_api
from resources.user import user_api

app = Flask(__name__)
app.register_blueprint(todo_api)
app.register_blueprint(user_api)


@app.route('/', methods=['GET', 'POST'])
def my_todos():
    return render_template('index.html')

if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
