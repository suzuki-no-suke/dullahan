from src.bots_manag.IBots_v1 import BotInterface_v1
from src.datadef.chat_message import Message_v1
from src.datadef.enums.message_sender_type import MessageSenderType

class Rubberduck(BotInterface_v1):
    botname = "rubberduck"
    agent_name = "rubberduck"
    display_name = "Rubberduck (message_v1)"
    useful_when = "Talking oneself, rubberducking"
    description = "They will listen to your story attentively, thoughtfully, and silently."
    enable_version = ["v1"]

    async def bot_response(self, message: Message_v1) -> list[Message_v1]:
        bot_resp = []

        # llm calling
        response = f"..."

        # build response
        bot_resp.append(Message_v1.build_msg(
            sender=MessageSenderType.chatbot,
            botname=self.botname,
            agent=self.agent_name,
            content=response,
        ))

        return bot_resp




