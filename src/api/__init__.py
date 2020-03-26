"""Init App"""
from flask import Flask
import os
from flask_jwt_extended import JWTManager

from api.database import db
from api.auth.views import mod as authModule
from api.public.views import mod as publicModule
from api.payees.views import mod as payeesModule
from api.payments.views import mod as paymentsModule
from api.settings.views import mod as settingsModule


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.init_app(app)

        JWTManager(app)

        app.register_blueprint(authModule)
        app.register_blueprint(publicModule)
        app.register_blueprint(payeesModule)
        app.register_blueprint(paymentsModule)
        app.register_blueprint(settingsModule)
        
        return app

