from ..Base import Base

import sqlalchemy
from sqlalchemy.schema import Column, Identity
from sqlalchemy.types import Integer, String, DateTime, Text

import enum

class ChatType(enum.Enum):
    Human = 'human'
    UserMeta = 'user_meta'
    Chatbot = 'chatbot'
    BotsMeta = 'bots_meta'

class ChatMessage(Base):
    __tablename__ = 'chat_message'

    pk = Column(Integer, Identity(), primary_key=True)
    id = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)
    type = Column(sqlalchemy.Enum(ChatType), nullable=False)
    botname = Column(String, nullable=False)
    agent = Column(String, nullable=True)
    content = Column(Text)

    def __str__(self) -> str:
        return f"ChatMessage - {self.pk} {self.id} {self.type} {self.botname} @ {self.time.isoformat()} : {self.content[:50]} "
