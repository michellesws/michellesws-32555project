"""CLIUniApp entry point. Run from the folder where students.data should live, e.g. `python src/App.py`."""
import os

from admin_control import AdminControl
from enrolment_system import EnrolmentSystem
from message_handler import MessageHandler as msg
from student_account_control import StudentAccountControl


def main():
    """Shows the university menu and opens the admin or student menu until the user exits."""
    
    db = EnrolmentSystem()
    try:
        while True:
            choice = msg.prompt("University System: (A)dmin, (S)tudent, or (X) exit: ").strip().upper()
            if choice == "A":
                AdminControl(db).run()
            elif choice == "S":
                StudentAccountControl(db).run()
            elif choice == "X":
                break
            else:
                msg.error("Invalid option, please choose A, S or X")
    except (KeyboardInterrupt, EOFError):
        print()
    msg.info("Thank You")


if __name__ == "__main__":
    main()
