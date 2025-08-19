from enum import Enum


class Status(Enum):
    CANCELLED = "cancelled"
    DONE = "done"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
