import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * A registered student and their subject enrolments.
 * Stored (serialised) in students.data by EnrolmentSystem.
 */
public class Student implements Serializable {
    private static final long serialVersionUID = 1L;

    public static final int MAX_SUBJECTS = 4;
    public static final double PASS_MARK = 50;

    private final String studentID;
    private final String name;
    private final String email;
    private String password;
    private final List<Subject> enrolments = new ArrayList<>();

    /** @param studentID unique 6-digit id, e.g. from EnrolmentSystem.generateStudentId() */
    public Student(String studentID, String name, String email, String password) {
        this.studentID = studentID;
        this.name = name;
        this.email = email;
        this.password = password;
    }

    public String getStudentId() {
        return studentID;
    }

    public String getName() {
        return name;
    }

    public String getEmail() {
        return email;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    /** Read-only view; use enrol()/removeSubject() to change enrolments. */
    public List<Subject> getEnrolments() {
        return Collections.unmodifiableList(enrolments);
    }

    public boolean canEnrol() {
        return enrolments.size() < MAX_SUBJECTS;
    }

    /**
     * Adds a subject to the enrolment list.
     * @return false if the student is already enrolled in MAX_SUBJECTS subjects
     */
    public boolean enrol(Subject subject) {
        if (!canEnrol()) {
            return false;
        }
        enrolments.add(subject);
        return true;
    }

    /** @return false if the student is not enrolled in a subject with this id */
    public boolean removeSubject(String subjectID) {
        return enrolments.removeIf(s -> s.getSubjectID().equals(subjectID));
    }

    /** Average mark of all enrolled subjects (0 if none). */
    public double getAverageMark() {
        return enrolments.stream().mapToDouble(Subject::getMark).average().orElse(0);
    }

    public String getOverallGrade() {
        return Subject.gradeFor(getAverageMark());
    }

    public boolean isPass() {
        return getAverageMark() >= PASS_MARK;
    }

    @Override
    public String toString() {
        return String.format("%s :: %s --> GRADE: %2s - MARK: %.2f",
                name, studentID, getOverallGrade(), getAverageMark());
    }
}
