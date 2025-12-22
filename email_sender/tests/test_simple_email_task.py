import pytest
from pydantic import ValidationError
from faststream.rabbit.testing import TestRabbitBroker
from src.main import broker
from src.config import config
from src.email_sender import email_sender
from src.main import simple_email_task
from src.exceptions import TemplateMismatch, TemplateNameNotFound


@pytest.fixture(autouse=True)
def mock_sent_messages(monkeypatch):
    sent_messages = [] 
    async def mock_send(to: str, text: str):
        sent_messages.append({"to": to, "text": text})

    monkeypatch.setattr(email_sender, "send_message", mock_send)

    yield sent_messages
    sent_messages.clear()



@pytest.mark.asyncio
async def test_confirm_email_task_valid_login(mock_sent_messages):
    async with TestRabbitBroker(broker) as test_broker:
        msg = {
            "text_name": "login_confirm_email",
            "to": "user@example.com",
            "payload": {"otp": "123456"}
        }

        await test_broker.publish(
            msg,
            queue=config.rabbit.RABBIT_EMAIL_QUEUE
        )

        assert len(mock_sent_messages) == 1
        simple_email_task.mock.assert_called_once()
        assert mock_sent_messages[0]["to"] == "user@example.com"
        assert "123456" in mock_sent_messages[0]["text"]


@pytest.mark.asyncio
async def test_confirm_email_task_invalid_event_type(mock_sent_messages):
    async with TestRabbitBroker(broker):
        with pytest.raises(TemplateNameNotFound):
            msg = {
                "text_name": "wrong_type",
                "to": "user@example.com",
                "payload": {"otp": "123456"}
            }

            await broker.publish(msg, queue=config.rabbit.RABBIT_EMAIL_QUEUE)

            assert len(mock_sent_messages) == 0


@pytest.mark.asyncio
async def test_confirm_email_task_invalid_payload(mock_sent_messages):
    async with TestRabbitBroker(broker):
        with pytest.raises(TemplateMismatch):
            msg = {
                "text_name": "register_confirm_email",
                "to": "user@example.com",
                "payload": {"wrong_field": "123"}
            }

            await broker.publish(msg, queue=config.rabbit.RABBIT_EMAIL_QUEUE)

            assert len(mock_sent_messages) == 0

@pytest.mark.asyncio
async def test_confirm_email_task_invalid_email(mock_sent_messages):
    async with TestRabbitBroker(broker):
        with pytest.raises(ValidationError):
            msg = {
                "text_name": "register_confirm_email",
                "to": "wrong email",
                "payload": {"otp": "123456"}
            }
            await broker.publish(msg, queue=config.rabbit.RABBIT_EMAIL_QUEUE)
            assert len(mock_sent_messages) == 0

