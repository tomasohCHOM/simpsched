import click
import questionary
from typing import Optional
from .constants import Action, Status
from .db import DatabaseHandler
from .utils import console
from .view import display_tasks_table


LOGO = """
     _                          _              _ 
 ___(_)_ __ ___  _ __  ___  ___| |__   ___  __| |
/ __| | '_ ` _ \\| '_ \\/ __|/ __| '_ \\ / _ \\/ _` |
\\__ \\ | | | | | | |_) \\__ \\ (__| | | |  __/ (_| |
|___/_|_| |_| |_| .__/|___/\\___|_| |_|\\___|\\__,_|
                |_|
"""


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Task manager CLI"""
    console.print(LOGO, style="#9bcffa", highlight=False)
    if ctx.invoked_subcommand is None:
        console.print(
            "Welcome to interactive mode. Choose any of the options to continue:\n"
        )
        interactive_loop()


def interactive_loop() -> None:
    while True:
        action = questionary.select(
            "Select one of the following actions", choices=[e.value for e in Action]
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
    click.echo(f"Task added: {title}")


@cli.command()
@click.option("--task_id", "-id", type=int, required=True)
def rm(task_id: int) -> None:
    """Remove a task given its id"""
    db = DatabaseHandler()
    db.remove_task(task_id)
    db.close()
    click.echo(f"Task removed with id: {task_id}")


@cli.command()
@click.option("--task_id", "-id", type=int, required=True)
@click.option("--status", "-s", type=click.Choice([e.value for e in Status]))
@click.option("--due", default=None, help="Due date (YYYY-MM-DD HH:MM:SS)", type=str)
def update(task_id: int, status: Optional[str], due: Optional[str]):
    """Update the status or due date of a task"""
    db = DatabaseHandler()
    if due:
        db.update_due_at(task_id, due)
    if status:
        db.update_status(task_id, status)
    db.close()
    click.echo(f"Updated task with id {task_id}")


@cli.command()
def ls() -> None:
    list_tasks()


# ---------------------------
# Interactive wrappers
# ---------------------------


def interactive_add() -> None:
    title = questionary.text("Enter task title:").ask()
    desc = questionary.text("Enter description (optional):").ask()
    due = questionary.text("Enter due date (YYYY-MM-DD HH:MM:SS) (optional):").ask()
    add.callback(title, desc or "", due or None)


def interactive_rm() -> None:
    task_id = questionary.text("Enter task id to remove:").ask()
    rm.callback(int(task_id))


def interactive_update() -> None:
    task_id = int(questionary.text("Enter task id to update:").ask())
    status = questionary.select(
        "Select new status", choices=[e.value for e in Status]
    ).ask()
    due = questionary.text("Enter new due date (optional):").ask()
    update.callback(task_id, status or None, due or None)


def list_tasks():
    """List all tasks"""
    db = DatabaseHandler()
    tasks = db.list_tasks()
    db.close()
    display_tasks_table(tasks)


if __name__ == "__main__":
    cli()
