from pydantic import BaseModel

from src.orm.models.chatbot import ChatBot

# bots information 定義
class BotsInfo(BaseModel):
    """
    ユーザーにも見せられるボットの管理情報
    """
    botname: str
    useful_when: str
    description: str
    supported_message_version: list[str]

    @classmethod
    def from_db(cls, db_data):
        return BotsInfo(
            botname=db_data.botname,
            useful_when=db_data.useful_when,
            description=db_data.description,
            supported_message_version=db_data.enable_version,
        )

class BotsDetail(BaseModel):
    """
    Bot作成・管理者のみが閲覧可能なボットの設定情報
    """
    botname: str
    useful_when: str
    description: str
    supported_message_version: list[str]
    module_filename: str
    classname: str

    @classmethod
    def from_db(cls, db_data):
        return BotsDetail(
            botname=b.botname,
            useful_when=b.useful_when,
            description=b.description,
            supported_message_version=b.enable_version,
            module_filename=b.module_filename,
            classname=b.classname,
        )

    def to_db(self):
        return ChatBot(
            botname=self.botname,
            useful_when=self.useful_when,
            description=self.description,
            enable_version=self.supported_message_version,
            module_filename=self.module_filename,
            classname=self.classname,
        )
