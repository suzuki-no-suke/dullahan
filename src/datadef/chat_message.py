from pydantic import BaseModel

import datetime
import uuid

from src.orm.models.chat_message import ChatMessage

from .enums.message_sender_type import MessageSenderType

# chat history 定義

class Message_v1(BaseModel):
    message_id: str = None # uuid
    time: datetime.datetime = None
    sender_type: MessageSenderType
    botname: str
    agent: str
    content: str

    @classmethod
    def build_msg(cls, sender: MessageSenderType, botname: str, agent: str, content: str):
        return Message_v1(
            message_id=str(uuid.uuid4()),
            time=datetime.datetime.now(),
            sender_type=sender,
            botname=botname,
            agent=agent,
            content=content
        )

    @classmethod
    def from_db(cls, db_msg):
        return Message_v1(
            message_id=db_msg.id,
            time=db_msg.time,
            sender_type=db_msg.sender_type,
            botname=db_msg.botname,
            agent=db_msg.agent,
            content=db_msg.content
        )

    def to_db(self):
        return ChatMessage(
            id=self.message_id,
            time=self.time,
            sender_type=self.sender_type,
            botname=self.botname,
            agent=self.botname,
            content=self.content,
            message_version="v1",
        )


class Message_v2(BaseModel):
    message_id: str # uuid
    time: datetime.datetime
    type: MessageSenderType
    botname: str
    agent: str
    content: str
    body: dict