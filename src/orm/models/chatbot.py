from ..Base import Base

from sqlalchemy.schema import Column, Identity
from sqlalchemy.types import Integer, String, Text, JSON

class ChatBot(Base):
    __tablename__ = 'chatbot'

    pk = Column(Integer, Identity(), primary_key=True)
    botname = Column(String(255), nullable=False)
    useful_when = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    enable_version = Column(JSON)
    # for real use information
    module_filename = Column(String)
    classname = Column(String)

    def diff_dict(self) -> dict:
        return {
            'botname': self.botname,
            'useful_when': self.useful_when,
            'description': self.description,
            'enable_version': self.enable_version,
            'module_filename': self.module_filename,
            'classname': self.classname
        }

    def __str__(self) -> str:
        return f"ChatBot - {self.pk} {self.botname} (module {self.module_filename} class {self.classname})"
