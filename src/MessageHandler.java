/**
 * Console output in one place so every menu uses the same colours and indentation.
 * Indent: 0 = university menu, 1 = student/admin menu, 2 = enrolment menu.
 */
public class MessageHandler {
    public static final String RESET = "\u001B[0m";
    public static final String RED = "\u001B[31m";
    public static final String GREEN = "\u001B[32m";
    public static final String YELLOW = "\u001B[33m";
    public static final String CYAN = "\u001B[36m";

    private static final String INDENT = "        ";

    public static void message(String text) {
        System.out.println(text);
    }

    public static void message(String text, int indent) {
        System.out.println(INDENT.repeat(indent) + text);
    }

    /** Menu prompts, e.g. "Student System (l/r/x): ". Uses print, not println. */
    public static void prompt(String text, int indent) {
        System.out.print(INDENT.repeat(indent) + CYAN + text + RESET);
    }

    public static void info(String text, int indent) {
        message(YELLOW + text + RESET, indent);
    }

    public static void success(String text, int indent) {
        message(GREEN + text + RESET, indent);
    }

    public static void error(String text, int indent) {
        message(RED + text + RESET, indent);
    }
}
