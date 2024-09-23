from pydantic import BaseModel

from src.datadef.enums.chat_status import ChatStatus

from src.datadef.chat_message import *

class ChatShortHistory(BaseModel):
    history_id: str # uuid
    chat_status: ChatStatus
    data_version: str # v1, etc
    title: str
    summary: str

class ChatHistory(BaseModel):
    history_id: str # uuid
    chat_status: ChatStatus
    data_version: str # v1, etc
    title: str
    summary: str
    messages: list[Message_v1 | Message_v2]

