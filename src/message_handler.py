RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"

INDENT = "        "


class MessageHandler:
    """Console output in one place so every menu uses the same colours and indentation.

    indent: 0 = university menu, 1 = student/admin menu, 2 = enrolment menu.
    """

    @staticmethod
    def message(text, indent=0):
        """Prints plain text at the given indent level."""
        print(INDENT * indent + text)

    @staticmethod
    def prompt(text, indent=0):
        """Shows a menu prompt, e.g. "Student System (l/r/x): ", and returns what the user types."""
        return input(INDENT * indent + CYAN + text + RESET)

    @staticmethod
    def info(text, indent=0):
        """Prints text in yellow (general information)."""
        MessageHandler.message(YELLOW + text + RESET, indent)

    @staticmethod
    def success(text, indent=0):
        """Prints text in green (headings such as Student Sign Up)."""
        MessageHandler.message(GREEN + text + RESET, indent)

    @staticmethod
    def error(text, indent=0):
        """Prints text in red (errors)."""
        MessageHandler.message(RED + text + RESET, indent)
