# -*- coding: utf-8 -*-
from flask import Flask, render_template

from spell_check import commands, main
from spell_check.extensions import bootstrap


def create_app(config_object: str = "spell_check.settings") -> Flask:
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    Args:
        config_object (str, optional): The configuration object to use. Defaults to "spell_check.settings".

    Returns:
        Flask: An instance of a Flask application
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    bootstrap.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(main.views.blueprint)
    return None


def register_errorhandlers(app: Flask):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template("errors/{0}.html".format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)


def register_shellcontext(app: Flask):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return None

    app.shell_context_processor(shell_context)


def register_commands(app: Flask):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
    app.cli.add_command(commands.blacken)
