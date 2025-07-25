from flask import Blueprint, request, jsonify
from ..models import db, KnowledgeProfile
from flask_jwt_extended import jwt_required, get_jwt_identity

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/knowledge_profiles", methods=["POST"])
@jwt_required()
def create_knowledge_profile():
    data = request.json
    required_fields = ["topic_id", "level_id", "mastery_level"]
    if not all(data.get(f) for f in required_fields):
        return jsonify(error="Faltan campos obligatorios"), 400
    user_id = int(get_jwt_identity())
    profile = KnowledgeProfile(
        user_id=user_id,
        topic_id=data["topic_id"],
        level_id=data["level_id"],
        mastery_level=data["mastery_level"],
    )
    db.session.add(profile)
    db.session.commit()
    return (
        jsonify(
            id=profile.id,
            user_id=profile.user_id,
            topic_id=profile.topic_id,
            level_id=profile.level_id,
            mastery_level=float(profile.mastery_level),
        ),
        201,
    )
