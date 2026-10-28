import base64
import hashlib
import json
import os
import random
import sys

from student import Student

FILE_NAME = "students.data"
SECRET_KEY = b"32555-uni-enrolment-key"


class EnrolmentSystem:
    """The "Database" class: owns the list of students and keeps it in sync with students.data.

    students.data holds a JSON array of students, each with their subjects,
    encoded with encode()/decode() so the raw data cannot be read by opening the file.
    Every method that changes data saves to the file straight away.

    If you change a Student you got from find_student()/find_student_by_email()
    (enrol, remove_subject, password), call save_data() afterwards.
    """

    def __init__(self, file_name=FILE_NAME):
        """Loads students.data (creating it if missing)."""
        self.file_name = file_name
        self.students = []
        self.used_student_ids = set()
        self.used_subject_ids = set()
        self.load_data()

    def load_data(self):
        """Creates students.data if it does not exist, then reads all students from it."""
        self.students = []
        if not os.path.exists(self.file_name):
            self.save_data()
            return
        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                text = f.read()
            if text.strip():
                self.students = [Student.from_dict(d) for d in json.loads(self.decode(text))]
        except (OSError, ValueError, KeyError, TypeError) as e:
            print(f"Could not read {self.file_name}: {e}", file=sys.stderr)
            self.students = []
        self._rebuild_used_ids()

    def save_data(self):
        """Writes all students to students.data as encoded JSON."""
        try:
            text = json.dumps([s.to_dict() for s in self.students])
            with open(self.file_name, "w", encoding="utf-8") as f:
                f.write(self.encode(text))
        except OSError as e:
            print(f"Could not write {self.file_name}: {e}", file=sys.stderr)
        self._rebuild_used_ids()

    @staticmethod
    def _keystream(length):
        """Returns length bytes derived from SECRET_KEY (SHA-256 of key + block counter)."""
        stream = b""
        counter = 0
        while len(stream) < length:
            stream += hashlib.sha256(SECRET_KEY + counter.to_bytes(4, "big")).digest()
            counter += 1
        return stream[:length]

    @classmethod
    def encode(cls, text):
        """XORs the text with the keystream and returns it as base64."""
        data = text.encode("utf-8")
        scrambled = bytes(a ^ b for a, b in zip(data, cls._keystream(len(data))))
        return base64.b64encode(scrambled).decode("ascii")

    @classmethod
    def decode(cls, text):
        """Reverses encode(). Plain JSON (an old, unencoded file) is returned unchanged."""
        text = text.strip()
        if text.startswith("["):
            return text
        scrambled = base64.b64decode(text, validate=True)
        data = bytes(a ^ b for a, b in zip(scrambled, cls._keystream(len(scrambled))))
        return data.decode("utf-8")

    def get_students(self):
        """Returns a copy of the list (changing the list does not affect the database)."""
        return list(self.students)

    def find_student(self, student_id):
        """Returns the student with this id, or None."""
        for s in self.students:
            if s.student_id == student_id:
                return s
        return None

    def find_student_by_email(self, email):
        """Returns the student with this email (case-insensitive), or None."""
        for s in self.students:
            if s.email.lower() == email.lower():
                return s
        return None

    def add_student(self, student):
        """Adds a new student and saves. Check find_student_by_email() first."""
        self.students.append(student)
        self.save_data()

    def remove_student(self, student_id):
        """Returns False if no student has this id."""
        student = self.find_student(student_id)
        if student is None:
            return False
        self.students.remove(student)
        self.save_data()
        return True

    def clear_students(self):
        """Removes every student from students.data."""
        self.students = []
        self.save_data()

    def generate_student_id(self):
        """Unique random id from 000001 to 999999."""
        return self._generate_unique_id(self.used_student_ids, 999999, 6)

    def generate_subject_id(self):
        """Unique random id from 001 to 999."""
        return self._generate_unique_id(self.used_subject_ids, 999, 3)

    @staticmethod
    def _generate_unique_id(used, maximum, digits):
        """Returns a random zero-padded id from 1 to maximum that is not in used."""
        if len(used) >= maximum:
            raise RuntimeError("No more ids available")
        while True:
            new_id = str(random.randint(1, maximum)).zfill(digits)
            if new_id not in used:
                used.add(new_id)
                return new_id

    def _rebuild_used_ids(self):
        """Rebuilds the sets of taken student and subject ids from the current students."""
        # ids of removed students/subjects become free again after the next save/load
        self.used_student_ids = {s.student_id for s in self.students}
        self.used_subject_ids = {sub.subject_id for s in self.students for sub in s.subjects}
