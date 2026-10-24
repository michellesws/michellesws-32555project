from message_handler import MessageHandler as msg
from student import MAX_SUBJECTS
from subject import Subject
from validator import Validator


class StudentEnrolmentControl:
    """Subject enrolment menu for a logged-in student (c/e/r/s/x).

    Every change is saved to students.data straight away.
    """

    def __init__(self, db, student):
        """db: the EnrolmentSystem; student: the logged-in Student."""
        self.db = db
        self.student = student

    def run(self):
        """Shows the enrolment menu and runs the chosen action until the student types x."""
        while True:
            choice = msg.prompt("Student Course Menu: (c)hange password, (e)nrol, (r)emove subject, (s)how subjects, or (x) exit: ", 2).strip().lower()
            if choice != "x" and not self.reload_student():
                msg.error("Student account no longer exists", 2)
                return
            if choice == "c":
                self.change_password()
            elif choice == "e":
                self.enrol()
            elif choice == "r":
                self.remove()
            elif choice == "s":
                self.show()
            elif choice == "x":
                return
            else:
                msg.error("Invalid option, please choose c, e, r, s or x", 2)

    def reload_student(self):
        """Re-reads students.data so saving never brings back students an admin removed or cleared."""
        self.db.load_data()
        self.student = self.db.find_student(self.student.student_id)
        return self.student is not None

    def show_count(self):
        """Prints how many subjects the student is enrolled in."""
        msg.info(f"You are now enrolled in {len(self.student.subjects)} out of {MAX_SUBJECTS} subjects", 2)

    def change_password(self):
        """Asks for a new password until it is valid and confirmed, then saves it."""
        msg.info("Updating Password", 2)
        while True:
            new_password = msg.prompt("New Password: ", 2).strip()
            if not Validator.is_valid_password(new_password):
                msg.error("Incorrect password format", 2)
                continue
            confirm = msg.prompt("Confirm Password: ", 2).strip()
            if new_password != confirm:
                msg.error("Password does not match - try again", 2)
                continue
            break
        self.student.password = new_password
        self.db.save_data()

    def enrol(self):
        """Enrols the student in a new random subject (max 4) and saves."""
        if not self.student.can_enrol():
            msg.error(f"Students are allowed to enrol in {MAX_SUBJECTS} subjects only", 2)
            return
        try:
            subject = Subject(self.db.generate_subject_id())
        except RuntimeError:
            msg.error("No subject ids left, cannot enrol", 2)
            return
        self.student.enrol(subject)
        self.db.save_data()
        msg.info(f"Enrolling in Subject-{subject.subject_id}", 2)
        self.show_count()

    def remove(self):
        """Asks for a subject id and removes that subject from the student's enrolment."""
        subject_id = msg.prompt("Remove Subject by ID: ", 2).strip()
        if not self.student.remove_subject(subject_id):
            msg.error(f"Subject {subject_id} does not exist", 2)
            return
        self.db.save_data()
        msg.info(f"Droping Subject-{subject_id}", 2)
        self.show_count()

    def show(self):
        """Prints all enrolled subjects with their marks and grades."""
        msg.info(f"Showing {len(self.student.subjects)} subjects", 2)
        for subject in self.student.subjects:
            msg.message(str(subject), 2)
