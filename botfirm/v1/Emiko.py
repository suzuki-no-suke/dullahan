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
import traceback

class Emiko(BotInterface_v1):
    botname = "emiko"
    agent_name = "emiko"
    display_name = "笑子"
    useful_when = "cheer up yourself !"
    description = "response something cheer you up !"
    enable_version = ["v1"]

    async def bot_response(self, message: Message_v1, history: ChatHistory) -> list[Message_v1]:
        dbobj = SQLFactory.default_env()
        raw_table = TableRawMessage(dbobj)
        bot_resp = []

        prompt = f"""あなたは女性で、とても明るい気持ち・性格です。
あなたに話しかけてきているのは、そんなあなたに元気づけられたいと思っている人物です。
あなたはあなた自身がどうであろうかということはいったん置いておき、
ひとまず目の前の相手を元気づけられるとよいなと考えて行動します。

あなたに対して次のような言葉を投げかけてきました。
あなたはこれに対して反応を返してあげてください

「{message.content}」
"""
        # chatgpt-4o-mini
        try:
            chatgpt = CallOpenAI(os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini")

            if len(history.messages) <= 1:
                request = chatgpt.history_to_request_v1(
                    Message_v1(
                        sender_type=MessageSenderType.human,
                        content=prompt),
                    history)
            else:
                request = chatgpt.history_to_request_v1(message, history)
            print(request)
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
            traceback.print_exc()
            bot_resp.append(err_msg)

        return bot_resp




