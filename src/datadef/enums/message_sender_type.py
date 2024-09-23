import enum

class MessageSenderType(enum.Enum):
    Human = 'human'
    UserMeta = 'user_meta'
    Chatbot = 'chatbot'
    BotsMeta = 'bots_meta'
