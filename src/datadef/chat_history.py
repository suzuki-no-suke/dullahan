from pydantic import BaseModel

from src.datadef.enums.chat_status import ChatStatus

from src.datadef.chat_message import *

class ChatShortHistory(BaseModel):
    history_id: str # uuid
    chat_status: ChatStatus
    message_version: str # v1, etc
    title: str
    summary: str

    @classmethod
    def from_db(cls, dbdata):
        return ChatShortHistory(
            history_id=dbdata.id,
            chat_status=dbdata.status,
            message_version=dbdata.message_version,
            title=dbdata.title if dbdata.title else "---",
            summary=dbdata.summary if dbdata.summary else "---",
        )


class ChatHistory(BaseModel):
    history_id: str # uuid
    chat_status: ChatStatus
    message_version: str # v1, etc
    title: str
    summary: str
    messages: list[Message_v1 | Message_v2]

    @classmethod
    def from_db(cls, dbdata):
        return ChatHistory(
            history_id=dbdata.id,
            chat_status=dbdata.status,
            message_version=dbdata.message_version,
            title=dbdata.title if dbdata.title else "---",
            summary=dbdata.summary if dbdata.summary else "---",
            messages=[],
        )