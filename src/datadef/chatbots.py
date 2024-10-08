from pydantic import BaseModel

from src.orm.models.chatbot import ChatBot

# bots information 定義
class BotsInfo(BaseModel):
    """
    ユーザーにも見せられるボットの管理情報
    """
    botname: str
    display_name: str
    useful_when: str
    description: str
    supported_message_version: list[str]

    @classmethod
    def from_db(cls, db_data):
        return BotsInfo(
            botname=db_data.botname,
            display_name=db_data.display_name,
            useful_when=db_data.useful_when,
            description=db_data.description,
            supported_message_version=db_data.enable_version,
        )

class BotsDetail(BaseModel):
    """
    Bot作成・管理者のみが閲覧可能なボットの設定情報
    """
    botname: str
    display_name: str
    useful_when: str
    description: str
    supported_message_version: list[str]
    module_filename: str
    classname: str

    @classmethod
    def from_db(cls, db_data):
        return BotsDetail(
            botname=db_data.botname,
            display_name=db_data.display_name,
            useful_when=db_data.useful_when,
            description=db_data.description,
            supported_message_version=db_data.enable_version,
            module_filename=db_data.module_filename,
            classname=db_data.classname,
        )

    def to_db(self):
        return ChatBot(
            botname=self.botname,
            display_name=self.display_name,
            useful_when=self.useful_when,
            description=self.description,
            enable_version=self.supported_message_version,
            module_filename=self.module_filename,
            classname=self.classname,
        )
