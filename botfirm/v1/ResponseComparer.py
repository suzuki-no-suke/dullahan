from src.bots_manag.IBots_v1 import BotInterface_v1
from src.datadef.chat_message import Message_v1
from src.datadef.chat_history import ChatHistory
from src.datadef.enums.message_sender_type import MessageSenderType

from src.orm.Base import SQLFactory
from src.orm.tables.table_raw_message import TableRawMessage

from ..helper.llm_call.openai_chat import CallOpenAI
from ..helper.llm_call.claude import CallClaude
from ..helper.llm_call.gemini_generate_only import CallGemini
from ..helper.llm_call.perplexity import CallPerplexity

import uuid
import os
import datetime

class ResponseComparer(BotInterface_v1):
    botname = "response_comparer"
    agent_name = "resopnse_comparer"
    display_name = "同時投げかけBOT"
    useful_when = "compare multi LLM api response at once"
    description = """Compare LLM API resopnse at once.
targets are 

  * ChatGPT-4o
  * ChatGPT-4o-mini
  * Claude 3.5 Sonnet
  * gemini-1.5-flash
  * perplexity : llama-3.1-sonar-small-128k-online
  * perplexity : llama-3.1-70b-instruct

"""
    enable_version = ["v1"]

    async def bot_response(self, message: Message_v1, history: ChatHistory) -> list[Message_v1]:
        dbobj = SQLFactory.default_env()
        raw_table = TableRawMessage(dbobj)
        bot_resp = []

        subject = message.content

        # chatgpt-4o-mini
        try:
            chatgpt = CallOpenAI(os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini")

            request = [
                {
                    "role": "user",
                    "content": subject
                }
            ]
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

            bot_resp.append(resp)
        except Exception as ex:
            err_msg = Message_v1.build_msg(
                sender=MessageSenderType.bots_meta,
                botname=self.botname,
                agent=self.agent_name,
                content=f"Failed to call LLM API : chat gpt : gpt-4o-mini : {ex}"
            )
            bot_resp.append(err_msg)

        # chatgpt-4o
        try:
            chatgpt = CallOpenAI(os.getenv("OPENAI_API_KEY"), model="gpt-4o")

            request = [
                {
                    "role": "user",
                    "content": subject
                }
            ]
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

            bot_resp.append(resp)
        except Exception as ex:
            err_msg = Message_v1.build_msg(
                sender=MessageSenderType.bots_meta,
                botname=self.botname,
                agent=self.agent_name,
                content=f"Failed to call LLM API : chat gpt : gpt-4o : {ex}"
            )
            bot_resp.append(err_msg)

        # claude 3.5 sonnet
        try:
            claude = CallClaude(os.getenv("ANTHOROPIC_API_KEY"), model="claude-3-5-sonnet-20240620")

            request = [
                {
                    "role": "user",
                    "content": subject
                }
            ]
            raw_resp = await claude.call(request)

            resp = claude.response_to_message_v1(raw_resp)
            msg_id = str(uuid.uuid4())
            msg_time = datetime.datetime.now()
            raw_table.insert(msg_id, raw_resp.to_dict())

            # build response
            resp.message_id = msg_id
            resp.time = msg_time
            resp.sender_type = MessageSenderType.chatbot
            resp.botname = self.botname
            resp.agent = self.agent_name

            bot_resp.append(resp)
        except Exception as ex:
            err_msg = Message_v1.build_msg(
                sender=MessageSenderType.bots_meta,
                botname=self.botname,
                agent=self.agent_name,
                content=f"Failed to call LLM API : chat gpt : claude-3.5-sonnet : {ex}"
            )
            bot_resp.append(err_msg)

        # gemini-1.5-flash
        try:
            gemini = CallGemini(os.getenv("GEMINI_API_KEY"), model="gemini-1.5-flash")

            request = f"User: {subject}"
            raw_resp = await gemini.call(request)

            resp = gemini.response_to_message_v1(raw_resp)
            msg_id = str(uuid.uuid4())
            msg_time = datetime.datetime.now()
            raw_table.insert(msg_id, raw_resp.to_dict())

            # build response
            resp.message_id = msg_id
            resp.time = msg_time
            resp.sender_type = MessageSenderType.chatbot
            resp.botname = self.botname
            resp.agent = self.agent_name

            bot_resp.append(resp)
        except Exception as ex:
            err_msg = Message_v1.build_msg(
                sender=MessageSenderType.bots_meta,
                botname=self.botname,
                agent=self.agent_name,
                content=f"Failed to call LLM API : chat gpt : gemini-1.5-flash : {ex}"
            )
            bot_resp.append(err_msg)
    
        # perlpexity : llama-3.1-sonar-small-128k-online
        try:
            perp = CallPerplexity(os.getenv("PERPLEXITY_API_KEY"), model="llama-3.1-sonar-small-128k-online")

            request = [
                {
                    "role": "user",
                    "content": subject
                }
            ]
            raw_resp = await perp.call(request)

            resp = perp.response_to_message_v1(raw_resp)
            msg_id = str(uuid.uuid4())
            msg_time = datetime.datetime.now()
            raw_table.insert(msg_id, raw_resp.to_dict())

            # build response
            resp.message_id = msg_id
            resp.time = msg_time
            resp.sender_type = MessageSenderType.chatbot
            resp.botname = self.botname
            resp.agent = self.agent_name

            bot_resp.append(resp)
        except Exception as ex:
            err_msg = Message_v1.build_msg(
                sender=MessageSenderType.bots_meta,
                botname=self.botname,
                agent=self.agent_name,
                content=f"Failed to call LLM API : chat gpt : llama-3.1-sonar-small-128k-online : {ex}"
            )
            bot_resp.append(err_msg)

        # perlpexity : llama-3.1-70b-instruct
        try:
            perp = CallPerplexity(os.getenv("PERPLEXITY_API_KEY"), model="llama-3.1-70b-instruct")

            request = [
                {
                    "role": "user",
                    "content": subject
                }
            ]
            raw_resp = await perp.call(request)

            resp = perp.response_to_message_v1(raw_resp)
            msg_id = str(uuid.uuid4())
            msg_time = datetime.datetime.now()
            raw_table.insert(msg_id, raw_resp.to_dict())

            # build response
            resp.message_id = msg_id
            resp.time = msg_time
            resp.sender_type = MessageSenderType.chatbot
            resp.botname = self.botname
            resp.agent = self.agent_name

            bot_resp.append(resp)
        except Exception as ex:
            err_msg = Message_v1.build_msg(
                sender=MessageSenderType.bots_meta,
                botname=self.botname,
                agent=self.agent_name,
                content=f"Failed to call LLM API : chat gpt : llama-3.1-70b-instruct : {ex}"
            )
            bot_resp.append(err_msg)

        return bot_resp




