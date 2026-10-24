import random

MIN_MARK = 25
MAX_MARK = 100


def grade_for(mark):
    """UTS grading: HD >= 85, D >= 75, C >= 65, P >= 50, otherwise Z (fail)."""
    if mark >= 85:
        return "HD"
    if mark >= 75:
        return "D"
    if mark >= 65:
        return "C"
    if mark >= 50:
        return "P"
    return "Z"


class Subject:
    """A subject a student is enrolled in.

    The mark (25-100) is generated randomly on creation and the grade is derived from it.
    """

    def __init__(self, subject_id, mark=None):
        """Creates a subject; a random mark is generated unless one is given."""
        # subject_id: unique 3-digit id, e.g. from EnrolmentSystem.generate_subject_id()
        # mark: only passed when loading from students.data
        self.subject_id = subject_id
        self.mark = mark if mark is not None else random.randint(MIN_MARK, MAX_MARK)
        self.grade = self.calculate_grade()

    def calculate_grade(self):
        """Returns the grade for this subject's mark."""
        return grade_for(self.mark)

    def to_dict(self):
        """Converts the subject to a dict so it can be saved as JSON."""
        return {"id": self.subject_id, "mark": self.mark, "grade": self.grade}

    @classmethod
    def from_dict(cls, data):
        """Creates a subject from a dict read from students.data."""
        # the grade is saved for readability; it is recalculated from the mark
        return cls(data["id"], data["mark"])

    def __str__(self):
        """Text used in the enrolment menu, e.g. [ Subject::123 -- mark = 78 -- grade =  D ]"""
        return f"[ Subject::{self.subject_id} -- mark = {self.mark} -- grade = {self.grade:>2} ]"
