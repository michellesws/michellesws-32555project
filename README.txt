CLIUniApp and GUIUniApp - 32555 Assessment 1 Part 2
====================================================

Language and requirements
-------------------------
- Python 3.8 or newer (tested with Python 3.14 on Windows 11).
- No additional libraries. Only the Python standard library is used
  (json, os, random, re, sys, tkinter).
- tkinter is included in the standard Python installers for Windows and macOS.
  On Linux it may need to be installed separately, e.g. `sudo apt install python3-tk`.

Folder structure
----------------
src/
  App.py                        CLIUniApp entry point (University System menu)
  GUIUniApp.py                  GUIUniApp entry point (login, enrolment, subject and exception windows)
  student_account_control.py    Student System menu: login / register
  student_enrolment_control.py  Subject Enrolment System menu: change password / enrol / remove / show
  admin_control.py              Admin System menu: clear / group / partition / remove / show
  enrolment_system.py           Database class: creates, reads, writes and clears students.data
  student.py                    Student model class
  subject.py                    Subject model class
  validator.py                  Email and password regex validation
  message_handler.py            Coloured, indented console output

How to run
----------
Open a terminal in this folder (the folder containing README.txt and src/) and run:

  CLI:  python src/App.py
  GUI:  python src/GUIUniApp.py

(On Windows, `py` can be used instead of `python`.)

students.data is created automatically in the folder the program is run from.
Run both applications from this same folder so that they share the same students.data.

GUIUniApp is for registered students only, so register a student in CLIUniApp first
(University System -> S -> r), then log in with the same email and password in GUIUniApp.

Email and password formats
--------------------------
- Email:    firstname.lastname@university.com          e.g. john.smith@university.com
- Password: starts with an upper-case letter, has at least 5 letters,
            followed by 3 or more digits                e.g. Helloworld123
