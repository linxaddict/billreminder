# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, jsonify
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from billreminder import commands
from billreminder.api.bills import BillsView, BillView
from billreminder.extensions import bcrypt, db, login_manager, ma, migrate, api as api_config
from billreminder.http_status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from billreminder.settings import ProdConfig


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)

    register_api_resources()

    register_extensions(app)
    register_blueprints(app)
    register_api_resources()
    register_error_handlers(app)
    register_shell_context(app)
    register_commands(app)

    return app


def register_api_resources():
    api_config.add_resource(BillsView, '/bills')
    api_config.add_resource(BillView, '/bills/<int:bill_id>')


def register_extensions(app):
    from billreminder import api

    """Register Flask extensions."""
    bcrypt.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    api_config.init_app(api.blueprint)

    return None


def register_blueprints(app):
    from billreminder import api
    app.register_blueprint(api.blueprint, url_prefix='/api')


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
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
