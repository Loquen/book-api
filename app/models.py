from app import db

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  books = db.relationship('Book', backref='owner', lazy='dynamic')

  def __repr__(self):
    return '<User {}>'.format(self.username)

class Book(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  author = db.Column(db.String(120), index=True)
  title = db.Column(db.String(120), index=True)
  read = db.Column(db.Boolean, index=True, default=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    return '<Book {}>'.format(self.title)