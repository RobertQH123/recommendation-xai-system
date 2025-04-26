from .db import db
from datetime import datetime


class Estudiante(db.Model):
    __tablename__ = "estudiantes"
    estudiante_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    correo = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255), nullable=False)
    nivel_academico = db.Column(db.Integer)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    ultima_actividad = db.Column(db.DateTime)

    interacciones = db.relationship("Interaccion", backref="estudiante", lazy=True)
    recomendaciones = db.relationship("Recomendacion", backref="estudiante", lazy=True)
    feedbacks = db.relationship("Feedback", backref="estudiante", lazy=True)


class Recurso(db.Model):
    __tablename__ = "recursos"
    recurso_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    descripcion = db.Column(db.Text)
    tipo_recurso = db.Column(db.String(50))
    dificultad = db.Column(db.Integer)
    tema = db.Column(db.String(100))
    url_recurso = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    interacciones = db.relationship("Interaccion", backref="recurso", lazy=True)
    recomendaciones = db.relationship("Recomendacion", backref="recurso", lazy=True)


class Interaccion(db.Model):
    __tablename__ = "interacciones"
    interaccion_id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(
        db.Integer, db.ForeignKey("estudiantes.estudiante_id"), nullable=False
    )
    recurso_id = db.Column(
        db.Integer, db.ForeignKey("recursos.recurso_id"), nullable=False
    )
    tiempo_invertido = db.Column(db.Integer)
    puntuacion = db.Column(db.Integer)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)


class Recomendacion(db.Model):
    __tablename__ = "recomendaciones"
    recomendacion_id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(
        db.Integer, db.ForeignKey("estudiantes.estudiante_id"), nullable=False
    )
    recurso_id = db.Column(
        db.Integer, db.ForeignKey("recursos.recurso_id"), nullable=False
    )
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    explicacion = db.Column(db.Text)

    feedbacks = db.relationship("Feedback", backref="recomendacion", lazy=True)


class Feedback(db.Model):
    __tablename__ = "feedback"
    feedback_id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(
        db.Integer, db.ForeignKey("estudiantes.estudiante_id"), nullable=False
    )
    recomendacion_id = db.Column(
        db.Integer, db.ForeignKey("recomendaciones.recomendacion_id"), nullable=False
    )
    puntuacion = db.Column(db.Integer)
    comentario = db.Column(db.Text)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
