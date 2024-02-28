from flask import Flask
from config import Config
from .site.routes import site
from .authentication.routes import auth
from .api.routes import api
from models import User
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db as root_db, login_manager, ma
from flask_cors import CORS
from helpers import JSONEncoder
from flask_login import LoginManager

app = Flask(__name__)
CORS(app)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.signin'  # Specify the view for login, adjust as necessary

@login_manager.user_loader
def load_user(user_id):
    # User loading logic, adjust as necessary
    return User.query.get(user_id)


app._json_encoder = JSONEncoder
app.config.from_object(Config)
root_db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
migrate = Migrate(app, root_db)