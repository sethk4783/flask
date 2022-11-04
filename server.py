from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from users.api import UserRegister, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mariadb+mariadbconnector://root:investor_portal@127.0.0.1:3306/investor_portal"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "VFr9thFHOzdCJwbDSFr6p0UlonYmapkw"

jwt = JWTManager(app)
api = Api(app)

@app.before_first_request
def create_tables():
    from db import db
    db.init_app(app)
    db.create_all()

# jwt = JWT(app, authenticate, identity)  # Auto Creates /auth endpoint

api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user')

if __name__ == '__main__':
    app.run(debug=True) # important to mention debug=True
