from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

import datetime
import enum
import uuid


# ---------------------------------------------------------

from src.orm.Base import SQLFactory
from src.orm.models.chatbot import ChatBot
from src.orm.tables.table_chatbot import TableChatbot
from src.orm.tables.build_chat_history import TableChatHistoryList
from src.orm.tables.table_chathistory import TableChatHistory
from src.orm.tables.table_chatmessage import TableChatMessage

from src.orm.models.chat_history import ChatStatus
from src.orm.models.chat_message import ChatMessage, ChatType

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
    title: str
    summary: str
    messages: list[Message_v1 | Message_v2]


# ---------------------------------------------------------
# experimental bot dummy
async def bot_dummy_v1(mesg: Message_v1) -> Message_v1:
    # expand user message
    user_msg = mesg.content

    # llm calling
    response = f"echobot : {user_msg}"

    # build response
    bot_mesg = Message_v1(
        message_id=str(uuid.uuid4()),
        time=datetime.datetime.now(),
        type=MessageType_v1.Chatbot,
        botname="dummybot_v1",
        agent="dummbot_v1",
        content=response
    )

    return bot_mesg


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
            title=h.title if h.title else "---",
            summary=h.summary if h.summary else "---",
            message_version=h.message_version
        ))
    return history_list


# ---------------------------------------------------------
# v1 chatting definition

# チャット履歴を取得するエンドポイント
@app.get("/v1/chat/history", tags=["Chatting"])
@app.get("/v1/chat/history/{history_id}", tags=["Chatting"])
async def v1_get_chat_history(history_id: int | None = None):
    dbobj = SQLFactory.default_env()
    history = TableChatHistory(dbobj)
    history_msg = TableChatHistoryList(dbobj)

    if history_id is None:
        # 新規作成しそれを返す
        history_id = history.create_new_history(uuid.uuid4())
    else:
        # 存在するかをチェック
        if not history.exists(history_id):
            raise HTTPException(status_code=404, detail=f"history {history_id} not exists")

    data = history.get_single_history(history_id)
    messages = history_msg.get_all_messages(history_id)

    # build response
    response_messages = [
        Message_v1(
            message_id=m.id,
            time=m.time,
            type=m.type,
            botname=m.botname,
            agent=m.agent,
            content=m.content
        ) for m in messages
    ]
    response_history = ChatHistory(
        history_id=history_id,
        chat_status=data.status,
        data_version=data.message_version,
        title=data.title if data.title else "---",
        summary=data.summary if data.summary else "---",
        messages=response_messages
    )
    return response_history


@app.post("/v1/chat/send", tags=["Chatting"])
async def v1_send_message(history_id: str, message: Message_v1):
    dbobj = SQLFactory.default_env()
    history = TableChatHistory(dbobj)
    history_msg = TableChatHistoryList(dbobj)
    msg_table = TableChatMessage(dbobj)

    # history の存在確認
    if not history.exists(history_id):
        raise HTTPException(status_code=404, detail=f"history {history_id} not exists")

    # add user messages to history
    new_message_data = ChatMessage(
        id=str(uuid.uuid4()),
        time=datetime.datetime.now(),   # ignore client side timestamp
        type=message.type,
        botname=message.botname,
        agent=message.agent,
        content=message.content,
        message_version="v1"
    )

    # message added to db
    msg_table.upsert_message(new_message_data)
    msg_id = new_message_data.id
    history_msg.append_new_message(history_id, msg_id, new_message_data.time)

    # TBD : Chatbot 応答の構築
    bot_msg = bot_dummy_v1(message)

    # Chatbot message added to db
    msg_table.upsert_message(bot_msg)
    history_msg.append_new_message(history_id, bot_msg.id, bot_msg.time)

    # 応答の返却
    return bot_msg


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
