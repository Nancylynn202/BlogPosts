import hashlib

from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as JWS_Serializer

from .. import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    CONFIRMED_TOKEN_EXPIRY = 300
    GRAVATAR_SERVICE_URI = 'https://secure.gravatar.com/avatar'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    location = db.Column(db.String(100))
    bio = db.Column(db.Text())
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    email = db.Column(db.String(128), unique=True, index=True)
    username = db.Column(db.String(100), index=True, unique=True)
    password_hash = db.Column(db.String(128), nullable=False, unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return f'{self.__class__.__name__}(username={self.username})'

    def avatar(self, size=100, default='identicon'):
        code = hashlib.md5(self.email.encode('utf8')).hexdigest()
        return f'{self.GRAVATAR_SERVICE_URI}/{code}?s={size}&d={default}'

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def password(self):
        raise AttributeError('Attribute password can not be accessed!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def generate_confirmed_token(self):
        serializer = JWS_Serializer(secret_key=current_app.config['SECRET_KEY'],
                                    expires_in=self.CONFIRMED_TOKEN_EXPIRY)
        return serializer.dumps({'confirm': self.id}).decode('utf8')

    def save(self):
        db.session.add(self)
        db.session.commit()