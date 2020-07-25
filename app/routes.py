from flask import render_template
from app import app, db
from flask_login import current_user, login_user, logout_user
from app.models import User, Book
from app.forms import LoginForm

@app.shell_context_processor
def make_shell_context():
  return {'db': db, 'User': User, 'Book': Book}

@app.route('/')
@app.route('/index')
def index():
  user = {'username': 'Loquen'}
  # return {'test': 'hello json world'} #JSON
  return render_template('index.html', title='Home', user=user)

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
    return redirect(url_for('index'))
  return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))