from flask import Blueprint, request, jsonify
from ..models import db, Topic, Category
from flask_jwt_extended import jwt_required

topic_bp = Blueprint("topic", __name__)


@topic_bp.route("/topics", methods=["POST"])
@jwt_required()
def create_topic():
    data = request.json
    if not data.get("name") or not data.get("category_id"):
        return jsonify(error="Faltan campos obligatorios"), 400
    if Topic.query.filter_by(
        name=data["name"], category_id=data["category_id"]
    ).first():
        return jsonify(error="El tema ya existe en esta categoría"), 400
    topic = Topic(
        name=data["name"],
        category_id=data["category_id"],
        description=data.get("description", ""),
    )
    db.session.add(topic)
    db.session.commit()
    return (
        jsonify(
            id=topic.id,
            name=topic.name,
            category_id=topic.category_id,
            description=topic.description,
        ),
        201,
    )
