from random import randint

def generate_otp_code() -> str:
    return str(randint(100000, 999999))
