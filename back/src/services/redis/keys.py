from enum import StrEnum


class RedisKeys(StrEnum):
    LOGIN_OTP = "otp:login:{email}"

    REGISTER_OTP = "otp:signup:{email}"
    REGISTER_GHOST_USER = "ghost_user:signup:{email}"

    REQUEST_LIMITER = "rate_limit:{key}"
