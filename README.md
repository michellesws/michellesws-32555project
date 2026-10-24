# Welcome to the 32555 Group Assignment Repository 

Welcome! This repository is dedicated to our **32555** course group project.
 
## our group work (document uml design)
the group work share file can access this link https://drive.google.com/drive/folders/1oL0tV5FJ5mAc5mSi4k0PfpnXGrGW-J6o?usp=sharing

## Resource
https://github.com/FarshidKeivanian


## CLIUniApp code (Python)

Python 3.8+. No extra libraries. Students are saved as JSON in `students.data`.

### Done (model + utilities)

| File | What it does |
|---|---|
| `subject.py` | `Subject`: random 25–100 mark, grade (HD/D/C/P/Z) from mark |
| `student.py` | `Student`: id, name, email, password, subjects (max 4), average mark, pass/fail |
| `enrolment_system.py` | `EnrolmentSystem`, the database: reads/writes `students.data` (JSON), finds/adds/removes students, generates unique ids |
| `validator.py` | `Validator`: email and password regex |
| `message_handler.py` | `MessageHandler`: coloured and indented console output |

Main methods for controllers:

```python
from enrolment_system import EnrolmentSystem
from student import Student
from subject import Subject
from validator import Validator

db = EnrolmentSystem()                            # creates/loads students.data

# register
Validator.is_valid_email(email); Validator.is_valid_password(pw)
db.find_student_by_email(email)                   # None = not registered yet
db.add_student(Student(db.generate_student_id(), name, email, pw))   # saves

# enrol / remove / change password (then save!)
student.can_enrol()
student.enrol(Subject(db.generate_subject_id()))
student.remove_subject(subject_id)
student.password = new_pw
db.save_data()

# admin
db.get_students();  db.remove_student(student_id);  db.clear_students()
student.overall_grade();  student.is_pass();  student.average_mark()
```

### Menus and GUI

- [x] `App.py` – main university menu (A/S/X)
- [x] `student_account_control.py` – `StudentAccountControl`, student menu: login / register (l/r/x)
- [x] `student_enrolment_control.py` – `StudentEnrolmentControl`, enrolment menu (c/e/r/s/x)
- [x] `admin_control.py` – `AdminControl`, admin menu (c/g/p/r/s/x)
- [x] `GUIUniApp.py` – login, enrolment, subject and exception windows (tkinter)

### Running

Run both apps from the project root so they share the same `students.data`:

```
python src/App.py         # CLIUniApp
python src/GUIUniApp.py   # GUIUniApp (register students in CLIUniApp first)
```
