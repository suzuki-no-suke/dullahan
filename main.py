from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

import datetime
import enum


# ---------------------------------------------------------

from src.orm.Base import SQLFactory
from src.orm.models.chatbot import ChatBot
from src.orm.tables.table_chatbot import TableChatbot
from src.orm.tables.build_chat_history import TableChatHistoryList
from src.orm.tables.table_chathistory import TableChatHistory

from src.orm.models.chat_history import ChatStatus


# ---------------------------------------------------------
# 共通ステータス応答
class GeneralStatus(BaseModel):
    status: int
    message: str
    detail: str = ""

# bots information 定義
class BotsInfo(BaseModel):
    botname: str
    useful_when: str
    description: str
    supported_message_version: list[str]

class BotsDetail(BaseModel):
    botname: str
    useful_when: str
    description: str
    supported_message_version: list[str]
    module_filename: str
    classname: str

# chat history 定義
class MessageType_v1(enum.Enum):
    Human = 'human'
    Chatbot = 'chatbot'

class Message_v1(BaseModel):
    message_id: str # uuid
    time: datetime.datetime
    type: MessageType_v1
    botname: str
    agent: str
    content: str

class MessageType_v2(enum.Enum):
    Human = 'human'
    HumanMeta = 'human_meta'
    Chatbot = 'chatbot'
    BotsMeta = 'bots_meta'

class Message_v2(BaseModel):
    message_id: str # uuid
    time: datetime.datetime
    type: MessageType_v2
    botname: str
    agent: str
    content: str
    body: dict

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
    messages: list[Message_v1 | Message_v2]




# ---------------------------------------------------------
# bots list
@app.get("/bots/list", tags=["Chatbot"])
async def get_chatbot_list() -> list[BotsInfo]:
    dbobj = SQLFactory.default_env()

    # get all bots info
    chatbots = TableChatbot(dbobj)
    allbots = chatbots.get_all_bots()

    print(allbots)

    bots = []
    for b in allbots:
        b_data = BotsInfo(
            botname=b.botname,
            useful_when=b.useful_when,
            description=b.description,
            supported_message_version=b.enable_version,
        )
        bots.append(b_data)
    return bots

@app.get("/bots/detail/{botname}", tags=["Chatbot"])
async def get_chatbot_detail(botname: str) -> BotsInfo:
    dbobj = SQLFactory.default_env()

    # get single bot info
    chatbots = TableChatbot(dbobj)
    single_bot = chatbots.get_single_bot(botname)

    if not single_bot:
        return HTMLResponse(content="Bot not found", status_code=404)

    b = single_bot[0]
    b_data = BotsInfo(
        botname=b.botname,
        useful_when=b.useful_when,
        description=b.description,
        supported_message_version=b.enable_version,
    )
    return b_data

@app.get("/bots/edit/{botname}", response_model=BotsDetail, tags=["Chatbot"])
async def get_bot_detail_for_edit(botname: str) -> BotsDetail:
    dbobj = SQLFactory.default_env()
    chatbots = TableChatbot(dbobj)
    single_bot = chatbots.get_single_bot(botname)

    if not single_bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    b = single_bot[0]
    b_data = BotsDetail(
        botname=b.botname,
        useful_when=b.useful_when,
        description=b.description,
        supported_message_version=b.enable_version,
        module_filename=b.module_filename,
        classname=b.classname,
    )
    return b_data

@app.post("/bots/edit/", tags=["Chatbot"])
async def edit_bot(bot: BotsDetail):
    dbobj = SQLFactory.default_env()
    chatbots = TableChatbot(dbobj)

    # upsert bot
    botdata = ChatBot(
        botname=bot.botname,
        useful_when=bot.useful_when,
        description=bot.description,
        enable_version=bot.supported_message_version,
        module_filename=bot.module_filename,
        classname=bot.classname,
    )
    upserted = chatbots.upsert_single_bot(botdata)
    
    return GeneralStatus(
        status=200,
        message=f"bot successfully updated/added : {upserted.botname}",
    )


# ---------------------------------------------------------
# chat history list definition

@app.get("/chatlist", tags=["HistoryList"])
async def get_chatlist() -> list[ChatShortHistory]:
    dbobj = SQLFactory.default_env()
    history = TableChatHistory(dbobj)
    
    all_history = history.get_all_history()
    history_list = []
    for h in all_history:
        history_list.append(ChatShortHistory(
            id=h.id,
            status=h.status,
            title=h.title if "---" else h.title,
            summary=h.summary if "---" else h.summary,
            message_version=h.message_version
        ))
    return history_list


# ---------------------------------------------------------
# v1 chatting definition

# チャット履歴を取得するエンドポイント
@app.get("/v1/chat/history", tags=["Chatting"])
@app.get("/v1/chat/history/{id}", tags=["Chatting"])
async def v1_get_chat_history(id: int = None):
    if id is None:
        # 新規作成のロジックを追加
        return {"message": "New chat history created"}
    else:
        # DBからチャット履歴を取得するロジックを追加
        return {"message": f"Chat history for ID {id} retrieved"}

# メッセージを送信するエンドポイント
@app.post("/v1/chat/send", tags=["Chatting"])
async def v1_send_message(message: Message_v1):
    # ここにメッセージ送信のロジックを追加
    return {"message": "Message sent", "content": message.content}  # 変更: message.contentにアクセス


# ---------------------------------------------------------
# support frontend response

from fastapi.responses import HTMLResponse
import os

@app.get("/help_ui/{filename}", response_class=HTMLResponse)
async def get_help_ui(filename: str):
    file_path = os.path.join("help_ui", filename)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return HTMLResponse(content=content)
    else:
        return HTMLResponse(content="File not found", status_code=404)

@app.get("/help_ui/statics/{filename}", response_class=HTMLResponse)
async def get_help_ui_statics(filename: str):
    file_path = os.path.join("help_ui", "statics", filename)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return HTMLResponse(content=content)
    else:
        return HTMLResponse(content="File not found", status_code=404)
