from flask import Blueprint, Response, request, jsonify, make_response
from api.user.models import User
from api import app, bcrypt, db, mail
from datetime import datetime, timedelta
import jwt

main = Blueprint("main", __name__)


@main.route("/")
def hello_world():
    return "<h1>Welcome to FarmSense!</h1>"


# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt()
# bcrypt.generate_password_hash('admin').decode('utf-8')
# admin  $2b$12$1AVxnruURKia1IBVik2tGuXZemtxpUS89q3Z319fVKdrbqgOW6Fk.
@main.route("/login", methods=["POST"])
def Login():
    req = request.get_json()
    uname = req["username"]
    pwd = req["password"]
    user = User.objects(UserName=uname).first()
    if user:
        if bcrypt.check_password_hash(user.Password, pwd):
            duration = timedelta(minutes=3)
            token = jwt.encode(
                {"user": uname, "exp": datetime.utcnow() + duration},
                app.config["SECRET_KEY"],
            )
            return jsonify({"token": token.decode("utf-8")})
        else:
            return "Invalid Password"
    else:
        return "User Not Found"


@main.route("/logout")
def logout():
    return "Success"
