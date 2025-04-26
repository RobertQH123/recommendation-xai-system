from flask import Blueprint, request, jsonify
from .models import db, Estudiante
from .auth import authenticate_estudiante
from .security import hash_password
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

bp = Blueprint("routes", __name__)


@bp.route("/login", methods=["POST"])
def login():
    data = request.json
    estudiante = authenticate_estudiante(data["correo"], data["password"])
    if estudiante:
        access_token = create_access_token(
            identity=str(estudiante.estudiante_id), expires_delta=timedelta(hours=1)
        )
        return jsonify(token=access_token), 200

    return jsonify(error="Credenciales inválidas"), 401


@bp.route("/register", methods=["POST"])
def register():
    data = request.json

    if not data.get("nombre") or not data.get("correo") or not data.get("password"):
        return jsonify(error="Faltan campos obligatorios"), 400

    existing_user = Estudiante.query.filter_by(correo=data["correo"]).first()
    if existing_user:
        return jsonify(error="Correo ya está registrado"), 400

    password_hash = hash_password(data["password"])
    new_estudiante = Estudiante(
        nombre=data["nombre"],
        correo=data["correo"],
        password=password_hash,
        nivel_academico=data.get("nivel_academico", 1),
    )
    db.session.add(new_estudiante)
    db.session.commit()

    return jsonify(message="Estudiante registrado exitosamente"), 201


@bp.route("/estudiantes", methods=["GET"])
@jwt_required()
def get_estudiantes():
    estudiante_id = int(get_jwt_identity())
    estudiante = Estudiante.query.get(estudiante_id)
    return (
        jsonify(
            id=estudiante.estudiante_id,
            nombre=estudiante.nombre,
            correo=estudiante.correo,
            nivel_academico=estudiante.nivel_academico,
        ),
        200,
    )
