from flask import Flask, jsonify
from .db import db  # Asegúrate de importar el objeto db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
jwt = JWTManager()

limiter = Limiter(get_remote_address)


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    @app.errorhandler(429)
    def ratelimit_error(e):
        return (
            jsonify(
                error="Too many requests",
                message="Excede el limite de peticiones",
            ),
            429,
        )

    jwt = JWTManager(app)
    db.init_app(app)  # Inicializa la base de datos con la app
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate = Migrate(app, db)

    CORS(app, resources={r"/*": {"origins": "*"}})

    limiter.init_app(app)

    with app.app_context():
        from .routers import auth_bp, rec_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(rec_bp)
        db.create_all()  # Crea las tablas al iniciar la app

    return app
