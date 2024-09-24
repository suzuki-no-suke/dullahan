from abc import ABC, abstractmethod

from src.datadef.chat_message import Message_v1

# インターフェイスクラスの定義
class BotInterface_v1(ABC):
    botname = "ibot_v1_interface"
    agent_name = "botinterface_v1"
    display_name = "undefined"
    useful_when = "implement bots"
    description = "abstruct interface class of bot, for Message_v1"

    @abstractmethod
    async def bot_response(self, message: Message_v1) -> list[Message_v1]:
        raise NotImplementedError("This is Interface class. implement error occured on bot ")
