import google.generativeai as googlegenai

from src.datadef.chat_history import ChatHistory
from src.datadef.chat_message import Message_v1
from src.datadef.enums.message_sender_type import MessageSenderType

import asyncio

class CallGemini:
    def __init__(self, api_key, model="gemini-1.5-flash"):
        googlegenai.configure(api_key=api_key)
        self.model = googlegenai.GenerativeModel(model)

    async def call(self, request):
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            self.model.generate_content,
            request
        )
        return response

    def history_to_request_v1(self, user_request: Message_v1, history: ChatHistory) -> str:
        request = ""
        for msg in history.messages:
            if msg.sender_type == MessageSenderType.system:
                request += f"System: {msg.content}\n"
            elif msg.sender_type == MessageSenderType.human:
                request += f"User: {msg.content}\n"
            elif msg.sender_type == MessageSenderType.chatbot:
                request += f"Assistant: {msg.content}\n"
        request += f"User: {user_request.content} \n"
        return request

    def response_to_message_v1(self, raw_response) -> Message_v1:
        return Message_v1(
            content=raw_response.text
        )