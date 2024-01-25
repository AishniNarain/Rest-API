#Using HTTP Response Headers, Pagination

from flask import Flask, jsonify, request, make_response, abort
from flask_restful import reqparse
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

class User(db.Model):
    
    id =db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),nullable= False)
    password = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    avatar = db.Column(db.String(50), nullable=True)
    
    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'contact': self.contact,
            'gender' : self.gender,
            'avatar': self.avatar
        }
        
#Adding arguments for update/put method
user_update_args = reqparse.RequestParser()
user_update_args.add_argument("id", type=int, help="Name of the user is required")
user_update_args.add_argument("username", type=str, help="Username of the user")
user_update_args.add_argument("password", type=str, help="Password of the user")
user_update_args.add_argument("contact", type=str, help="Contact of the user")
user_update_args.add_argument("gender", type=str, help="Gender of the user")
user_update_args.add_argument("avatar", type=str, help="Avatar of the user")


#Adding arguments for patch method
user_patch_args = reqparse.RequestParser()
user_patch_args.add_argument("username", type=str, help="Username of the user")
user_patch_args.add_argument("password", type=str, help="Password of the user")

#Get all users
@app.route('/users',methods=['GET'])
def get_all_users():
    users = User.query.all()
    
    if not users:
        return make_response({"message":"No Users Found"})
    
    res = make_response(jsonify([user.json() for user in users]), 200)
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/all_users',methods=['GET'])
def get_users():
    users = User.query.all()
    
    if not users:
        return make_response({"message":"No Users Found"})
    
    result = ([user.json() for user in users])
    
    return jsonify(get_paginated_list(
        result,
        '/users',
        start=request.args.get('start', 1),
        limit=request.args.get('limit', 20)
    ))

#Pagintaion Method

def get_paginated_list(results, url, start, limit):
    start = int(start)
    limit = int(limit)
    count = len(results)
    if count < start or limit < 0:
        abort(404)
    # make response
    obj = {}
    # obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
    # make next url
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
    # finally extract result according to bounds
    obj['results'] = results[(start - 1):(start - 1 + limit)]
    return obj
    

#Get a specific user by it's id
@app.route('/users/<int:id>',methods=['GET'])
def get_user(id):
    users = User.query.filter_by(id=id).first()
    
    if not users:
        return make_response({"error":"User does not exist with this id"})
    
    return make_response({
            'id': users.id,
            'username': users.username,
            'password': users.password,
            'contact': users.contact,
            'gender' : users.gender,
            'avatar': users.avatar
    })

#Creating a new user
@app.route('/users',methods=['POST'])
def create_user():
    data = request.get_json()
    
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return make_response({"message": "Username already exists. Choose a different username"}, 400)
    
    new_user = User(id= data['id'],username= data['username'],password = data['password'],contact = data['contact'],gender = data['gender'])

    db.session.add(new_user)
    db.session.commit()
    return make_response({"message":"User added successfully"}, 201)

# Updating a specific user by it's id
@app.route('/users/update/<int:id>', methods=['PUT'])
def update_user(id):
    args = user_update_args.parse_args()
    result = User.query.filter_by(id=id).first()
    if not result:
        abort(404, message="User doesn't exist, cannot update")

    if args['id']:
        result.id = args['id']
    if args['username']:
        result.username = args['username']
    if args['password']:
        result.password = args['password']
    if args['contact']:
        result.contact = args['contact']
    if args['gender']:
        result.gender = args['gender']
        
    db.session.commit()

    return make_response({"message":"User updated Successfully"}, 201)

# #Deleting a specific user by it's id
@app.route('/users/delete/<int:id>',methods=['DELETE'])
def delete_book(id):
    users = User.query.filter_by(id=id).first()
    
    if not users:
        return {'error':'Book Not Found'}
    
    db.session.delete(users)
    db.session.commit()
    
    return make_response({'data':'User deleted successfully'}, 200)

# Updating a specific user details by it's id
@app.route('/users/patch/<int:id>', methods=['PATCH'])
def patch_user(id):
    args = user_patch_args.parse_args()
    result = User.query.filter_by(id=id).first()
    if not result:
        abort(404, message="User doesn't exist, cannot update")

    if args['username']:
        result.username = args['username']
    if args['password']:
        result.password = args['password']
        
    db.session.commit()

    return make_response({"message":"User details updated successfully"}, 201)

#Uploading avatar of the user
@app.route('/users/<int:id>/upload/avatar', methods=['PATCH'])
def upload_file(id):
    result = User.query.filter_by(id=id).first()
    if not result:
        make_response({"message":"User doesn't exist, cannot upload file"},404)
        
    file = request.files['avatar']
    uniquefilename = str(datetime.now().timestamp()).replace(".","")
    filenamesplit = file.filename.split(".")
    ext = filenamesplit[len(filenamesplit)-1]
    filepath = f"Files/{uniquefilename}.{ext}"
    file.save(filepath)
    
    if file:
        result.avatar = filepath
        db.session.commit()
        return make_response({"message":"File Uploaded Successfully"},201)
    else:
        return make_response({"message":"Cannot Upload File"},202)

if __name__ == '__main__':
    app.run(debug=True)