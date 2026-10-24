from message_handler import MessageHandler as msg
from student import Student
from student_enrolment_control import StudentEnrolmentControl
from validator import Validator


class StudentAccountControl:
    """Student menu: login / register (l/r/x)."""

    def __init__(self, db):
        """db: the EnrolmentSystem that reads and writes students.data."""
        self.db = db

    def run(self):
        """Shows the student menu and runs login or register until the student types x."""
        while True:
            choice = msg.prompt("Student System: (l)ogin, (r)egister, or (x) exit: ", 1).strip().lower()
            if choice == "l":
                self.login()
            elif choice == "r":
                self.register()
            elif choice == "x":
                return
            else:
                msg.error("Invalid option, please choose l, r or x", 1)

    def read_credentials(self, email_prompt="Email: "):
        """Asks for email and password; returns None if either has the wrong format."""
        email = msg.prompt(email_prompt, 1).strip()
        if email.lower() == "x":
            return "exit"
        password = msg.prompt("Password: ", 1).strip()
        if not (Validator.is_valid_email(email) and Validator.is_valid_password(password)):
            msg.error("Incorrect email or password format", 1)
            return None
        msg.info("email and password formats acceptable", 1)
        return email, password

    def register(self):
        """Keeps asking until the student is registered, or the user types x as the email."""
        msg.success("Student Sign Up", 1)
        while True:
            credentials = self.read_credentials("Email (or x to go back): ")
            if credentials == "exit":
                return
            if credentials is None:
                continue
            email, password = credentials

            self.db.load_data()
            existing = self.db.find_student_by_email(email)
            if existing is not None:
                msg.error(f"Student {existing.name} already exists", 1)
                continue

            name = msg.prompt("Name: ", 1).strip()
            if not name:
                msg.error("Name cannot be empty", 1)
                continue
            try:
                student_id = self.db.generate_student_id()
            except RuntimeError:
                msg.error("No student ids left, cannot register", 1)
                return
            msg.info(f"Enrolling Student {name}", 1)
            self.db.add_student(Student(student_id, name, email, password))
            return

    def login(self):
        """Checks the credentials against students.data and opens the enrolment menu if they match."""
        msg.success("Student Sign In", 1)
        credentials = self.read_credentials()
        if credentials is None or credentials == "exit":
            return
        email, password = credentials

        self.db.load_data()
        student = self.db.find_student_by_email(email)
        if student is None or student.password != password:
            msg.error("Student does not exist", 1)
            return
        StudentEnrolmentControl(self.db, student).run()
