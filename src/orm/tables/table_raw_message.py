from src.orm.models.raw_message_data import RawMessageData

class TableRawMessage:
    def __init__(self, dbobj):
        self.dbobj = dbobj

    def insert(self, message_id: str, raw_data : dict):
        with self.dbobj.get_new_session() as s:
            sess = s.session
            RawMessageData(message_id=message_id, data=raw_data)
            sess.add(raw_data)
            sess.commit()
