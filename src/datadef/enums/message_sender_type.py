import enum

class MessageSenderType(enum.Enum):
    human = 'human'
    user_meta = 'user_meta'
    chatbot = 'chatbot'
    bots_meta = 'bots_meta'
    system = 'system'
