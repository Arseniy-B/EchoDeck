import bcrypt

class PasswordHelper():
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode("utf-8")
        return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def check_password_strength(password: str):
        if 50 > len(password) > 3:
            return True
        return False

