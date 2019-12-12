from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_material import Material

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
material = Material()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
login_manager.login_message = "Faça o Login para acessar esta página!"

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    material.init_app(app)

    from app.principal.routes import principal
    from app.errors.handlers import errors
    from app.auth.routes import auth
    from app.grupo.routes import grupo
    from app.conta.routes import conta
    from app.setor.routes import setor

    app.register_blueprint(principal)
    app.register_blueprint(errors)
    app.register_blueprint(auth)
    app.register_blueprint(grupo)
    app.register_blueprint(conta)
    app.register_blueprint(setor)

    return app
