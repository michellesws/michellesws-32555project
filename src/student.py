from subject import Subject, grade_for

MAX_SUBJECTS = 4
PASS_MARK = 50


class Student:
    """A registered student and their subject enrolments.

    Stored as JSON in students.data by EnrolmentSystem.
    """

    def __init__(self, student_id, name, email, password, subjects=None):
        # student_id: unique 6-digit id, e.g. from EnrolmentSystem.generate_student_id()
        self.student_id = student_id
        self.name = name
        self.email = email
        self.password = password
        self.subjects = subjects if subjects is not None else []

    def can_enrol(self):
        return len(self.subjects) < MAX_SUBJECTS

    def enrol(self, subject):
        """Adds a subject. Returns False if already enrolled in MAX_SUBJECTS subjects."""
        if not self.can_enrol():
            return False
        self.subjects.append(subject)
        return True

    def remove_subject(self, subject_id):
        """Returns False if the student is not enrolled in a subject with this id."""
        for subject in self.subjects:
            if subject.subject_id == subject_id:
                self.subjects.remove(subject)
                return True
        return False

    def average_mark(self):
        """Average mark of all enrolled subjects (0 if none)."""
        if not self.subjects:
            return 0
        return sum(s.mark for s in self.subjects) / len(self.subjects)

    def overall_grade(self):
        return grade_for(self.average_mark())

    def is_pass(self):
        return self.average_mark() >= PASS_MARK

    def to_dict(self):
        return {
            "id": self.student_id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "subjects": [s.to_dict() for s in self.subjects],
        }

    @classmethod
    def from_dict(cls, data):
        subjects = [Subject.from_dict(s) for s in data.get("subjects", [])]
        return cls(data["id"], data["name"], data["email"], data["password"], subjects)

    def __str__(self):
        return (f"{self.name} :: {self.student_id} --> "
                f"GRADE: {self.overall_grade():>2} - MARK: {self.average_mark():.2f}")
