from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

api = Api()
bcrypt = Bcrypt()
login_manager = LoginManager()
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
