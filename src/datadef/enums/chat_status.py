import enum

class ChatStatus(enum.Enum):
    Waiting = 'waiting'
    InProgress = 'in_progress'
    Failed = 'failed'
    Completed = 'completed'
