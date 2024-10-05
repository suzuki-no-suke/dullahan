from src.bots_manag.IBots_v1 import BotInterface_v1
from src.datadef.chat_message import Message_v1
from src.datadef.chat_history import ChatHistory
from src.datadef.enums.message_sender_type import MessageSenderType

from ..helper.llm_call.openai_chat import CallOpenAI
from ..helper.web_retriever.GoogleSearch import GoogleSearch

from src.orm.Base import SQLFactory
from src.orm.tables.table_raw_message import TableRawMessage

import os

from jinja2 import Template

class PreResearcher(BotInterface_v1):
    botname = "pre_researcher"
    agent_name = "pre_researcher"
    display_name = "PreResearcher (v1)"
    useful_when = "search web resources for user's question"
    description = """Searching web resources
for user's question.

  1. generate search word
  2. search web for many search apis
  3. retrieve pages
  4. summary search results

Powered by ChatGPT (openai) 4o-mini and 4o 
"""
    enable_version = ["v1"]

    async def bot_response(self, message: Message_v1, history: ChatHistory) -> list[Message_v1]:
        dbobj = SQLFactory.default_env()
        raw_table = TableRawMessage(dbobj)

        subject = message.content
        bot_responses = []
        
        # prepare llm and retriever
        chatgpt_4o = CallOpenAI(os.getenv("OPENAI_API_KEY"), model="gpt-4o")
        chatgpt_4o_mini = CallOpenAI(os.getenv("OPENAI_API_KEY"))
        google_search = GoogleSearch(os.getenv("GOOGLE_API_KEY"), os.getenv("GOOGLE_CSE_ID"))

        # generate search word
        search_word_generate = """
ユーザーがこの情報について、Webから調べたいと考えた場合に、
どのような検索キーワードを使えばよいでしょうか？
また、それぞれの検索結果はなるべく重複がないようにしたいです。

解答形式
=======
input: <質問>
search:
- <検索ワード>
- <検索ワード>
- <検索ワード>


解答
=======
input: {{ user_input }}
search: 
"""
        # build search word response
        rendered_prompt = Template(search_word_generate).render({"user_input": subject})
        response = await chatgpt_4o.call(rendered_prompt)
        msgtmp = chatgpt_4o.response_to_message_v1(response)
        raw_table.insert(msgtmp.message_id, response.to_dict())

        bot_responses.append(Message_v1.build_msg(
            MessageSenderType.chatbot,
            self.botname,
            self.agent_name,
            rendered_prompt
        ))
        msgtmp.botname = self.botname
        msgtmp.agent = "chatgpt-4o"
        bot_responses.append(msgtmp)

        # parse search words
        search_words = self.word_parser(response)
        url_pot = set()
        for w in search_words:
            urls = google_search.search(w)
            if urls["succeed"]:
                url_pot.add(urls)
            else:
                pass





        prompt = """
次のテキストは、Webからユーザーの質問に応じた検索を行った結果とその要約です。
ユーザーの質問に対応する最終的な要約を作成してください。

また、そのあとに「また、私の知る限りでは、、、」という書き出しで
あなたの見解を述べてください。

ユーザーの質問：{{ user_input }}

-- 以下、Web情報のURLとその要約 --
{{ web_results }}
"""

        return bot_responses


    def word_parser(self, text):
        search_texts = []
        lines = text.split('\n')
        for l in lines:
            if l and l[0] == '-':
                search_texts.append(l[1:].strip())
        return search_texts

