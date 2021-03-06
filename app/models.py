from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

class User(UserMixin, db.Model):
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

  def avatar(self, size):
    digest = md5(self.email.lower().encode('utf-8')).hexdigest()
    return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

@login.user_loader
def load_user(id):
  return User.query.get(int(id))

  # Users: lo = pass1234, three = pass1234

class Book(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  author = db.Column(db.String(120), index=True)
  title = db.Column(db.String(120), index=True)
  read = db.Column(db.Boolean, index=True, default=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def finished_books(self):
    return Book.query.join()
    # user is current user, and book.read = true

  def new_books(self):
    return Book.query.filter(Book.user_id == self.id)

  def all_books(self):
    return Book.query.filter(Book.user_id == self.id)

  def __repr__(self):
    return '<Book {}>'.format(self.title)