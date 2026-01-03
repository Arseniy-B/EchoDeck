import jwt
from src.config import config
from datetime import timedelta, datetime, timezone


USER_ID = int

class JWT:
    @staticmethod
    def encode(
        user_id: USER_ID,
        private_key: str = config.jwt.private_key_path.read_text(),
        algorithm=config.jwt.algorithm,
        expire_minutes: int = config.jwt.access_token_expire_minutes,
    ):
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=expire_minutes)
        to_encode = {"sub": str(user_id), "exp": expire, "iat": now}
        encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
        return encoded

    @staticmethod
    def decode(
        token: str,
        public_key: str = config.jwt.public_key_path.read_text(),
        algorithm: str = config.jwt.algorithm,
    ) -> USER_ID | None:
        try:
            decoded = jwt.decode(token, public_key, algorithms=[algorithm])
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return None
        return int(decoded["sub"])
