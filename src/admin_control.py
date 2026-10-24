from message_handler import MessageHandler as msg, RED, RESET

GRADE_ORDER = ["HD", "D", "C", "P", "Z"]
NOTHING = "< Nothing to Display >"


class AdminControl:
    """Admin menu (c/g/p/r/s/x). Every action reads students.data first."""

    def __init__(self, db):
        """db: the EnrolmentSystem that reads and writes students.data."""
        self.db = db

    def run(self):
        """Shows the admin menu and runs the chosen action until the admin types x."""
        while True:
            choice = msg.prompt("Admin System: (c)lear database, (g)roup students, (p)artition students, (r)emove student, (s)how students, or (x) exit: ", 1).strip().lower()
            if choice == "c":
                self.clear()
            elif choice == "g":
                self.group()
            elif choice == "p":
                self.partition()
            elif choice == "r":
                self.remove()
            elif choice == "s":
                self.show()
            elif choice == "x":
                return
            else:
                msg.error("Invalid option, please choose c, g, p, r, s or x", 1)

    def students(self):
        """Reads students.data and returns all students."""
        self.db.load_data()
        return self.db.get_students()

    def clear(self):
        """Asks for confirmation, then removes all students from students.data."""
        msg.info("Clearing students database", 1)
        answer = msg.prompt(RED + "Are you sure you want to clear the database (Y)ES/(N)O: " + RESET, 1)
        if answer.strip().lower() in ("y", "yes"):
            self.db.clear_students()
            msg.info("Students data cleared", 1)
        else:
            msg.info("Clearing cancelled", 1)

    def group(self):
        """Prints students grouped by their overall grade (HD, D, C, P, Z)."""
        msg.info("Grade Grouping", 1)
        students = self.students()
        if not students:
            msg.message(NOTHING, 1)
            return
        for grade in GRADE_ORDER:
            in_grade = [str(s) for s in students if s.overall_grade() == grade]
            if in_grade:
                msg.message(f"{grade:<2} --> [{', '.join(in_grade)}]", 1)

    def partition(self):
        """Prints students split into FAIL (average < 50) and PASS lists."""
        msg.info("PASS/FAIL Partition", 1)
        students = self.students()
        failed = [str(s) for s in students if not s.is_pass()]
        passed = [str(s) for s in students if s.is_pass()]
        msg.message(f"FAIL --> [{', '.join(failed)}]", 1)
        msg.message(f"PASS --> [{', '.join(passed)}]", 1)

    def remove(self):
        """Asks for a student id and removes that student from students.data."""
        student_id = msg.prompt("Remove by ID: ", 1).strip()
        self.db.load_data()
        if self.db.remove_student(student_id):
            msg.info(f"Removing Student {student_id} Account", 1)
        else:
            msg.error(f"Student {student_id} does not exist", 1)

    def show(self):
        """Prints every student's name, id and email."""
        msg.info("Student List", 1)
        students = self.students()
        if not students:
            msg.message(NOTHING, 1)
            return
        for s in students:
            msg.message(f"{s.name} :: {s.student_id} --> Email: {s.email}", 1)
