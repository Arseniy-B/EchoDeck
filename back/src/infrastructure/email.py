import smtplib
from email.message import EmailMessage
from src.config import config


class EmailSender:
    def __init__(self):
        msg = EmailMessage()
        msg["From"] = config.email.EMAIL_ADDRESS
        self.msg = msg

    def send_message(self, recipient_address: str, content: str):
        self.msg.set_content(content)
        self.msg["To"] = recipient_address
        with smtplib.SMTP_SSL(config.email.SMTP_SERVER, 465) as smtp:
            smtp.login(config.email.EMAIL_ADDRESS, config.email.EMAIL_PASSWORD)
            smtp.send_message(self.msg)
