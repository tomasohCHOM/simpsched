from datetime import datetime
from prompt_toolkit.validation import Validator, ValidationError
from .db import DatabaseHandler


class ValidationFailedError(ValueError):
    pass


class BaseValidator(Validator):
    task_prompt: str

    def __init__(self, task_prompt: str):
        self.task_prompt = task_prompt

    def check(self, value):
        """
        Reusable validation logic for non-interactive use.
        Should raise ValidationFailedError if invalid.
        """
        raise NotImplementedError

    def validate(self, document):
        """prompt_toolkit calls this for interactive commands."""
        value = document.text
        try:
            self.check(value)
        except ValueError as e:
            raise ValidationError(
                message=str(e),
                cursor_position=len(value),
            )


class InputNotEmptyValidator(BaseValidator):
    def check(self, value):
        if not value or not value.strip():
            raise ValidationFailedError("Input must be non-empty.")


class TaskIdExistsValidator(BaseValidator):
    def check(self, value):
        if (db := DatabaseHandler()) and not db.get_task(value):
            raise ValidationFailedError(f"No task found with id {value}")


class IsValidIsoValidator(BaseValidator):
    FORMATS = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]

    def check(self, value):
        if not value:
            return True
        for fmt in self.FORMATS:
            try:
                datetime.strptime(value, fmt)
                return True
            except ValueError:
                continue
        raise ValidationFailedError(
            "Invalid ISO Date. Date must be in 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS' format"
        )


validators = {
    "add": [InputNotEmptyValidator("title"), IsValidIsoValidator("due_at")],
    "rm": [
        TaskIdExistsValidator("task_id"),
    ],
    "update": [
        TaskIdExistsValidator("task_id"),
        InputNotEmptyValidator("title"),
        IsValidIsoValidator("due_at"),
    ],
}
