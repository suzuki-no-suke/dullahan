from src.bots_manag.IBots_v1 import BotInterface_v1
from src.datadef.chat_message import Message_v1
from src.datadef.chat_history import ChatHistory
from src.datadef.enums.message_sender_type import MessageSenderType

from ..helper.prompts.parser.line_parse import LineParse
from ..helper.web_retriever.AsyncHTTPRequest import AsyncHTTPRequest, RequestStatus
from ..helper.llm_call.claude import CallClaude

from src.orm.Base import SQLFactory
from src.orm.tables.table_raw_message import TableRawMessage

import datetime
import os
import uuid

class CommandWeb(BotInterface_v1):
    botname = "command_web"
    agent_name = "command_web"
    display_name = "う！ (Web 調査班)"
    useful_when = "Download and markdown formatting web resources"
    description = """Web (うぇぶ＝＞う) 調査 BOT
URLを見たらサイトと思ってMarkdownで要約する
テキストとかは無視する（それだけだと不便なので検索リンクにする）

powered by Claude
"""
    enable_version = ["v1"]

    async def bot_response(self, message: Message_v1, history: ChatHistory) -> list[Message_v1]:
        dbobj = SQLFactory.default_env()
        raw_table = TableRawMessage(dbobj)

        # parse lines
        content = message.content
        urls = [l for l in LineParse(content, skip_empty=True)]

        # build markdown myself
        nowtime = datetime.datetime.now().isoformat()
        response = f"# web check @ {nowtime}\n\n"

        message_id = str(uuid.uuid4())

        # retreive all
        for url_like in urls:
            subbody, rawdata = await self.retrieve_and_response(url_like)
            raw_table.insert(message_id, rawdata.to_dict())
            response += subbody

        # build response
        bot_resp = []
        bot_resp.append(Message_v1.build_msg(
            sender=MessageSenderType.chatbot,
            botname=self.botname,
            agent=self.agent_name,
            content=response,
        ))
        bot_resp[0].message_id = message_id

        return bot_resp

    async def retrieve_and_response(self, url_or_msg: str):
        getter = AsyncHTTPRequest(url_or_msg)
        get_result = await getter.get()
        markdown = ""
        if get_result.status == RequestStatus.InvalidURL:
            # not url
            markdown += f"## (NOT URL) : {url_or_msg}\n"
            markdown += f"[Google](https://www.google.co.jp/search?q={url_or_msg})\n"
            markdown += f"[Bing](https://www.bing.co.jp/search?q={url_or_msg})\n"
            markdown += f"[DuckDuckGo](https://www.duckduckgo.com/?q={url_or_msg})\n"
            markdown += "\n"
        elif get_result.status == RequestStatus.NotFound:
            # not found
            markdown += f"## (NOT FOUND) : {url_or_msg}\n"
            markdown += "\n"
        elif get_result.status == RequestStatus.Found:
            # found
            retrieved = getter.analysis()
            markdown += f"## [{retrieved.title}]({url_or_msg})\n"
            markdown += f"description: \n\n"
            markdown += f"{retrieved.description}\n\n"
            markdown += f"full text: \n\n"

            # summarize
            llm = CallClaude(os.getenv("ANTHOROPIC_API_KEY"))
            prompt = f"""
次のテキストはWebページのソースコードです。この内容からコンテンツを抽出し、要約してください

## HTML TEXT
{retrieved.full_html}
"""
            request = [{"role": "user", "content": prompt}]
            response = await llm.call(request)
            markdown += f"{response.content[0].text}\n\n"

        return markdown, response



