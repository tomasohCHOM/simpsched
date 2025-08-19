import click
from typing import Optional
from rich.console import Console
from .constants import Status
from .db import DatabaseHandler


LOGO = """
     _                          _              _ 
 ___(_)_ __ ___  _ __  ___  ___| |__   ___  __| |
/ __| | '_ ` _ \\| '_ \\/ __|/ __| '_ \\ / _ \\/ _` |
\\__ \\ | | | | | | |_) \\__ \\ (__| | | |  __/ (_| |
|___/_|_| |_| |_| .__/|___/\\___|_| |_|\\___|\\__,_|
                |_|
"""

console = Console()


@click.group()
def cli() -> None:
    """Task manager CLI"""
    console.print(LOGO, style="#9bcffa", highlight=False)


@cli.command()
@click.option("--title", "-t", help="Task name", type=str, required=True)
@click.option("--desc", "-d", default="", help="Task description", type=str)
@click.option("--due", default=None, help="Due date (YYYY-MM-DD HH:MM:SS)", type=str)
def add(title: str, desc: str, due: str) -> None:
    """Add a new task"""
    db = DatabaseHandler()
    db.add_task(title, desc, due)
    db.close()
    print(f"Task added: {title}")


@cli.command()
@click.option("--task_id", "-id", type=int, required=True)
def rm(task_id: int) -> None:
    """Remove a task given its id"""
    db = DatabaseHandler()
    db.remove_task(task_id)
    db.close()
    print(f"Task removed with id: {task_id}")


@cli.command()
@click.option("--task_id", "-id", type=int, required=True)
@click.option("--status", "-s", type=click.Choice([e.value for e in Status]))
@click.option("--due", default=None, help="Due date (YYYY-MM-DD HH:MM:SS)", type=str)
def update(task_id: int, status: Optional[str], due: Optional[str]):
    """Update the status of a task with its id"""
    db = DatabaseHandler()
    if due:
        db.update_due_at(task_id, due)
    if status:
        db.update_status(task_id, status)
    db.close()
    print(f"Updated status of task with id {task_id}")


@cli.command()
def ls() -> None:
    """List all tasks"""
    db = DatabaseHandler()
    tasks = db.list_tasks()
    db.close()
    if not tasks:
        click.echo("No tasks found")
        return
    for t in tasks:
        click.echo(f"[{t[0]}] {t[1]} ({t[3]}) - due {t[5]}")


if __name__ == "__main__":
    cli()
