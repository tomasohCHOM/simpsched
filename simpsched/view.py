from rich.console import Console
from rich.table import Table
from rich import box
from typing import List
from .constants import STATUS_COLORS, Status
from .models import Task
from .utils import get_due_status


LOGO = """
     _                          _              _ 
 ___(_)_ __ ___  _ __  ___  ___| |__   ___  __| |
/ __| | '_ ` _ \\| '_ \\/ __|/ __| '_ \\ / _ \\/ _` |
\\__ \\ | | | | | | |_) \\__ \\ (__| | | |  __/ (_| |
|___/_|_| |_| |_| .__/|___/\\___|_| |_|\\___|\\__,_|
                |_|
"""

console = Console()


def display_tasks_table(tasks: List[Task]) -> None:
    if not tasks:
        display_task_message("No tasks to show.")
        return

    table = Table(
        title="Tasks",
        show_header=True,
        header_style="bold cyan",
        box=box.SQUARE,
        show_lines=True,
    )
    table.add_column("ID", style="dim")
    table.add_column("Title", style="bold")
    table.add_column("Description", style="italic")
    table.add_column("Status", style="bold")
    table.add_column("Due")

    for task in tasks:
        status_color = STATUS_COLORS.get(task.status, "white")
        due_display = "-"
        if task.status in [Status.CANCELLED.value, Status.DONE.value]:
            due_display = task.due_at if task.due_at else "-"
        elif task.due_at:
            due_status, due_status_color = get_due_status(task.due_at)
            due_display = (
                f"{task.due_at} [{due_status_color}]({due_status})[/{due_status_color}]"
                if due_status
                else task.due_at
            )
        table.add_row(
            str(task.id),
            task.title,
            task.desc or "-",
            f"[{status_color}]{task.status}[/{status_color}]",
            due_display,
        )

    console.print()
    console.print(table)
    console.print()


def display_logo() -> None:
    console.print(LOGO, style="#9bcffa", highlight=False)


def display_task_message(message: str) -> None:
    console.print(f"\n{message}\n", style="italic")
