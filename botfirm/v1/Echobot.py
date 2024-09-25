from src.bots_manag.IBots_v1 import BotInterface_v1
from src.datadef.chat_message import Message_v1
from src.datadef.enums.message_sender_type import MessageSenderType

class Echobot(BotInterface_v1):
    botname = "echobot"
    agent_name = "echobot"
    display_name = "Echobot (message_v1)"
    useful_when = "testing message interface"
    description = "echo user input to output. Helpful for testing"
    enable_version = ["v1"]

    async def bot_response(self, message: Message_v1) -> list[Message_v1]:
        bot_resp = []

        # bots core
        # expand user message
        user_msg = message.content

        # llm calling
        response = f"echobot : {user_msg}"

        # build response
        bot_resp.append(Message_v1.build_msg(
            sender=MessageSenderType.chatbot,
            botname=self.botname,
            agent=self.agent_name,
            content=response,
        ))

        return bot_resp




