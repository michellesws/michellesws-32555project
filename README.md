# Welcome to the 32555 Group Assignment Repository 

Welcome! This repository is dedicated to our **32555** course group project.
 
## our group work (document uml design)
the group work share file can access this link https://drive.google.com/drive/folders/1oL0tV5FJ5mAc5mSi4k0PfpnXGrGW-J6o?usp=sharing

## Resource
https://github.com/FarshidKeivanian


## CLIUniApp code

Java 11+ (uses `String.repeat`). No extra libraries.

### Done (model + utilities)

| Class | What it does |
|---|---|
| `Subject` | Random 25–100 mark, grade (HD/D/C/P/Z) from mark |
| `Student` | id, name, email, password, enrolments (max 4), average mark, pass/fail |
| `EnrolmentSystem` | The database: reads/writes `students.data`, finds/adds/removes students, generates unique ids |
| `Validator` | Email and password regex |
| `MessageHandler` | Coloured and indented console output |

Main methods for controllers:

```java
EnrolmentSystem db = new EnrolmentSystem();       // creates/loads students.data

// register
Validator.isValidEmail(email); Validator.isValidPassword(pw);
db.findStudentByEmail(email);                     // null = not registered yet
db.addStudent(new Student(db.generateStudentId(), name, email, pw));   // saves

// enrol / remove / change password (then save!)
student.canEnrol();
student.enrol(new Subject(db.generateSubjectId()));
student.removeSubject(subjectId);
student.setPassword(newPw);
db.saveData();

// admin
db.getStudents();  db.removeStudent(id);  db.clearStudents();
student.getOverallGrade();  student.isPass();  student.getAverageMark();
```

### To do (rest of the team)

- [ ] `UniApp` – main university menu (A/S/X)
- [ ] `StudentAccountControl` – student menu: login / register (l/r/x)
- [ ] `StudentEnrolmentControl` – enrolment menu (c/e/r/s/x)
- [ ] `AdminControl` – admin menu (c/g/p/r/s/x)
- [ ] GUIUniApp – login, enrolment, subject and exception windows
