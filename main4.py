from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

todos = {
    1: {"task": "Task 1", "summary":"Writing Task 1"},
    2: {"task": "Task 2", "summary":"Writing Task 2"},
    3: {"task": "Task 3", "summary":"Writing Task 3"},
}

class ToDo(Resource):
    def get(self,todo_id):
        return todos[todo_id]
    
class ToDoList(Resource):
    def get(self):
        return todos

api.add_resource(ToDo, '/todos/<int:todo_id>')
api.add_resource(ToDoList,'/todos/')

if __name__ == '__main__':
    app.run(debug=True)