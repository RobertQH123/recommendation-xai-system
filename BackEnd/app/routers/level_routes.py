from flask import Blueprint, request, jsonify
from ..models import db, Level
from flask_jwt_extended import jwt_required

level_bp = Blueprint("level", __name__)


@level_bp.route("/levels", methods=["POST"])
@jwt_required()
def create_level():
    data = request.json
    if not data.get("name"):
        return jsonify(error="Falta el nombre del nivel"), 400
    if Level.query.filter_by(name=data["name"]).first():
        return jsonify(error="El nivel ya existe"), 400
    level = Level(name=data["name"])
    db.session.add(level)
    db.session.commit()
    return jsonify(id=level.id, name=level.name), 201


@level_bp.route("/levels", methods=["GET"])
@jwt_required()
def get_levels():
    levels = Level.query.all()
    return jsonify([{"id": l.id, "name": l.name} for l in levels]), 200


@level_bp.route("/levels/<int:level_id>", methods=["PUT"])
@jwt_required()
def update_level(level_id):
    level = Level.query.get(level_id)
    if not level:
        return jsonify(error="Nivel no encontrado"), 404
    data = request.json
    if "name" in data:
        level.name = data["name"]
    db.session.commit()
    return jsonify(message="Nivel actualizado"), 200


@level_bp.route("/levels/<int:level_id>", methods=["DELETE"])
@jwt_required()
def delete_level(level_id):
    level = Level.query.get(level_id)
    if not level:
        return jsonify(error="Nivel no encontrado"), 404
    db.session.delete(level)
    db.session.commit()
    return jsonify(message="Nivel eliminado"), 200
