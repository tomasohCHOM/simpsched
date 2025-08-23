import click
import questionary
from typing import Optional
from .constants import Action, Status, FLAGS, HELP
from .db import DatabaseHandler
from .steps import task_prompts, steps
from .utils import run_interactive_steps, run_validations, process_iso_date, sort_tasks
from .validations import ValidationFailedError
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
@click.option(FLAGS["title"], help=HELP["title"], required=True)
@click.option(FLAGS["desc"], help=HELP["desc"], default="")
@click.option(
    FLAGS["status"],
    help=HELP["status"],
    type=click.Choice([s.value for s in Status]),
    default=Status.PENDING.value,
)
@click.option(FLAGS["due_at"], help=HELP["due_at"], default=None)
def add(
    title: str,
    desc: str,
    status: str,
    due_at: Optional[str] = None,
) -> None:
    """Add a new task"""
    db = DatabaseHandler()
    try:
        run_validations("add", {"title": title, "due_at": due_at})
    except ValidationFailedError as e:
        display_task_message(str(e))
        return
    db.add_task(title, desc, status, process_iso_date(due_at))
    db.close()
    display_task_message(f"Task added: {title}")
    list_tasks()


@cli.command()
@click.option(FLAGS["id"], help=HELP["id"], type=int, required=True)
def rm(id: int) -> None:
    """Remove a task given its id"""
    try:
        run_validations("rm", {"task_id": id})
    except ValidationFailedError as e:
        display_task_message(str(e))
        return
    db = DatabaseHandler()
    db.remove_task(id)
    db.close()
    display_task_message(f"Task removed with id: {id}")
    list_tasks()


@cli.command()
@click.option(FLAGS["id"], help=HELP["id"], type=int, required=True)
@click.option(FLAGS["title"], help=HELP["title"])
@click.option(FLAGS["desc"], help=HELP["desc"])
@click.option(
    FLAGS["status"],
    type=click.Choice([s.value for s in Status]),
    default=Status.PENDING.value,
    help=HELP["status"],
)
@click.option(FLAGS["due_at"], help=HELP["due_at"])
def update(
    id: int,
    title: Optional[str] = None,
    desc: Optional[str] = None,
    status: Optional[str] = None,
    due_at: Optional[str] = None,
) -> None:
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
    try:
        run_validations("update", {"task_id": id, **updates})
    except ValidationFailedError as e:
        display_task_message(str(e))
        return
    db = DatabaseHandler()
    db.update_task(id, **updates)
    db.close()
    display_task_message(f"Updated task with id: {id}")
    list_tasks()


@cli.command()
def ls() -> None:
    """List all available tasks"""
    list_tasks()


# ---------------------------
# Interactive commands
# ---------------------------


def interactive_add() -> None:
    answers = run_interactive_steps(steps["add"])
    if answers is None:
        return
    add.callback(**answers)


def interactive_rm() -> None:
    answers = run_interactive_steps(steps["rm"])
    if answers is None or not answers["confirm"]:
        return
    rm.callback(int(answers["task_id"]))


def interactive_update() -> None:
    base_answers = run_interactive_steps(steps["update"])
    if not base_answers or not base_answers["fields"]:
        return
    task_id = int(base_answers["task_id"])
    selected_fields = base_answers["fields"]
    # Filter prompts based on the chosen fields to update
    prompts = [task_prompts[name] for name in selected_fields]
    answers = run_interactive_steps(prompts)
    if not answers:
        return
    update.callback(task_id, **answers)


def list_tasks() -> None:
    db = DatabaseHandler()
    tasks = db.list_tasks()
    db.close()
    display_tasks_table(sort_tasks(tasks))


if __name__ == "__main__":
    cli()
