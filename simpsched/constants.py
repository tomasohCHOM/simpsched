from enum import Enum


class Action(Enum):
    ADD = "Add"
    UPDATE = "Update"
    REMOVE = "Remove"
    LIST = "List"
    EXIT = "Exit"


class Status(Enum):
    CANCELLED = "cancelled"
    DONE = "done"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
