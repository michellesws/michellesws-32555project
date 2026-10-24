"""GUIUniApp: login, enrolment, subject and exception windows for registered students.

Uses the same students.data as CLIUniApp, so run it from the same folder, e.g. `python src/GUIUniApp.py`.
"""
import tkinter as tk
from tkinter import ttk

from enrolment_system import EnrolmentSystem
from student import MAX_SUBJECTS
from subject import Subject
from validator import Validator


class ExceptionWindow(tk.Toplevel):
    """Modal window that shows an error message."""

    def __init__(self, parent, title, message):
        """Builds the error window with the message and an OK button."""
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.transient(parent)
        ttk.Label(self, text=message, foreground="red", padding=20, wraplength=320).pack()
        ttk.Button(self, text="OK", command=self.destroy).pack(pady=(0, 15))
        self.bind("<Return>", lambda e: self.destroy())
        self.grab_set()
        self.focus_set()


class LoginWindow:
    """Main window: students log in with an email and password stored in students.data."""

    def __init__(self, root):
        """Builds the login form with email and password fields and a Login button."""
        self.root = root
        root.title("GUIUniApp - Login")
        root.resizable(False, False)

        frame = ttk.Frame(root, padding=20)
        frame.pack()
        ttk.Label(frame, text="Student Login", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15))
        ttk.Label(frame, text="Email:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.email = ttk.Entry(frame, width=32)
        self.email.grid(row=1, column=1, pady=5)
        ttk.Label(frame, text="Password:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.password = ttk.Entry(frame, width=32, show="*")
        self.password.grid(row=2, column=1, pady=5)
        ttk.Button(frame, text="Login", command=self.login).grid(row=3, column=0, columnspan=2, pady=(15, 0))

        root.bind("<Return>", lambda e: self.login())
        self.email.focus_set()

    def login(self):
        """Checks the fields and credentials, then opens the enrolment window or shows an error."""
        email = self.email.get().strip()
        password = self.password.get().strip()
        if not email or not password:
            ExceptionWindow(self.root, "Login Error", "Email and password cannot be empty.")
            return
        if not Validator.is_valid_email(email):
            ExceptionWindow(self.root, "Format Error", "Incorrect email format.\nExample: firstname.lastname@university.com")
            return
        if not Validator.is_valid_password(password):
            ExceptionWindow(self.root, "Format Error",
                            "Incorrect password format.\nIt must start with an upper-case letter, "
                            "have at least 5 letters and end with 3 or more digits.")
            return

        db = EnrolmentSystem()  # reads students.data, including students registered in CLIUniApp
        student = db.find_student_by_email(email)
        if student is None or student.password != password:
            ExceptionWindow(self.root, "Login Error", "Incorrect student credentials.")
            return

        self.password.delete(0, tk.END)
        self.root.withdraw()
        EnrolmentWindow(self.root, db, student)


class EnrolmentWindow(tk.Toplevel):
    """Lets a logged-in student enrol in up to MAX_SUBJECTS subjects."""

    def __init__(self, root, db, student):
        """Builds the window with the student's details, enrolment list and buttons."""
        super().__init__(root)
        self.root = root
        self.db = db
        self.student = student
        self.title("GUIUniApp - Enrolment")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.logout)

        frame = ttk.Frame(self, padding=20)
        frame.pack()
        ttk.Label(frame, text=f"Welcome, {student.name} ({student.student_id})",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w")
        self.count = ttk.Label(frame)
        self.count.pack(anchor="w", pady=(5, 10))

        ttk.Label(frame, text="Enrolment list:").pack(anchor="w")
        self.subjects = tk.Listbox(frame, width=40, height=MAX_SUBJECTS)
        self.subjects.pack(pady=(0, 10))

        buttons = ttk.Frame(frame)
        buttons.pack()
        ttk.Button(buttons, text="Enrol", command=self.enrol).pack(side="left", padx=5)
        ttk.Button(buttons, text="Show Subjects", command=self.show_subjects).pack(side="left", padx=5)
        ttk.Button(buttons, text="Logout", command=self.logout).pack(side="left", padx=5)
        self.refresh()

    def refresh(self):
        """Updates the enrolment count and the list of enrolled subjects."""
        self.count.config(text=f"Enrolled in {len(self.student.subjects)} out of {MAX_SUBJECTS} subjects")
        self.subjects.delete(0, tk.END)
        for subject in self.student.subjects:
            self.subjects.insert(tk.END, f"Subject-{subject.subject_id}")

    def reload_student(self):
        """Re-reads students.data so saving never brings back students an admin removed or cleared.

        Returns False (and logs out) if this student no longer exists.
        """
        self.db.load_data()
        self.student = self.db.find_student(self.student.student_id)
        if self.student is None:
            ExceptionWindow(self.root, "Account Error", "Student account no longer exists.")
            self.logout()
            return False
        return True

    def enrol(self):
        """Enrols the student in a new random subject, or shows an error if already in 4 subjects."""
        if not self.reload_student():
            return
        if not self.student.can_enrol():
            ExceptionWindow(self, "Enrolment Error", f"Students are allowed to enrol in {MAX_SUBJECTS} subjects only.")
            return
        self.student.enrol(Subject(self.db.generate_subject_id()))
        self.db.save_data()
        self.refresh()

    def show_subjects(self):
        """Opens the subject window with the student's marks and grades."""
        if self.reload_student():
            SubjectWindow(self, self.student)

    def logout(self):
        """Closes the enrolment window and shows the login window again."""
        self.destroy()
        self.root.deiconify()


class SubjectWindow(tk.Toplevel):
    """Lists the student's enrolled subjects with their marks and grades."""

    def __init__(self, parent, student):
        """Builds a table of the enrolled subjects with their marks and grades."""
        super().__init__(parent)
        self.title("GUIUniApp - Subjects")
        self.resizable(False, False)
        self.transient(parent)

        frame = ttk.Frame(self, padding=20)
        frame.pack()
        ttk.Label(frame, text=f"Showing {len(student.subjects)} subjects").pack(anchor="w", pady=(0, 10))
        table = ttk.Treeview(frame, columns=("id", "mark", "grade"), show="headings", height=MAX_SUBJECTS)
        for column, heading in (("id", "Subject"), ("mark", "Mark"), ("grade", "Grade")):
            table.heading(column, text=heading)
            table.column(column, width=100, anchor="center")
        for subject in student.subjects:
            table.insert("", tk.END, values=(subject.subject_id, subject.mark, subject.grade))
        table.pack()
        ttk.Label(frame, text=f"Average mark: {student.average_mark():.2f}   Grade: {student.overall_grade()}").pack(anchor="w", pady=(10, 0))
        ttk.Button(frame, text="Close", command=self.destroy).pack(pady=(15, 0))


def main():
    """Opens the login window and starts the GUI."""
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
