from app import app

@app.route('/')
@app.route('/index')
def index():
  return {'test': 'hello json world'}