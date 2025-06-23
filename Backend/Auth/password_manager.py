from werkzeug.security import generate_password_hash, check_password_hash

class PasswordManager:
    def hash_password(self, password: str) -> str:
        return generate_password_hash(password)

    def verify_password(self, password: str, hashed: str) -> bool:
        return check_password_hash(hashed, password)