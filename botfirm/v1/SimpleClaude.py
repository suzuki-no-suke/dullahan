from src.bots_manag.IBots_v1 import BotInterface_v1
from src.datadef.chat_message import Message_v1
from src.datadef.chat_history import ChatHistory
from src.datadef.enums.message_sender_type import MessageSenderType

from src.orm.Base import SQLFactory
from src.orm.tables.table_raw_message import TableRawMessage

from ..helper.llm_call.claude import CallClaude

import uuid
import os
import datetime

class SimpleClaude(BotInterface_v1):
    botname = "simple_claude_35_sonnet"
    agent_name = "simple_claude_35_sonnet"
    display_name = "Claude 3.5 sonnet"
    useful_when = "very stable and challenging llm"
    description = """Simply use Claude 3.5 sonnet  via API."""
    enable_version = ["v1"]

    async def bot_response(self, message: Message_v1, history: ChatHistory) -> list[Message_v1]:
        dbobj = SQLFactory.default_env()
        raw_table = TableRawMessage(dbobj)

        # bots core

        # llm calling
        chatgpt = CallClaude(os.getenv("ANTHOROPIC_API_KEY"))
        request = chatgpt.history_to_request_v1(message, history)
        
        raw_resp = await chatgpt.call(request)

        resp = chatgpt.response_to_message_v1(raw_resp)
        msg_id = str(uuid.uuid4())
        msg_time = datetime.datetime.now()
        raw_table.insert(msg_id, raw_resp.to_dict())

        # build response
        resp.message_id = msg_id
        resp.time = msg_time
        resp.sender_type = MessageSenderType.chatbot
        resp.botname = self.botname
        resp.agent = self.agent_name

        return [resp]
