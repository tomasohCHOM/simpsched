import questionary
from datetime import datetime, timedelta
from typing import List
from .constants import Status, STATUS_PRIORITY
from .db import DatabaseHandler
from .models import Task
from .validations import BaseValidator, validators


def run_interactive_steps(steps):
    """
    Run a sequence of `steps`. Each step is a dict with:
    - `name` (str): key for the answer dict
    - `qtype` (str): 'text', 'confirm', 'select', etc.
    - `prompt` (str): the prompt text
    - `kwargs` (dict, optional): extra arguments (validators, choices, etc.)

    Returns dict of `answers` or None if cancelled.
    """
    answers = {}
    try:
        for step in steps:
            qtype = step["qtype"]
            message = step["prompt"]
            kwargs = step.get("kwargs", {})

            prompt_func = getattr(questionary, qtype)
            answer = prompt_func(message, **kwargs).ask()

            if answer is None:
                raise KeyboardInterrupt

            answers[step["name"]] = answer

        return answers

    except KeyboardInterrupt:
        return None


def run_validations(command: str, data: dict):
    """Run all validations for the given command"""
    cmd_validators: List[BaseValidator] = validators.get(command, [])
    for validator in cmd_validators:
        if validator.task_prompt in data and data[validator.task_prompt] is not None:
            validator.check(data[validator.task_prompt])


def remove_inactive_tasks() -> List[str]:
    db = DatabaseHandler()
    tasks = db.list_tasks()
    cutoff = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    removable_tasks = [
        task
        for task in tasks
        if task.status in [Status.CANCELLED.value, Status.DONE.value]
        and datetime.strptime(task.updated_at, "%Y-%m-%d %H:%M:%S") < cutoff
    ]
    for task in removable_tasks:
        db.remove_task(task.id)
    db.close()
    return [task.title for task in removable_tasks]


def process_iso_date(date: str) -> str:
    return date if not date or len(date.split()) > 1 else date + " 23:59:59"


def get_due_status(due_at: str) -> List[str]:
    """Takes `due_at` as argument and determines its due status (and its corresponding color)"""
    if not due_at:
        return "", ""
    diff = datetime.strptime(due_at, "%Y-%m-%d %H:%M:%S") - datetime.now()
    if diff.total_seconds() < 0:
        return "overdue", "red"
    elif diff <= timedelta(hours=6):
        return "due soon", "yellow"
    return "on time", "white"


def sort_tasks(tasks: List[Task]) -> List[Task]:
    return sorted(
        tasks,
        key=lambda t: (
            t.due_at is None or t.due_at == "",
            t.due_at or datetime.max,
            STATUS_PRIORITY.get(t.status, 99),
            t.title.lower(),
        ),
    )
