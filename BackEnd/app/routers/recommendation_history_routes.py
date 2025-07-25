from flask import Blueprint, request, jsonify
from ..models import db, RecommendationHistory
from flask_jwt_extended import jwt_required, get_jwt_identity

recommendation_history_bp = Blueprint("recommendation_history", __name__)


@recommendation_history_bp.route("/recommendation_history", methods=["POST"])
@jwt_required()
def create_recommendation_history():
    data = request.json
    required_fields = ["resource_id"]
    if not all(data.get(f) for f in required_fields):
        return jsonify(error="Faltan campos obligatorios"), 400
    user_id = int(get_jwt_identity())
    history = RecommendationHistory(
        user_id=user_id,
        resource_id=data["resource_id"],
        status=data.get("status", "pending"),
        feedback=data.get("feedback", ""),
    )
    db.session.add(history)
    db.session.commit()
    return (
        jsonify(
            id=history.id,
            user_id=history.user_id,
            resource_id=history.resource_id,
            status=history.status,
            feedback=history.feedback,
        ),
        201,
    )
