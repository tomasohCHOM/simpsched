from .constants import Status
from .validations import TitleNotEmptyValidator

task_prompts = {
    "title": {
        "name": "title",
        "qtype": "text",
        "prompt": "Enter task title:",
        "kwargs": {"validate": TitleNotEmptyValidator},
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
    },
    "task_id": {
        "name": "task_id",
        "qtype": "text",
        "prompt": "Enter the task id:",
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
        # task_prompts["status"],
        task_prompts["due_at"],
    ],
    "rm": [task_prompts["task_id"], task_prompts["confirm"]],
    "update": [
        task_prompts["task_id"],
        task_prompts["choose"],
    ],
}
