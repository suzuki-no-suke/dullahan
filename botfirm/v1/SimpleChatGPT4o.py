from src.bots_manag.IBots_v1 import BotInterface_v1
from src.datadef.chat_message import Message_v1
from src.datadef.chat_history import ChatHistory
from src.datadef.enums.message_sender_type import MessageSenderType

from src.orm.Base import SQLFactory
from src.orm.tables.table_raw_message import TableRawMessage

from ..helper.llm_call.openai_chat import CallOpenAI

import uuid
import os
import datetime

class SimpleChatGPT4o(BotInterface_v1):
    botname = "simple_chatgpt_4o"
    agent_name = "simple_chatgpt_4o"
    display_name = "ChatGPT 4o (full)"
    useful_when = "smartest llm chat engine at 2024"
    description = """Simply use ChatGPT 4o (not mini !) via API."""
    enable_version = ["v1"]

    async def bot_response(self, message: Message_v1, history: ChatHistory) -> list[Message_v1]:
        dbobj = SQLFactory.default_env()
        raw_table = TableRawMessage(dbobj)

        # bots core

        # llm calling
        chatgpt = CallOpenAI(os.getenv("OPENAI_API_KEY"))
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
