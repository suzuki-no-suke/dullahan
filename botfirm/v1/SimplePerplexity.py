from src.bots_manag.IBots_v1 import BotInterface_v1
from src.datadef.chat_message import Message_v1
from src.datadef.chat_history import ChatHistory
from src.datadef.enums.message_sender_type import MessageSenderType

from src.orm.Base import SQLFactory
from src.orm.tables.table_raw_message import TableRawMessage

from ..helper.llm_call.perplexity import CallPerplexity

import uuid
import os
import datetime

class SimplePerplexity(BotInterface_v1):
    botname = "simple_perplexity"
    agent_name = "simple_perpleity"
    display_name = "Perplexity calling bot"
    useful_when = "Searching web resources with smart LLM and online web retrieval - just once."
    description = """Use perplexity via API, source URLs are all closed.
but it is not only LLM / Web search.

Caution:
  - not multitime chatting supported
"""
    enable_version = ["v1"]

    async def bot_response(self, message: Message_v1, history: ChatHistory) -> list[Message_v1]:
        dbobj = SQLFactory.default_env()
        raw_table = TableRawMessage(dbobj)

        # bots core

        # llm calling
        perp = CallPerplexity(os.getenv("PERPLEXITY_API_KEY"))
        request = perp.history_to_request_v1(message, history)
        
        raw_resp = await perp.call(request)

        perp_resp = perp.response_to_message_v1()
        msg_id = str(uuid.uuid4())
        msg_time = datetime.datetime.now()
        raw_table.insert(msg_id, raw_resp)

        # build response
        perp_resp.message_id = msg_id
        perp_resp.time = msg_time
        perp_resp.sender_type = MessageSenderType.chatbot
        perp_resp.botname = self.botname
        perp_resp.agent = "perplexity"

        return perp_resp




