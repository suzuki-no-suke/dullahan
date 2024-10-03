from ..Base import Base

import sqlalchemy
from sqlalchemy.schema import Column, Identity
from sqlalchemy.types import Integer, String, DateTime

from src.datadef.enums.chat_status import ChatStatus

class ChatHistory(Base):
    __tablename__ = 'chat_history'

    pk = Column(Integer, Identity(), primary_key=True)
    id = Column(String, nullable=False)
    status = Column(sqlalchemy.Enum(ChatStatus), nullable=False)
    title = Column(String, nullable=True)
    summary = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=False))
    message_version = Column(String, nullable=False)

    def diff_dict(self):
        return {
            'status': self.status,
            'title': self.title,
            'summary': self.summary,
            'message_version': self.message_version,
        }

    def __str__(self) -> str:
        return f"ChatHistory - {self.pk} {self.id} {self.message_version} ({self.status}) @ {self.created_at}"
