from flask import Blueprint, request, jsonify
from ..models import db, Test
from flask_jwt_extended import jwt_required, get_jwt_identity

test_bp = Blueprint("test", __name__)


@test_bp.route("/tests", methods=["POST"])
@jwt_required()
def create_test():
    data = request.json
    required_fields = ["topic_id", "level_id", "score"]
    if not all(data.get(f) for f in required_fields):
        return jsonify(error="Faltan campos obligatorios"), 400
    user_id = int(get_jwt_identity())
    test = Test(
        user_id=user_id,
        topic_id=data["topic_id"],
        level_id=data["level_id"],
        score=data["score"],
    )
    db.session.add(test)
    db.session.commit()
    return (
        jsonify(
            id=test.id,
            user_id=test.user_id,
            topic_id=test.topic_id,
            level_id=test.level_id,
            score=float(test.score),
        ),
        201,
    )
