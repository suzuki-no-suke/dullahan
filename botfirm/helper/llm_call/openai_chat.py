import openai

from src.datadef.chat_history import ChatHistory
from src.datadef.chat_message import Message_v1
from src.datadef.enums.message_sender_type import MessageSenderType

class CallOpenAI:
    def __init__(self, api_key, model="gpt-4o-mini"):
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model

    async def call(self, request):
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=request,
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
            MessageSenderType.chatbot, "unknown", "unknown",
            raw_response.choices[0].message.content)