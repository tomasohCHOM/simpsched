import questionary
from rich.console import Console

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
