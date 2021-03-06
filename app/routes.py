from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app, db
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Book
from app.forms import LoginForm, RegistrationForm, AddBookForm

@app.shell_context_processor
def make_shell_context():
  return {'db': db, 'User': User, 'Book': Book}

@app.route('/')
@app.route('/index')
@login_required
def index():
  # return {'test': 'hello json world'} #JSON
  books = [
    {
      'title': "A Space Odessey",
      'author': "Arthur C. Clarke",
    },
    {
      'title': "Ender's game",
      'author': "Orson Scott Card",
    }
  ]
  return render_template('index.html', title='Home', books=books)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('index')
    return redirect(next_page)
  return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Congratulations, you are now a registered user!')
    return redirect(url_for('login'))
  return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
  user = User.query.filter_by(username=username).first_or_404()
  books = [
    {'author': 'test1', 'title': 'Test Book 1'},
    {'author': 'test2', 'title': 'Test Book 2'},
  ]
  return render_template('user.html', user=user, books=books)

@app.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
  if current_user.is_anonymous:
    return redirect(url_for('login'))
  form = AddBookForm()
  if form.validate_on_submit():
    book = Book(author=form.author.data, title=form.title.data, read=form.read.data, user_id=current_user.id)
    db.session.add(book)
    db.session.commit()
     flash('Your book is now added!')
    return redirect(url_for('user', username=current_user.username ))
  return render_template('add_book.html', title='Add A Book', form=form)