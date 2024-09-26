from src.bots_manag.IBots_v1 import BotInterface_v1
from src.datadef.chat_message import Message_v1
from src.datadef.chat_history import ChatHistory
from src.datadef.enums.message_sender_type import MessageSenderType

from src.orm.Base import SQLFactory
from src.orm.tables.table_raw_message import TableRawMessage

from ..helper.llm_call.gemini_generate_only import CallGemini

import uuid
import os
import datetime

class SimpleGemini(BotInterface_v1):
    botname = "simple_gemini_35_flash"
    agent_name = "simple_gemini_35_flash"
    display_name = "Gemini 3.5 Flash"
    useful_when = "Very reasonable price llm provided by Google."
    description = """Simply use Gemini 3.5 Flash with API"""
    enable_version = ["v1"]

    async def bot_response(self, message: Message_v1, history: ChatHistory) -> list[Message_v1]:
        dbobj = SQLFactory.default_env()
        raw_table = TableRawMessage(dbobj)

        # bots core

        # llm calling
        gemini = CallGemini(os.getenv("GEMINI_API_KEY"))
        request = gemini.history_to_request_v1(message, history)
        
        raw_resp = await gemini.call(request)

        bot_resp = gemini.response_to_message_v1(raw_resp)
        msg_id = str(uuid.uuid4())
        msg_time = datetime.datetime.now()
        raw_table.insert(msg_id, raw_resp.to_dict())

        # build response
        bot_resp.message_id = msg_id
        bot_resp.time = msg_time
        bot_resp.sender_type = MessageSenderType.chatbot
        bot_resp.botname = self.botname
        bot_resp.agent = self.agent_name

        return [bot_resp]
