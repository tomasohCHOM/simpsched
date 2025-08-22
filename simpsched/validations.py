from prompt_toolkit.validation import Validator, ValidationError


class TitleNotEmptyValidator(Validator):
    def is_valid_title(self, title: str) -> bool:
        return len(title) != 0 and title.strip() != ""

    def validate(self, document):
        text = document.text
        if not self.is_valid_title(text):
            raise ValidationError(
                message="Input must be non-empty",
                cursor_position=len(text),
            )


def is_valid_iso_str(iso_str: str) -> bool:
    return True
