from rich.table import Table
from rich import box
from typing import List
from .constants import STATUS_COLORS
from .db import Task
from .utils import console


def display_tasks_table(tasks: List[Task]) -> None:
    if not tasks:
        console.print("No tasks to show.")
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
    table.add_column("Status")
    table.add_column("Due")

    for task in tasks:
        status_color = STATUS_COLORS.get(task.status, "white")
        table.add_row(
            str(task.id),
            task.title,
            task.description or "",
            f"[{status_color}]{task.status}[/{status_color}]",
            task.due_at or "—",
        )

    console.print(table)
