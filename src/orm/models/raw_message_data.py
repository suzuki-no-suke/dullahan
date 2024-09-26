from ..Base import Base

from sqlalchemy.schema import Column
from sqlalchemy.types import String, JSON

class RawMessageData(Base):
    __tablename__ = 'raw_message_data'

    message_id = Column(String(64), primary_key=True)
    data = Column(JSON, nullable=False)
