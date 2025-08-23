import questionary
from typing import List
from rich.console import Console
from .steps import validators
from .validations import BaseValidator

console = Console()


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


def process_iso_date(date: str) -> str:
    return date if len(date.split()) > 1 else date + " 23:59:59"
