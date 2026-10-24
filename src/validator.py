import re

# firstname.lastname@university.com
EMAIL_REGEX = r"^[a-zA-Z]+\.[a-zA-Z]+@university\.com$"

# Starts with an upper-case letter, at least 5 letters in total, then 3 or more digits
PASSWORD_REGEX = r"^[A-Z][a-zA-Z]{4,}[0-9]{3,}$"


class Validator:
    """Regex checks for login and registration."""

    @staticmethod
    def is_valid_email(email):
        """Returns True if the email looks like firstname.lastname@university.com."""
        return email is not None and re.match(EMAIL_REGEX, email) is not None

    @staticmethod
    def is_valid_password(password):
        """Returns True if the password matches PASSWORD_REGEX."""
        return password is not None and re.match(PASSWORD_REGEX, password) is not None
