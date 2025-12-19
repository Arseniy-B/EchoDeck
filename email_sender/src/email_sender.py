import smtplib
from email.message import EmailMessage

from src.config import config


class EmailSender:
    def __init__(self):
        msg = EmailMessage()
        msg["From"] = config.email.EMAIL_ADDRESS
        self.msg = msg

    async def send_message(self, to: str, text: str):
        breakpoint()
        # self.msg.set_content(text)
        # self.msg["To"] = to 
        # with smtplib.SMTP_SSL(config.email.SMTP_SERVER, 465) as smtp:
        #     smtp.login(config.email.EMAIL_ADDRESS, config.email.EMAIL_PASSWORD)
        #     smtp.send_message(self.msg)


email_sender = EmailSender()
