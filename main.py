from flask import Flask
from flask_restful import Api, Resource
from flask.views import MethodView

app = Flask(__name__)
api = Api(app)

names = {"tim" : {"age":19, "gender" : "male"},
		"bill" : {"age":70, "gender" : "male"}}

# class HelloWorld(Resource):
# 	def get(self,name,test):
# 		return {"name": name, "test" : test}

class HelloWorld(Resource):
	def get(self,name):
		return names[name]


	# def post(self):
	# 	return {"data": "Data Posted"}

# api.add_resource(HelloWorld, '/helloworld/<string:name>/<int:test>')
api.add_resource(HelloWorld, '/helloworld/<string:name>')

if __name__ == "__main__":
	app.run(debug=True)

