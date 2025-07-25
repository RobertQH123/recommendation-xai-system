from flask import Blueprint, request, jsonify
from ..models import db, Interaction
from flask_jwt_extended import jwt_required, get_jwt_identity

interaction_bp = Blueprint("interaction", __name__)


@interaction_bp.route("/interactions", methods=["POST"])
@jwt_required()
def create_interaction():
    data = request.json
    required_fields = ["resource_id", "rating"]
    if not all(data.get(f) for f in required_fields):
        return jsonify(error="Faltan campos obligatorios"), 400
    user_id = int(get_jwt_identity())
    interaction = Interaction(
        user_id=user_id,
        resource_id=data["resource_id"],
        rating=data["rating"],
        comment=data.get("comment", ""),
    )
    db.session.add(interaction)
    db.session.commit()
    return (
        jsonify(
            id=interaction.id,
            user_id=interaction.user_id,
            resource_id=interaction.resource_id,
            rating=interaction.rating,
        ),
        201,
    )


@interaction_bp.route("/interactions", methods=["GET"])
@jwt_required()
def get_interactions():
    user_id = int(get_jwt_identity())
    interactions = Interaction.query.filter_by(user_id=user_id).all()
    return (
        jsonify(
            [
                {
                    "id": i.id,
                    "user_id": i.user_id,
                    "resource_id": i.resource_id,
                    "rating": i.rating,
                    "comment": i.comment,
                    "interaction_date": i.interaction_date,
                }
                for i in interactions
            ]
        ),
        200,
    )


@interaction_bp.route("/interactions/<int:interaction_id>", methods=["PUT"])
@jwt_required()
def update_interaction(interaction_id):
    user_id = int(get_jwt_identity())
    interaction = Interaction.query.filter_by(
        id=interaction_id, user_id=user_id
    ).first()
    if not interaction:
        return jsonify(error="Interacción no encontrada"), 404
    data = request.json
    if "rating" in data:
        interaction.rating = data["rating"]
    if "comment" in data:
        interaction.comment = data["comment"]
    db.session.commit()
    return jsonify(message="Interacción actualizada"), 200


@interaction_bp.route("/interactions/<int:interaction_id>", methods=["DELETE"])
@jwt_required()
def delete_interaction(interaction_id):
    user_id = int(get_jwt_identity())
    interaction = Interaction.query.filter_by(
        id=interaction_id, user_id=user_id
    ).first()
    if not interaction:
        return jsonify(error="Interacción no encontrada"), 404
    db.session.delete(interaction)
    db.session.commit()
    return jsonify(message="Interacción eliminada"), 200
