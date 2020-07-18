from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  books = db.relationship('Book', backref='owner', lazy='dynamic')

  def __repr__(self):
    return '<User {}>'.format(self.username)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

class Book(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  author = db.Column(db.String(120), index=True)
  title = db.Column(db.String(120), index=True)
  read = db.Column(db.Boolean, index=True, default=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    return '<Book {}>'.format(self.title)