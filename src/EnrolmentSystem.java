import java.io.EOFException;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Random;
import java.util.Set;

/**
 * The "Database" class: owns the list of students and keeps it in sync with students.data.
 * Every method that changes data saves to the file straight away.
 *
 * If you modify a Student you got from findStudent()/findStudentByEmail()
 * (enrol, removeSubject, setPassword), call saveData() afterwards.
 */
public class EnrolmentSystem {
    public static final String FILE_NAME = "students.data";

    private static final Random RANDOM = new Random();

    private final File file;
    private List<Student> students = new ArrayList<>();
    private final Set<String> usedStudentIds = new HashSet<>();
    private final Set<String> usedSubjectIds = new HashSet<>();

    public EnrolmentSystem() {
        this(FILE_NAME);
    }

    public EnrolmentSystem(String fileName) {
        this.file = new File(fileName);
        loadData();
    }

    /** Creates students.data if it does not exist, then reads all students from it. */
    @SuppressWarnings("unchecked")
    public void loadData() {
        try {
            if (file.createNewFile()) {
                students = new ArrayList<>();
                saveData();
                return;
            }
            try (ObjectInputStream in = new ObjectInputStream(new FileInputStream(file))) {
                students = (List<Student>) in.readObject();
            }
        } catch (EOFException e) {
            // empty file - treat as no students
            students = new ArrayList<>();
        } catch (IOException | ClassNotFoundException | ClassCastException e) {
            System.err.println("Could not read " + file.getName() + ": " + e.getMessage());
            students = new ArrayList<>();
        }
        rebuildUsedIds();
    }

    /** Writes all students to students.data. */
    public void saveData() {
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(file))) {
            out.writeObject(students);
        } catch (IOException e) {
            System.err.println("Could not write " + file.getName() + ": " + e.getMessage());
        }
        rebuildUsedIds();
    }

    /** Returns a copy of all students (changing the list does not affect the database). */
    public List<Student> getStudents() {
        return new ArrayList<>(students);
    }

    public Student findStudent(String id) {
        for (Student s : students) {
            if (s.getStudentId().equals(id)) {
                return s;
            }
        }
        return null;
    }

    public Student findStudentByEmail(String email) {
        for (Student s : students) {
            if (s.getEmail().equalsIgnoreCase(email)) {
                return s;
            }
        }
        return null;
    }

    /** Adds a new student and saves. Callers should check findStudentByEmail() first. */
    public void addStudent(Student student) {
        students.add(student);
        saveData();
    }

    /** @return false if no student has this id */
    public boolean removeStudent(String id) {
        boolean removed = students.removeIf(s -> s.getStudentId().equals(id));
        if (removed) {
            saveData();
        }
        return removed;
    }

    /** Removes every student from students.data. */
    public void clearStudents() {
        students.clear();
        saveData();
    }

    /** Unique random id from 000001 to 999999. */
    public String generateStudentId() {
        return generateUniqueId(usedStudentIds, 999999, "%06d");
    }

    /** Unique random id from 001 to 999. */
    public String generateSubjectId() {
        return generateUniqueId(usedSubjectIds, 999, "%03d");
    }

    private String generateUniqueId(Set<String> used, int max, String format) {
        if (used.size() >= max) {
            throw new IllegalStateException("No more ids available");
        }
        String id;
        do {
            id = String.format(format, RANDOM.nextInt(max) + 1);
        } while (used.contains(id));
        used.add(id);
        return id;
    }

    /** Ids of removed students/subjects become free again after the next save/load. */
    private void rebuildUsedIds() {
        usedStudentIds.clear();
        usedSubjectIds.clear();
        for (Student s : students) {
            usedStudentIds.add(s.getStudentId());
            for (Subject sub : s.getEnrolments()) {
                usedSubjectIds.add(sub.getSubjectID());
            }
        }
    }
}
