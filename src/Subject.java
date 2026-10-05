import java.io.Serializable;
import java.util.Random;

/**
 * A subject a student is enrolled in.
 * The mark (25-100) is generated randomly on creation and the grade is derived from it.
 */
public class Subject implements Serializable {
    private static final long serialVersionUID = 1L;

    public static final int MIN_MARK = 25;
    public static final int MAX_MARK = 100;

    private static final Random RANDOM = new Random();

    private final String subjectID;
    private final double mark;
    private final String grade;

    /** @param subjectID unique 3-digit id, e.g. from EnrolmentSystem.generateSubjectId() */
    public Subject(String subjectID) {
        this.subjectID = subjectID;
        this.mark = MIN_MARK + RANDOM.nextInt(MAX_MARK - MIN_MARK + 1);
        this.grade = calculateGrade();
    }

    /** UTS grading: HD >= 85, D >= 75, C >= 65, P >= 50, otherwise Z (fail). */
    public String calculateGrade() {
        return gradeFor(mark);
    }

    /** Shared with Student so the overall grade uses the same scale. */
    public static String gradeFor(double mark) {
        if (mark >= 85) return "HD";
        if (mark >= 75) return "D";
        if (mark >= 65) return "C";
        if (mark >= 50) return "P";
        return "Z";
    }

    public String getSubjectID() {
        return subjectID;
    }

    public double getMark() {
        return mark;
    }

    public String getGrade() {
        return grade;
    }

    @Override
    public String toString() {
        return String.format("[ Subject::%s -- mark = %.0f -- grade = %2s ]", subjectID, mark, grade);
    }
}
