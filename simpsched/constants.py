from enum import Enum


class Action(Enum):
    ADD = "Add"
    UPDATE = "Update"
    REMOVE = "Remove"
    LIST = "List"
    EXIT = "Exit"


class Status(Enum):
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
    DONE = "done"
    CANCELLED = "cancelled"


STATUS_COLORS = {
    Status.CANCELLED.value: "red",
    Status.DONE.value: "green",
    Status.IN_PROGRESS.value: "yellow",
    Status.PENDING.value: "dim",
}

USER_PROMPTS = {
    "title": "Enter task title",
    "desc": "Enter desc (optional):",
    "due_at": "Enter due date (YYYY-MM-DD HH:MM:SS) (optional):",
    "status": "Select the status of your task:",
}
