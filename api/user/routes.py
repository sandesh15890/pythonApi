from flask import Blueprint
from api import bcrypt, app
from api.user.models import User, UserProfile
from flask import request, jsonify
from api.utils.utils import token_required

users = Blueprint("users", __name__)


@users.route("/add", methods=["POST"])
def CreateUser():
    req = request.get_json()
    uname = req["username"]
    pwd = req["password"]
    mail = req["email"]
    firstname = req["firstname"]
    lastname = req["lastname"]
    address = req["address"]
    mobile = req["mobile"]
    password = bcrypt.generate_password_hash(pwd).decode("utf-8")
    user = User(
        UserName=uname, Email=mail, Password=password, Mobile=mobile, IsActive=True
    )
    user.save()
    userProfile = UserProfile(
        FirstName=firstname, LastName=lastname, Address=address, User_Id=user
    )
    userProfile.save()
    return "Success"


@users.route("/update", methods=["POST"])
def UpdateUserDetails():
    req = request.get_json()
    uname = req["username"]
    pwd = req["password"]
    mail = req["email"]
    firstname = req["firstname"]
    lastname = req["lastname"]
    address = req["address"]
    mobile = req["mobile"]
    user = User.objects(UserName=uname).first()
    password = bcrypt.generate_password_hash(pwd).decode("utf-8")
    user.update(Email=mail, Password=password, Mobile=mobile)
    userProfile = UserProfile.objects(User_Id=user).first()
    userProfile.update(FirstName=firstname, LastName=lastname, Address=address)
    userProfile.reload()
    return dict({"data": userProfile})


@users.route("/GetUser", methods=["GET"])
@token_required
def GetUser():
    users = User.objects().first()
    return dict({"data": users})


@users.route("/DeleteUser", methods=["POST"])
def DeleteUser():
    req = request.get_json()
    uname = req["username"]
    users = User.objects().filter(UserName=uname)
    return dict({"data": users})
