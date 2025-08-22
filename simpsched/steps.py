from .constants import Status
from .validations import TitleNotEmptyValidator

steps = {
    "add": [
        {
            "name": "title",
            "qtype": "text",
            "prompt": "Enter task title:",
            "kwargs": {"validate": TitleNotEmptyValidator},
        },
        {
            "name": "desc",
            "qtype": "text",
            "prompt": "Enter description (optional):",
        },
        {
            "name": "due",
            "qtype": "text",
            "prompt": "Enter due date (YYYY-MM-DD HH:MM:SS) (optional):",
        },
        {
            "name": "confirm",
            "qtype": "confirm",
            "prompt": "Do you want to save this task?",
        },
    ],
    "rm": [
        {
            "name": "task_id",
            "qtype": "text",
            "prompt": "Enter the id of the task you want to remove:",
        },
        {
            "name": "confirm",
            "qtype": "confirm",
            "prompt": "Are you sure you want to remove this task?",
        },
    ],
    "update": [
        {
            "name": "fields",
            "qtype": "checkbox",
            "prompt": "Which field(s) do you want to edit?",
            "kwargs": {
                "choices": ["title", "description", "due_at", "status"],
            },
        },
    ],
    "update_fields": {
        "title": [
            {
                "name": "title",
                "qtype": "text",
                "prompt": "Enter new title:",
            }
        ],
        "description": [
            {
                "name": "description",
                "qtype": "text",
                "prompt": "Enter new description:",
            }
        ],
        "due_at": [
            {
                "name": "due_at",
                "qtype": "text",
                "prompt": "Enter new due date (YYYY-MM-DD HH:MM:SS):",
            }
        ],
        "status": [
            {
                "name": "status",
                "qtype": "select",
                "prompt": "Select new status:",
                "kwargs": {"choices": [s.value for s in Status]},
            }
        ],
    },
}
