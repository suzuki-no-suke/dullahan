from ..Base import Base

import sqlalchemy
from sqlalchemy.schema import Column, Identity
from sqlalchemy.types import Integer, String, DateTime, Text

from src.datadef.enums.message_sender_type import MessageSenderType

import uuid
import datetime

class ChatMessage(Base):
    __tablename__ = 'chat_message'

    pk = Column(Integer, Identity(), primary_key=True)
    id = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)
    sender_type = Column(sqlalchemy.Enum(MessageSenderType), nullable=False)
    botname = Column(String, nullable=False)
    agent = Column(String, nullable=True)
    content = Column(Text)
    message_version = Column(Text, nullable=False)

    def diff_dict(self):
        return {
            'time': self.time,
            'sender_type': self.sender_type,
            'botname': self.botname,
            'agent': self.agent,
            'content': self.content,
            'message_version': self.message_version
        }

    @classmethod
    def build_msg_v1(sender: MessageSenderType, botname: str, agent: str, content: str):
        return ChatMessage(
            id=str(uuid.uuid4()),
            time=datetime.datetime.now(),
            sender_type=sender,
            botname=botname,
            agent=agent,
            content=content,
            message_version="v1",
        )

    def __str__(self) -> str:
        return f"ChatMessage - {self.pk} {self.id} {self.sender_type} {self.botname} {self.message_version} @ {self.time.isoformat()} : {self.content[:50]} "
