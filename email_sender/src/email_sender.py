import smtplib
from email.message import EmailMessage
from src.config import config
import logging


logger = logging.getLogger(__name__)


class EmailSender:
    def __init__(self):
        msg = EmailMessage()
        msg["From"] = config.email.EMAIL_ADDRESS
        self.msg = msg

    async def send_message(self, to: str, text: str):
        self.msg.set_content(text)
        self.msg["To"] = to 
        with smtplib.SMTP_SSL(config.email.SMTP_SERVER, 465) as smtp:
            smtp.login(config.email.EMAIL_ADDRESS, config.email.EMAIL_PASSWORD)
            smtp.send_message(self.msg)
        logger.info("a email letter was sent", extra={"email": to})


email_sender = EmailSender()
