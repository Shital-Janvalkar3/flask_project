from flask import Flask, jsonify, request, json, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_marshmallow import Marshmallow


app = Flask(__name__)


db = SQLAlchemy()
ma = Marshmallow()


mysql = MySQL(app)

class User(db.Model): 
    id = db.Column(db.Integer, primary_key= True)
    name =db.Column(db.String(30), nullable= False)
    email = db.Column(db.String(30), nullable = False)
    role = db.Column(db.String(20), nullable=False)


    def __init__ (self, name, email, role):
        self.name =name
        self.email = email
        self.role = role


class UserSchema(ma.Schema):
    class Meta :
        fields = ('id', 'name', 'email', 'role')
        
user_schema = UserSchema()
users_schema = UserSchema(many=True) 
        
        

#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/user"
db.init_app(app)
with app.app_context():
    db.create_all()
    
 
@app.route("/", methods=["GET"])
def index():
    return "<h1>Welcome<h1>"

# Define a route `/hello` that returns the string "Hello, World!" when accessed
@app.route("/hello", methods=['GET'])
def hello():
  return "Hello"   
    
 

 #Implement a route `/new_user` 
@app.route("/new_user", methods=['POST'])
def add_user() :
    _json = request.json
    name = _json['name']
    email = _json['email']
    role = _json['role']
    new_user = User(name=name, email=email, role=role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"Message": "User has been added successfully"})
  





#Implement a route `/users` that retrieves a list of users from a MySQL database
@app.route("/users", methods=['GET'])
def get_user():
    user = []
    data = User.query.all()
    users = users_schema.dump(data)
    return jsonify(users)


#Create a route `/users/<id>` that retrieves a specific user's details from the database 
@app.route("/user/<id>", methods=['GET'])
def user_by_id(id):
    
    if str.isdigit(id) == False:
        return jsonify({"Message" : "the id of the user cannot be string"})
    else:
        data = []
        user = User.query.get(id)
        if user is None:
            return jsonify(f"No product was found")
        data = user_schema.dump(user)
        return jsonify(data)
    
    
    
#DELETE A USER
@app.route("/user/delete/<id>", methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(f"product has been deleted successfully")
    




if __name__ == "__main__":
    app.run(debug=True)
