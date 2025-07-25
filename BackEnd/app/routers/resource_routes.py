from flask import Blueprint, request, jsonify
from ..models import db, Resource
from flask_jwt_extended import jwt_required

resource_bp = Blueprint("resource", __name__)


@resource_bp.route("/resources", methods=["POST"])
@jwt_required()
def create_resource():
    data = request.json
    required_fields = ["name", "topic_id", "level_id"]
    if not all(data.get(f) for f in required_fields):
        return jsonify(error="Faltan campos obligatorios"), 400
    resource = Resource(
        name=data["name"],
        topic_id=data["topic_id"],
        level_id=data["level_id"],
        description=data.get("description", ""),
        resource_url=data.get("resource_url", ""),
        difficulty=data.get("difficulty", None),
    )
    db.session.add(resource)
    db.session.commit()
    return (
        jsonify(
            id=resource.id,
            name=resource.name,
            topic_id=resource.topic_id,
            level_id=resource.level_id,
        ),
        201,
    )
