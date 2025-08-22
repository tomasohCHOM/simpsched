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


STATUS_COLORS = {
    Status.CANCELLED.value: "red",
    Status.DONE.value: "green",
    Status.IN_PROGRESS.value: "yellow",
    Status.PENDING.value: "dim",
}

USER_PROMPTS = {
    "add": {
        "title": "Enter task title",
        "description": "Enter description (optional):",
        "due_at": "Enter due date (YYYY-MM-DD HH:MM:SS) (optional):",
    }
}
