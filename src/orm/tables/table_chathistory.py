from src.orm.models.chat_history import ChatHistory, ChatStatus
from src.orm.models.chat_message_list import ChatMessageList

import datetime

from sqlalchemy import select, func, desc
from sqlalchemy.orm import aliased

class TableChatHistory:
    def __init__(self, dbobj):
        self.dbobj = dbobj

    def get_all_history(self):
        with self.dbobj.get_new_session() as s:
            sess = s.session
            return sess.query(ChatHistory).all()

    def get_all_history_time_ordered(self):
        with self.dbobj.get_new_session() as s:
            sess = s.session
            return sess.query(ChatHistory).asc(ChatHistory.created_at).all()

    def get_all_history_with_messagetime(self):
        with self.dbobj.get_new_session() as s:
            sess = s.session
            subquery = (
                select(func.max(ChatMessageList.time).label('latest_time'))
                    .where(ChatMessageList.history_id == ChatHistory.id)
                    .scalar_subquery()
                    .correlate(ChatHistory)
            )
            query = (
                select(ChatHistory)
                    .order_by(desc(subquery))
            )
            return sess.execute(query).scalars().all()

    def create_new_history(self, uuid):
        with self.dbobj.get_new_session() as s:
            sess = s.session
            new_history = ChatHistory(
                id=uuid,
                status=ChatStatus.waiting,
                title=None,
                summary=None,
                created_at=datetime.datetime.now(),
                message_version="v1"
            )
            sess.add(new_history)
            sess.commit()
            return uuid

    def update_history(self, chat_history):
        with self.dbobj.get_new_session() as s:
            sess = s.session
            existing_history = sess.query(ChatHistory).filter_by(id=chat_history.id).first()
            if existing_history:
                sess.query(ChatHistory).filter_by(id=chat_history.id) \
                    .update(chat_history.diff_dict())
                return True
            return False

    def update_status(self,  history_id, status):
        with self.dbobj.get_new_session() as s:
            sess = s.session
            sess.query(ChatHistory) \
                .filter_by(id=history_id) \
                .update({"status": status})
            sess.commit()

    def update_title_and_summary(self, history_id, title, summary):
        with self.dbobj.get_new_session() as s:
            sess = s.session
            sess.query(ChatHistory) \
                .filter_by(id=history_id) \
                .update({
                    "title": title,
                    "summary": summary
                })
            sess.commit()

    def get_single_history(self, history_id):
        with self.dbobj.get_new_session() as s:
            sess = s.session
            return sess.query(ChatHistory).filter_by(id=history_id).first()

    def exists(self, history_id):
        with self.dbobj.get_new_session() as s:
            sess = s.session
            return sess.query(ChatHistory).filter_by(id=history_id).first() is not None
