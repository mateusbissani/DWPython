from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__, static_url_path='/static')
app.static_folder = 'static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
app.config['SECRET_KEY'] = 'p128edyiKASkasjnHLhnsdsxp197278619xkjhka'
app.config['UPLOAD_FOLDER'] = 'static/photos_posts'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
# login_manager.login_view = 'homepage'

from src import routes
