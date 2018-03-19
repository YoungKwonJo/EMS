from flask import Flask, render_template
from importlib import import_module
from flask_sqlalchemy import SQLAlchemy
from config import config

import os

def register_blueprints(app):

    for module_name in ('base', 'home', 'api'):
        module = import_module('.%s.routes' % (module_name), package=__package__)
        app.register_blueprint(module.blueprint)

def create_app():

    config_name = os.getenv('FLASK_CONFIG') or 'default'
    app = Flask(__name__, static_folder='base/static')

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    register_blueprints(app)

    db.init_app(app)

    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        db.create_all()

    return app

db = SQLAlchemy()
app = create_app()

if __name__ == '__main__':
    app.run(
        host = '0.0.0.0',
        port = 5000,
        threaded = True
        )
