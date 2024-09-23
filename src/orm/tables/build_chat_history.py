from src.orm.models.chat_message_list import ChatMessageList

class TableChatHistoryList:
    def __init__(self, dbobj):
        self.dbobj = dbobj

    def get_all_messages(self, history_id):
        with self.dbobj.get_new_session() as s:
            sess = s.session
            return sess.query(ChatMessageList) \
                .filter_by(history_id=history_id) \
                .order_by(ChatMessageList.time) \
                .all()

    def append_new_message(self, history_id, message_id, time):
        with self.dbobj.get_new_session() as s:
            sess = s.session
            new_message = ChatMessageList(
                history_id=history_id,
                message_id=message_id,
                time=time
            )
            sess.add(new_message)
            sess.commit()
            return new_message

