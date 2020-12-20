import os
from inventory.models.database import db
from inventory.routes import api
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    # sqlalchemy variables
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(basedir, 'inventory.db')

    # initialize database tables
    db.init_app(app)
    with app.app_context():
        from inventory.models.inventory import Category, Inventory, ItemDetail
        db.create_all()

    # register blueprints
    app.register_blueprint(api, url_prefix='/api')

    return app