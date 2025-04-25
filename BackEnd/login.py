from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from datetime import timedelta

app = Flask(__name__)

# Configuración
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://user:admin@localhost:5432/tesis"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "asdcfeasd"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


# Modelos
class Estudiante(db.Model):
    __tablename__ = "estudiantes"
    estudiante_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    nivel_academico = db.Column(db.Integer, nullable=False)
    fecha_registro = db.Column(db.DateTime)
    ultima_actividad = db.Column(db.DateTime)
    password_hash = db.Column(db.String(255), nullable=False)


# Rutas de autenticación
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    nuevo_estudiante = Estudiante(
        nombre=data["nombre"],
        correo=data["correo"],
        nivel_academico=data["nivel_academico"],
        password_hash=hashed_pw,
    )
    db.session.add(nuevo_estudiante)
    db.session.commit()
    return jsonify(message="Registro exitoso"), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    estudiante = Estudiante.query.filter_by(correo=data["correo"]).first()
    if estudiante and bcrypt.check_password_hash(
        estudiante.password_hash, data["password"]
    ):
        access_token = create_access_token(identity=estudiante.estudiante_id)
        return jsonify(access_token=access_token)
    return jsonify(message="Credenciales inválidas"), 401


@app.route("/perfil", methods=["GET"])
@jwt_required()
def perfil():
    estudiante_id = get_jwt_identity()
    estudiante = Estudiante.query.get(estudiante_id)
    return jsonify(
        id=estudiante.estudiante_id,
        nombre=estudiante.nombre,
        correo=estudiante.correo,
        nivel_academico=estudiante.nivel_academico,
    )


if __name__ == "__main__":
    app.run(debug=True)
