import click
import questionary
from typing import Optional
from .constants import Action, Status, USER_PROMPTS
from .db import DatabaseHandler
from .steps import steps
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
@click.option("--due", default=None, help="Due date (YYYY-MM-DD HH:MM:SS)", type=str)
def add(title: str, desc: str, due: str) -> None:
    """Add a new task"""
    db = DatabaseHandler()
    db.add_task(title, desc, due)
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
@click.option("--description", type=str, help="New description")
@click.option("--status", type=str, help="New status")
@click.option("--due_at", type=str, help="New due date (YYYY-MM-DD HH:MM:SS)")
def update(task_id, title, description=None, status=None, due_at=None):
    """Update a task given its id"""
    updates = {}
    if title is not None:
        updates["title"] = title
    if description is not None:
        updates["description"] = description
    if status is not None:
        updates["status"] = status
    if due_at is not None:
        updates["due_at"] = due_at

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
    if answers is None or not answers["confirm"]:
        return
    add.callback(answers["title"], answers["desc"], answers["due"] or None)


def interactive_rm() -> None:
    answers = run_interactive_steps(steps["rm"])
    if answers is None or not answers["confirm"]:
        return

    rm.callback(int(answers["task_id"]))


def interactive_update() -> None:
    task_id = questionary.text("Enter task ID to update:").ask()
    if task_id is None:
        return

    chosen = run_interactive_steps(steps["update"])
    if chosen is None:
        return

    fields = chosen["fields"]
    if not fields:
        display_task_message("No fields selected.")
        return

    updates = {}
    for field in fields:
        answer = run_interactive_steps(steps["update_fields"][field])
        if not answer:
            return
        updates.update(answer)

    update.callback(task_id, **updates)


def list_tasks():
    """List all tasks"""
    db = DatabaseHandler()
    tasks = db.list_tasks()
    db.close()
    display_tasks_table(tasks)


if __name__ == "__main__":
    cli()
