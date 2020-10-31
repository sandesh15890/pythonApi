from api import db, app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(db.Document):
    UserId = db.SequenceField()
    UserName = db.StringField(required=True, max_length=20, unique=True)
    Email = db.StringField(required=True, max_length=20, unique=True)
    Password = db.StringField(required=True, max_length=100)
    Mobile = db.StringField(required=True, max_length=15)
    Created_On = db.DateTimeField(default=datetime.now)
    IsActive = db.BooleanField(default=False)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

    # generate account reset token
    def get_reset_token(self, expires_in=1800):
        s = Serializer(app.config["SECRET_KEY"], expires_in)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)


class UserProfile(db.Document):
    UserProfileId = db.SequenceField()
    FirstName = db.StringField(required=True, max_length=20)
    LastName = db.StringField(required=True, max_length=20)
    Address = db.StringField(required=True, max_length=200)
    User_Id = db.LazyReferenceField(User)

    def __repr__(self):
        return f"UserProfile('{self.FirstName}','{ self.LastName }')"
