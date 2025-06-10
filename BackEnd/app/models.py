from .db import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    interactions = db.relationship("Interaction", backref="user", lazy=True)
    tests = db.relationship("Test", backref="user", lazy=True)
    knowledge_profiles = db.relationship("KnowledgeProfile", backref="user", lazy=True)
    recommendations = db.relationship(
        "RecommendationHistory", backref="user", lazy=True
    )


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    topics = db.relationship("Topic", backref="category", lazy=True)


class Topic(db.Model):
    __tablename__ = "topics"
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    resources = db.relationship("Resource", backref="topic", lazy=True)
    tests = db.relationship("Test", backref="topic", lazy=True)
    knowledge_profiles = db.relationship("KnowledgeProfile", backref="topic", lazy=True)


class Level(db.Model):
    __tablename__ = "levels"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    resources = db.relationship("Resource", backref="level", lazy=True)
    tests = db.relationship("Test", backref="level", lazy=True)
    knowledge_profiles = db.relationship("KnowledgeProfile", backref="level", lazy=True)


class Resource(db.Model):
    __tablename__ = "resources"
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey("levels.id"), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    resource_url = db.Column(db.Text)
    difficulty = db.Column(db.Numeric(3, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    interactions = db.relationship("Interaction", backref="resource", lazy=True)
    recommendations = db.relationship(
        "RecommendationHistory", backref="resource", lazy=True
    )


class Interaction(db.Model):
    __tablename__ = "interactions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey("resources.id"), nullable=False)
    interaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)


class Test(db.Model):
    __tablename__ = "tests"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey("levels.id"), nullable=False)
    test_date = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Numeric(4, 2), nullable=False)


class KnowledgeProfile(db.Model):
    __tablename__ = "knowledge_profile"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey("levels.id"), nullable=False)
    mastery_level = db.Column(db.Numeric(3, 2), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


class RecommendationHistory(db.Model):
    __tablename__ = "recommendation_history"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey("resources.id"), nullable=False)
    recommendation_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(
        db.String(50), default="pending"
    )  # 'pending', 'completed', 'dismissed'
    feedback = db.Column(db.Text)
