from flask import Flask, jsonify
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from billreminder import commands
from billreminder.db.database import BillReminderDb
from billreminder.extensions import bcrypt, db, login_manager, ma, migrate, api_v1 as api_v1_config, admin
from billreminder.http_status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from billreminder.settings import ProdConfig

from billreminder.api.v1 import views
from billreminder.api.v1 import models

from billreminder.api.v1.bills.admin import views as bills_views
from billreminder.api.v1.friends.admin import views as friends_views
from billreminder.api.v1.profile.admin import views as profiles_views
from billreminder.api.v1.reminders.admin import views as reminders_views


def create_app(config_object=ProdConfig):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_shell_context(app)
    register_commands(app)

    add_admin_views()

    return app


def register_extensions(app):
    from billreminder import api

    bcrypt.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    api_v1_config.init_app(api.blueprint)
    admin.init_app(app)

    return None


def add_admin_views():
    views = []

    views += bills_views
    views += friends_views
    views += profiles_views
    views += reminders_views

    for view in views:
        admin.add_view(view)


def register_blueprints(app):
    from billreminder import api
    app.register_blueprint(api.blueprint, url_prefix='/api/v1')


def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def validation_errors_handler(error):
        return jsonify(error.messages), HTTP_400_BAD_REQUEST

    @app.errorhandler(NoResultFound)
    def no_result_handler(error):
        return '404 Not found', HTTP_404_NOT_FOUND


def register_shell_context(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            # 'User': user.models.User
        }

    app.shell_context_processor(shell_context)


def register_commands(app):
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
