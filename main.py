# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# ---------------------------------------------------------
# bots information 定義
class BotsInfo(BaseModel):
    botname: str
    useful_when: str
    description: str
    enable_version: list[str]

# chat history 定義
class Message(BaseModel):
    content: str


# ---------------------------------------------------------
# bots list
@app.get("/bots/list")
async def get_chatbot_list():
    bots = [
        BotsInfo(botname="Bot1", useful_when="When you need help", description="This is Bot1", enable_version=["v1"]),
        BotsInfo(botname="Bot2", useful_when="For fun conversations", description="This is Bot2", enable_version=["v1"]),
    ]
    return bots


# ---------------------------------------------------------
# v1 definition

# チャット履歴を取得するエンドポイント
@app.get("/v1/chat/history")
@app.get("/v1/chat/history/{id}")
async def v1_get_chat_history(id: int = None):
    if id is None:
        # 新規作成のロジックを追加
        return {"message": "New chat history created"}
    else:
        # DBからチャット履歴を取得するロジックを追加
        return {"message": f"Chat history for ID {id} retrieved"}

# メッセージを送信するエンドポイント
@app.post("/chat/send")
async def v1_send_message(message: Message):  # 変更: 引数をMessage型に変更
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
