import random
import string
from .models import db, User  # Reemplazamos Estudiante por User
from .security import hash_password, check_password
from datetime import timedelta, datetime


def generate_otp():
    return "".join(random.choices(string.digits, k=6))


def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()

    if not user:
        return None

    if not check_password(user.password, password):
        return None

    return user
