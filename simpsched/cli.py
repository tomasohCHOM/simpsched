import click
import questionary
from .constants import Action
from .db import DatabaseHandler
from .steps import task_prompts, steps
from .utils import run_interactive_steps
from .view import display_logo, display_tasks_table, display_task_message


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Task manager CLI"""
    display_logo()
    if ctx.invoked_subcommand is None:
        display_task_message(
            "Welcome to interactive mode. Choose any of the options to continue:\n"
        )
        interactive_loop()


def interactive_loop() -> None:
    while True:
        action = questionary.select(
            "Select one of the following actions", choices=[a.value for a in Action]
        ).ask()
        if not action:
            break

        match action:
            case Action.ADD.value:
                interactive_add()
            case Action.REMOVE.value:
                interactive_rm()
            case Action.UPDATE.value:
                interactive_update()
            case Action.LIST.value:
                list_tasks()
            case Action.EXIT.value:
                break


# ---------------------------
# Non-interactive commands
# ---------------------------


@cli.command()
@click.option("--title", "-t", help="Task name", type=str, required=True)
@click.option("--desc", "-d", default="", help="Task description", type=str)
@click.option("--due_at", default=None, help="Due date (YYYY-MM-DD HH:MM:SS)", type=str)
def add(title: str, desc: str, due_at: str) -> None:
    """Add a new task"""
    db = DatabaseHandler()
    db.add_task(title, desc, due_at)
    db.close()
    display_task_message(f"Task added: {title}")


@cli.command()
@click.option("--task_id", "-id", type=int, required=True)
def rm(task_id: int) -> None:
    """Remove a task given its id"""
    db = DatabaseHandler()
    db.remove_task(task_id)
    db.close()
    display_task_message(f"Task removed with id: {task_id}")


@click.command()
@click.option("--task_id", type=int, required=True)
@click.option("--title", type=str, help="New title for the task")
@click.option("--desc", type=str, help="New desc")
@click.option("--status", type=str, help="New status")
@click.option("--due_at", type=str, help="New due date (YYYY-MM-DD HH:MM:SS)")
def update(task_id, title, desc=None, status=None, due_at=None):
    """Update a task given its id"""
    updates = {
        k: v
        for k, v in {
            "title": title,
            "desc": desc,
            "status": status,
            "due_at": due_at,
        }.items()
        if v is not None
    }

    db = DatabaseHandler()
    db.update_task(task_id, **updates)
    db.close()

    display_task_message(f"Updated task with id: {task_id}")


@cli.command()
def ls() -> None:
    list_tasks()


# ---------------------------
# Interactive commands
# ---------------------------


def interactive_add() -> None:
    answers = run_interactive_steps(steps["add"])
    if answers is None:
        return
    add.callback(answers["title"], answers["desc"], answers["due_at"] or None)


def interactive_rm() -> None:
    answers = run_interactive_steps(steps["rm"])
    if answers is None or not answers["confirm"]:
        return
    rm.callback(int(answers["task_id"]))


def interactive_update() -> None:
    base_answers = run_interactive_steps(steps["update"])
    if not base_answers or not base_answers["fields"]:
        return
    task_id = base_answers["task_id"]
    selected_fields = base_answers["fields"]
    # Filter prompts based on the chosen fields to update
    prompts = [task_prompts[name] for name in selected_fields]
    answers = run_interactive_steps(prompts)
    if not answers:
        return
    update.callback(task_id, **answers)


def list_tasks():
    """List all tasks"""
    db = DatabaseHandler()
    tasks = db.list_tasks()
    db.close()
    display_tasks_table(tasks)


if __name__ == "__main__":
    cli()
