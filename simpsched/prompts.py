from simpsched.utils import get_task_choices
from .constants import Status
from .validations import (
    InputNotEmptyValidator,
    IsValidIsoValidator,
)

task_prompts = {
    "title": {
        "name": "title",
        "qtype": "text",
        "prompt": "Enter task title:",
        "kwargs": {
            "validate": InputNotEmptyValidator("title"),
            "validate_while_typing": False,
        },
    },
    "desc": {
        "name": "desc",
        "qtype": "text",
        "prompt": "Enter task description (optional):",
    },
    "status": {
        "name": "status",
        "qtype": "select",
        "prompt": "Select task status:",
        "kwargs": {"choices": [s.value for s in Status]},
    },
    "due_at": {
        "name": "due_at",
        "qtype": "text",
        "prompt": "Enter due date (YYYY-MM-DD HH:MM:SS - time is optional) (optional):",
        "kwargs": {
            "validate": IsValidIsoValidator("due_at"),
            "validate_while_typing": False,
        },
    },
    "choose_task": {
        "name": "task_id",
        "qtype": "select",
        "prompt": "Choose from the following list of tasks:",
        "kwargs": {"choices": get_task_choices()},
    },
    "confirm": {
        "name": "confirm",
        "qtype": "confirm",
        "prompt": "Are you sure you want to remove this task?",
    },
    "choose": {
        "name": "fields",
        "qtype": "checkbox",
        "prompt": "Which field(s) do you want to edit?",
        "kwargs": {
            "choices": ["title", "desc", "due_at", "status"],
        },
    },
}

steps = {
    "add": [
        task_prompts["title"],
        task_prompts["desc"],
        task_prompts["status"],
        task_prompts["due_at"],
    ],
    "rm": [task_prompts["choose_task"], task_prompts["confirm"]],
    "update": [
        task_prompts["choose_task"],
        task_prompts["choose"],
    ],
}
