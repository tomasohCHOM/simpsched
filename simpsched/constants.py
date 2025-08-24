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

FLAGS = {
    "id": "--id",
    "title": "--title",
    "desc": "--desc",
    "due_at": "--due_at",
    "status": "--status",
}

HELP = {
    "id": "Task ID",
    "title": "Task title",
    "desc": "Task description",
    "due_at": "Due date (YYYY-MM-DD HH:MM:SS - time is optional)",
    "status": "Status of the task",
}

STATUS_PRIORITY = {
    Status.IN_PROGRESS.value: 0,
    Status.PENDING.value: 1,
    Status.CANCELLED.value: 2,
    Status.DONE.value: 3,
}
