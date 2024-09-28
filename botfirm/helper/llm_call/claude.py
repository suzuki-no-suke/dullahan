import anthropic

from src.datadef.chat_history import ChatHistory
from src.datadef.chat_message import Message_v1
from src.datadef.enums.message_sender_type import MessageSenderType

import asyncio
import functools

class CallClaude:
    def __init__(self, api_key, model="claude-3-5-sonnet-20240620", max_tokens=8192):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens

    async def call(self, request):
        print("request is -> ")
        print(request)
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            functools.partial(self.client.messages.create,
                model=self.model,
                messages=request,
                max_tokens=self.max_tokens)
        )
        return response

    def history_to_request_v1(self, user_request: Message_v1, history: ChatHistory) -> list[dict]:
        request = []
        for msg in history.messages:
            if msg.sender_type == MessageSenderType.system:
                request.append({
                    "role": "system",
                    "content": msg.content
                })
            elif msg.sender_type == MessageSenderType.human:
                request.append({
                    "role": "user",
                    "content": msg.content
                })
            elif msg.sender_type == MessageSenderType.chatbot:
                request.append({
                    "role": "assistant",
                    "content": msg.content
                })
        request.append({
            "role": "user",
            "content": user_request.content
        })
        return request

    def response_to_message_v1(self, raw_response) -> Message_v1:
        return Message_v1.build_msg(
            MessageSenderType.chatbot, "unknown", "claude",
            raw_response.content[0].text)