package demo.text;

public final class TextUtils {

    private TextUtils() {
    }

    public static boolean equals(String a, String b) {
        if (a == b) return true;
        if (a == null || b == null) return false;
        return a.equalsIgnoreCase(b); // BUG: спека требует учитывать регистр
    }
}
