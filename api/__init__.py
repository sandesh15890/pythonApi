from flask import Flask, Response
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_mongoengine import MongoEngine
from datetime import timedelta

app = Flask(__name__)
app.config["SECRET_KEY"] = "664f9413c918fe86e80591af37b91ca5"
app.config["MONGODB_SETTINGS"] = {
    "DB": "FarmSense",
    "host": "mongodb://sa:farmSense%402020@localhost:27017/FarmSense",
    "port": 27017,
}
db = MongoEngine(app)
bcrypt = Bcrypt(app)
app.config["REMEMBER_COOKIE_NAME"] = "userCookie"
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=0, seconds=5)
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "abc.com"
app.config["MAIL_PASSWORD"] = "abc"
mail = Mail(app)

from api.user.routes import users
from api.main.routes import main

app.register_blueprint(users)
app.register_blueprint(main)
