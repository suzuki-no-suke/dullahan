from src.orm.models.chat_message import ChatMessage

class TableChatMessage:
    def __init__(self, dbobj):
        self.dbobj = dbobj

    def get_messages(self, message_ids):
        with self.dbobj.get_new_session() as s:
            sess = s.session
            return sess.query(ChatMessage) \
                .filter_by(ChatMessage.id.in_(tuple(message_ids))) \
                .all()

    def upsert_message(self, message):
        with self.dbobj.get_new_session() as s:
            sess = s.session
            existing_message = sess.query(ChatMessage).filter_by(id=message.id).first()
            if existing_message:
                sess.query(ChatMessage) \
                    .filter_by(id=message.id) \
                    .update(message.diff_dict())
            else:
                sess.add(message)
            sess.commit()
            return sess.query(ChatMessage).filter_by(id=message.id).first()
