import math
import re

email_regex = re.compile(r"^\S+@\S+\.\S+$")
username_regex = re.compile(r"^\w*$")

# Courtesy of codaddict via https://stackoverflow.com/a/5142164
strong_password_regex = re.compile(
    r"^(?=.*[A-Z].*[A-Z])(?=.*[!@#$&*])(?=.*[0-9].*[0-9])(?=.*[a-z].*[a-z].*[a-z]).{8}$"
)


def coerce_empty_string_to_none(value: str) -> str:
    """This validator is used to sanitize HTML forms which will include inputs
    without a value as an empty string; a techncially valid value for many
    models may be invalid in business logic.
    """
    return value if value != "" else None


def nonempty_string(value: str) -> str:
    if value == "":
        raise ValueError("Required text field cannot be empty")
    return value


def positive_float(value: float) -> float:
    if value < 0:
        raise ValueError("Given numeric value must not be less than zero")
    return value


def regex_validator_factory(value, regex, message) -> str:
    if regex.search(value) is None:
        raise ValueError(message)
    return value


def is_email(value: str) -> str:
    return regex_validator_factory(value, email_regex, "Invalid email")


def is_username(value: str) -> str:
    return regex_validator_factory(
        value,
        username_regex,
        "Invalid username. A username should be a single word, allowing for "
        + "numbers, letters, and underscores",
    )


def password_is_strong(value: str) -> str:
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    symbols = "!@#$%^&*()-=_+,./;'[]\\<>?:\"{}|"
    digits = "0123456789"

    has_lowercase = False
    has_uppercase = False
    has_symbol = False
    has_digit = False

    for character in value:
        if character in lowercase or character in uppercase:
            has_lowercase = True
        elif character in symbols:
            has_symbol = True
        elif character in digits:
            has_digit = True
        else:
            continue

    range_ = 0
    if has_lowercase:
        range_ += len(lowercase)
    if has_uppercase:
        range_ += len(uppercase)
    if has_symbol:
        range_ += len(symbols)
    if has_digit:
        range_ += len(digits)

    entropy = len(value) * math.log2(range_)
    if entropy < 100:
        raise ValueError(
            "Password isn't strong enough. You can make your password "
            + "stronger by making it longer and adding upper and lower case "
            + "letters, numbers and symbols"
        )

    return value
