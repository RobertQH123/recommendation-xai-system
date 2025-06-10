from flask import Blueprint, request, jsonify
from ..models import db, User
from ..auth import authenticate_user
from ..security import hash_password
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = authenticate_user(data["email"], data["password"])
    if user:
        access_token = create_access_token(
            identity=str(user.id), expires_delta=timedelta(hours=1)
        )
        return jsonify(token=access_token), 200

    return jsonify(error="Credenciales inválidas"), 401


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    if not data.get("name") or not data.get("email") or not data.get("password"):
        return jsonify(error="Faltan campos obligatorios"), 400

    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify(error="Correo ya registrado"), 400

    password_hash = hash_password(data["password"])
    new_user = User(
        name=data["name"],
        email=data["email"],
        password=password_hash,
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify(message="Usuario registrado exitosamente"), 201


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_user():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    return (
        jsonify(
            id=user.id,
            name=user.name,
            email=user.email,
            registration_date=user.registration_date,
        ),
        200,
    )
