from dotenv import load_dotenv
load_dotenv()
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(root_path=os.getenv("ROOT_PATH", ""))

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv('ALLOW_ORIGINS'),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
from src.datadef.chat_updates import ChatDiff_v1

# ---------------------------------------------------------

from src.bots_manag.bot_manage import BotManager


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
        return HTTPException(detail="Bot not found", status_code=404)

    b_data = BotsInfo.from_db(single_bot)
    return b_data

@app.get("/bots/edit/{botname}", response_model=BotsDetail, tags=["Chatbot"])
async def get_bot_detail_for_edit(botname: str) -> BotsDetail:
    dbobj = SQLFactory.default_env()
    chatbots = TableChatbot(dbobj)
    single_bot = chatbots.get_single_bot(botname)

    if not single_bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    b_data = BotsDetail.from_db(single_bot)
    return b_data

@app.post("/bots/edit/", tags=["Chatbot"])
async def edit_bot(bot: BotsDetail) -> GeneralStatus:
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
    
    #all_history = history.get_all_history()
    #all_history = history.get_all_history_with_messagetime()
    all_history = history.get_all_history_time_ordered()
    # print(all_history)

    history_list = [ChatShortHistory.from_db(h) for h in all_history]
    return history_list


# ---------------------------------------------------------
# v1 chatting definition

# チャット履歴を取得するエンドポイント
@app.get("/v1/chat/history", tags=["Chatting"])
@app.get("/v1/chat/history/{history_id}", tags=["Chatting"])
async def v1_get_chat_history(history_id: str | None = None) -> ChatHistory:
    dbobj = SQLFactory.default_env()
    history = TableChatHistory(dbobj)
    history_msg = TableChatHistoryList(dbobj)
    chat_db = TableChatMessage(dbobj)

    if history_id is None:
        # 新規作成しそれを返す
        history_id = history.create_new_history(str(uuid.uuid4()))
    else:
        # 存在するかをチェック
        if not history.exists(history_id):
            raise HTTPException(status_code=404, detail=f"history {history_id} not exists")

    data = history.get_single_history(history_id)
    message_ids = [m.message_id for m in history_msg.get_all_messages(history_id)]
    messages = chat_db.get_messages(message_ids)

    # build response
    response_history = ChatHistory.from_db(data)
    response_history.messages = [Message_v1.from_db(m) for m in messages]
    return response_history

@app.post("/v1/chat/history", tags=["Chatting"])
async def v1_set_chat_history(history_id: str, title: str, summary: str) -> GeneralStatus:
    dbobj = SQLFactory.default_env()
    history = TableChatHistory(dbobj)

    print(f"title -> {title}, summary -> {summary}")

    # 履歴の存在確認
    if not history.exists(history_id):
        raise HTTPException(status_code=404, detail=f"history {history_id} not exists")

    # タイトルとサマリーを更新
    history.update_title_and_summary(history_id, title, summary)

    return GeneralStatus(
        status=200,
        message="title and summary updated",
        detail="no detail info"
    )

@app.post("/v1/chat/history/auto_title")
async def v1_auto_summary(history_id: str) -> ChatShortHistory:
    dbobj = SQLFactory.default_env()
    history = TableChatHistory(dbobj)
    history_msg = TableChatHistoryList(dbobj)
    msg_table = TableChatMessage(dbobj)

    # 履歴の存在確認
    if not history.exists(history_id):
        raise HTTPException(status_code=404, detail=f"history {history_id} not exists")

    # メッセージの取得
    message_dbdata = history_msg.get_all_messages(history_id)
    if not message_dbdata:
        raise HTTPException(status_code=404, detail=f"No messages found for history {history_id}")

    first_message = msg_table.get_messages([message_dbdata[0].message_id])[0]
    
    # タイトルとサマリーの設定（最初のメッセージの20文字）
    title_summary = first_message.content[:20]
    history.update_title_and_summary(history_id, title_summary, title_summary)

    # 更新されたデータの再取得
    updated_history = history.get_single_history(history_id)
    
    return ChatShortHistory.from_db(updated_history)



@app.post("/v1/chat/send", tags=["Chatting"])
async def v1_send_message(history_id: str, message: Message_v1) -> ChatDiff_v1:
    dbobj = SQLFactory.default_env()
    history = TableChatHistory(dbobj)
    history_msg = TableChatHistoryList(dbobj)
    msg_table = TableChatMessage(dbobj)
    bots_table = TableChatbot(dbobj)

    # history の存在確認
    if not history.exists(history_id):
        raise HTTPException(status_code=404, detail=f"history {history_id} not exists")

    # rebuild chat history
    history_dbdata = history.get_single_history(history_id)
    history_data = ChatHistory.from_db(history_dbdata)
    message_dbdata = history_msg.get_all_messages(history_id)
    message_fullbody = msg_table.get_messages([m.message_id for m in message_dbdata])
    history_data.messages = [Message_v1.from_db(m) for m in message_fullbody]

    # prepare response
    chat_resp = ChatDiff_v1(
        history_id=history_id,
        time=datetime.datetime.now(),
        messages=[]
    )

    message.message_id = str(uuid.uuid4()) if message.message_id is None else message.message_id
    message.time = datetime.datetime.now() if message.time is None else message.time
    chat_resp.messages.append(message)

    # update status
    history.update_status(history_id, ChatStatus.in_progress)

    # add user messages to history
    new_message_data = chat_resp.messages[0].to_db()
    msg_table.upsert_message(new_message_data)
    msg_id = new_message_data.id
    history_msg.append_new_message(history_id, msg_id, new_message_data.time)

    # load and call bot
    botdef = bots_table.get_single_bot(message.botname)
    if not botdef:
        raise HTTPException(404, f"requested bot ({message.botname}) not found")

    try:
        mgr = BotManager(botdef)
        mgr.load()
        bot_resp = await mgr.send(message, history_data)
    except Exception as ex:
        history.update_status(history_id, ChatStatus.failed)
        bot_resp += Message_v1.build_msg(
            sender=MessageSenderType.bots_meta,
            botname="error",
            agent="dullahan",
            content=f"bot process failed with exception : {ex}"
        )
        for msg in bot_resp:
            msg_table.upsert_message(msg.to_db())
            history_msg.append_new_message(history_id, msg.message_id, msg.time)
        return GeneralStatus(
            status=500,
            message=f"bot message failed with exception : {ex}"
        )

    chat_resp.messages += bot_resp

    # Chatbot message added to db
    for msg in bot_resp:
        msg_table.upsert_message(msg.to_db())
        history_msg.append_new_message(history_id, msg.message_id, msg.time)

    # update status
    history.update_status(history_id, ChatStatus.completed)

    # 応答の返却
    return chat_resp

