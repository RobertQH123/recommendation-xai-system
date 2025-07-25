from flask import Blueprint, request, jsonify
from ..models import db, Category
from flask_jwt_extended import jwt_required

category_bp = Blueprint("category", __name__)


@category_bp.route("/categories", methods=["POST"])
@jwt_required()
def create_category():
    data = request.json
    if not data.get("name"):
        return jsonify(error="Falta el nombre de la categoría"), 400
    if Category.query.filter_by(name=data["name"]).first():
        return jsonify(error="La categoría ya existe"), 400
    category = Category(name=data["name"])
    db.session.add(category)
    db.session.commit()
    return jsonify(id=category.id, name=category.name), 201
