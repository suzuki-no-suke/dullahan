import enum

class ChatStatus(enum.Enum):
    waiting = 'waiting'
    in_progress = 'in_progress'
    failed = 'failed'
    completed = 'completed'
