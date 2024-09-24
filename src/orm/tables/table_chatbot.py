from src.orm.models.chatbot import ChatBot

class TableChatbot:
    def __init__(self, dbobj):
        self.dbobj = dbobj

    def get_all_bots(self):
        with self.dbobj.get_new_session() as s:
            sess = s.session
            return sess.query(ChatBot).all()

    def get_single_bot(self, botname):
        with self.dbobj.get_new_session() as s:
            sess = s.session
            return sess.query(ChatBot).filter_by(botname=botname).first()

    def upsert_single_bot(self, chatbot):
        with self.dbobj.get_new_session() as s:
            sess = s.session
            existing_bot = sess.query(ChatBot).filter_by(botname=chatbot.botname).first()
            if existing_bot:
                sess.query(ChatBot).filter_by(botname=chatbot.botname).update(chatbot.diff_dict())
            else:
                sess.add(chatbot)
            sess.commit()
            return sess.query(ChatBot).filter_by(botname=chatbot.botname).first()
