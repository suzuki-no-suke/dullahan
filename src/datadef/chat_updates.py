from pydantic import BaseModel

import datetime
import uuid

from src.datadef.chat_message import Message_v1

from src.datadef.enums.message_sender_type import MessageSenderType


# chat の 更新内容通知 (ユーザー送信部も含む)
class ChatDiff_v1(BaseModel):
    history_id: str
    time: datetime.datetime
    messages: list[Message_v1]

    def add_msg(self, sender: MessageSenderType, botname: str, agent: str, content: str):
        self.messages.append(Message_v1(
            message_id=str(uuid.uuid4()),
            time=datetime.datetime.now(),
            sender_type=sender,
            botname=botname,
            agent=agent,
            content=content
        ))

    def add_msg_v1(self, mesg: Message_v1):
        if mesg.message_id is None: mesg.message_id = str(uuid.uuid4())
        if mesg.time is None: mesg.time = datetime.datetime.now()
        self.messages.append(mesg)
