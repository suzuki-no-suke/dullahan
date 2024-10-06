from pydantic import BaseModel

from src.datadef.enums.chat_status import ChatStatus

from src.datadef.chat_message import *

import datetime

class ChatShortHistory(BaseModel):
    history_id: str # uuid
    chat_status: ChatStatus
    message_version: str # v1, etc
    title: str
    summary: str
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None

    @classmethod
    def from_db(cls, dbdata):
        return ChatShortHistory(
            history_id=dbdata.id,
            chat_status=dbdata.status,
            message_version=dbdata.message_version,
            title=dbdata.title if dbdata.title else "---",
            summary=dbdata.summary if dbdata.summary else "---",
            created_at=dbdata.created_at if dbdata.created_at else None,
            updated_at=dbdata.updated_at if dbdata.updated_at else None,
        )


class ChatHistory(BaseModel):
    history_id: str # uuid
    chat_status: ChatStatus
    message_version: str # v1, etc
    title: str
    summary: str
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None
    messages: list[Message_v1 | Message_v2]

    @classmethod
    def from_db(cls, dbdata):
        return ChatHistory(
            history_id=dbdata.id,
            chat_status=dbdata.status,
            message_version=dbdata.message_version,
            title=dbdata.title if dbdata.title else "---",
            summary=dbdata.summary if dbdata.summary else "---",
            created_at=dbdata.created_at if dbdata.created_at else None,
            updated_at=dbdata.updated_at if dbdata.updated_at else None,
            messages=[],
        )