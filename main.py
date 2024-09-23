from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException

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
from src.orm.models.chat_message import ChatMessage, MessageSenderType

# ---------------------------------------------------------

from src.datadef.general import GeneralStatus
from src.datadef.chatbots import BotsInfo, BotsDetail
from src.datadef.chat_message import Message_v1
from src.datadef.chat_history import ChatHistory, ChatShortHistory


# ---------------------------------------------------------
# experimental bot dummy
async def bot_dummy_v1(mesg: Message_v1) -> Message_v1:
    # expand user message
    user_msg = mesg.content

    # llm calling
    response = f"echobot : {user_msg}"

    # build response
    bot_mesg = Message_v1.build_msg(
        sender=MessageSenderType.chatbot,
        botname="dummybot_v1",
        agent="dummybot_v1",
        content=response,
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

    bots = [BotsInfo.from_db(b) for b in allbots]
    return bots

@app.get("/bots/detail/{botname}", tags=["Chatbot"])
async def get_chatbot_detail(botname: str) -> BotsInfo:
    dbobj = SQLFactory.default_env()

    # get single bot info
    chatbots = TableChatbot(dbobj)
    single_bot = chatbots.get_single_bot(botname)

    if not single_bot:
        return HTMLResponse(content="Bot not found", status_code=404)

    b_data = BotsInfo.from_db(single_bot[0])
    return b_data

@app.get("/bots/edit/{botname}", response_model=BotsDetail, tags=["Chatbot"])
async def get_bot_detail_for_edit(botname: str) -> BotsDetail:
    dbobj = SQLFactory.default_env()
    chatbots = TableChatbot(dbobj)
    single_bot = chatbots.get_single_bot(botname)

    if not single_bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    b_data = BotsDetail.from_db(single_bot[0])
    return b_data

@app.post("/bots/edit/", tags=["Chatbot"])
async def edit_bot(bot: BotsDetail):
    dbobj = SQLFactory.default_env()
    chatbots = TableChatbot(dbobj)

    # upsert bot
    botdata = bot.to_db()
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
    # print(all_history)

    history_list = [ChatShortHistory.from_db(h) for h in all_history]
    return history_list


# ---------------------------------------------------------
# v1 chatting definition

# チャット履歴を取得するエンドポイント
@app.get("/v1/chat/history", tags=["Chatting"])
@app.get("/v1/chat/history/{history_id}", tags=["Chatting"])
async def v1_get_chat_history(history_id: str | None = None):
    dbobj = SQLFactory.default_env()
    history = TableChatHistory(dbobj)
    history_msg = TableChatHistoryList(dbobj)

    if history_id is None:
        # 新規作成しそれを返す
        history_id = history.create_new_history(str(uuid.uuid4()))
    else:
        # 存在するかをチェック
        if not history.exists(history_id):
            raise HTTPException(status_code=404, detail=f"history {history_id} not exists")

    data = history.get_single_history(history_id)
    messages = history_msg.get_all_messages(history_id)

    # build response
    response_history = ChatHistory.from_db(data)
    response_history.messages = [Message_v1.from_db(m) for m in messages]
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
    new_message_data = message.to_db()
    new_message_data.id = str(uuid.uuid4())
    new_message_data.time = datetime.datetime.now()

    # update status
    history.update_status(history_id, ChatStatus.in_progress)

    # message added to db
    msg_table.upsert_message(new_message_data)
    msg_id = new_message_data.id
    history_msg.append_new_message(history_id, msg_id, new_message_data.time)

    # TBD : Chatbot 応答の構築
    bot_msg = await bot_dummy_v1(message)

    # Chatbot message added to db
    msg_table.upsert_message(bot_msg.to_db())
    history_msg.append_new_message(history_id, bot_msg.message_id, bot_msg.time)
    history.update_status(history_id, ChatStatus.completed)

    # 応答の返却
    return bot_msg

