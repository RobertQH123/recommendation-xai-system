from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def hash_password(password):
    """
    Hashes the password using bcrypt.
    """
    return bcrypt.generate_password_hash(password).decode("utf-8")


def check_password(hashed_password, password):
    """
    Verifies if the hashed password matches the provided password.
    """
    return bcrypt.check_password_hash(hashed_password, password)
