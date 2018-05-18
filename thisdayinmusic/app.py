from flask import Flask

from thisdayinmusic import auth, api
from thisdayinmusic.extensions import db, jwt, migrate


def create_app(config=None, testing=False, cli=False):
    """Application factory, used to create application
    """
    app = Flask('thisdayinmusic')

    configure_app(app, testing)
    configure_extensions(app, cli)
    register_blueprints(app)

    return app


def configure_app(app, testing=False):
    """set configuration for application
    """
    # default configuration
    app.config.from_object('thisdayinmusic.config')

    if testing is True:
        # override with testing config
        app.config.from_object('thisdayinmusic.configtest')
    else:
        # override with env variable, fail silently if not set
        app.config.from_envvar("THISDAYINMUSIC_CONFIG", silent=True)


def configure_extensions(app, cli):
    """configure flask extensions
    """
    db.init_app(app)
    jwt.init_app(app)

    if cli is True:
        migrate.init_app(app, db)


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)
