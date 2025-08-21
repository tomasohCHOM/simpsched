from rich.table import Table
from .utils import console


def display_tasks_table(tasks) -> None:
    if not tasks:
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Title", style="bold")
    table.add_column("Description", style="italic")
    table.add_column("Status", style="green")
    table.add_column("Due", style="yellow")

    for t in tasks:
        table.add_row(str(t[0]), t[1], t[2] or "", t[3], t[5] or "—")

    console.print(table)
