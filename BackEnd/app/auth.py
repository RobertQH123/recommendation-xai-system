import random
import string
from .models import db, Estudiante  # Reemplazamos User por Estudiante
from .security import hash_password, check_password
from datetime import timedelta, datetime


def generate_otp():
    return "".join(random.choices(string.digits, k=6))


def authenticate_estudiante(correo, password):
    estudiante = Estudiante.query.filter_by(correo=correo).first()

    if not estudiante:
        return None

    if not check_password(
        estudiante.password, password
    ):  # Tu campo es `password`, no `password_hash`
        return None

    return estudiante
