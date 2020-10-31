from flask import request, jsonify
from api import app, mail
from flask_mail import Message
import jwt
from datetime import datetime, timedelta
from functools import wraps


def sendMail(user):
    msg = Message("message", sender="noreply@abc.com", recipients=[user.email])
    msg.body = f""" To,
                Good Morning {user.username}                
                """
    mail.send(msg)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get("token")
        if not token:
            return jsonify({"message": "token is missing"}), 403
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
        except:
            return jsonify({"message": "token is invalid"}), 403
        return f(*args, **kwargs)

    return decorated
