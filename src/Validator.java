import java.util.regex.Pattern;

/** Regex checks for login and registration. */
public class Validator {
    /** firstname.lastname@university.com */
    public static final String EMAIL_REGEX = "^[a-zA-Z]+\\.[a-zA-Z]+@university\\.com$";

    /** Starts with an upper-case letter, at least 5 letters in total, then 3 or more digits. */
    public static final String PASSWORD_REGEX = "^[A-Z][a-zA-Z]{4,}[0-9]{3,}$";

    private static final Pattern EMAIL_PATTERN = Pattern.compile(EMAIL_REGEX);
    private static final Pattern PASSWORD_PATTERN = Pattern.compile(PASSWORD_REGEX);

    public static boolean isValidEmail(String email) {
        return email != null && EMAIL_PATTERN.matcher(email).matches();
    }

    public static boolean isValidPassword(String password) {
        return password != null && PASSWORD_PATTERN.matcher(password).matches();
    }
}
