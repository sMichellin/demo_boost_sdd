package demo.fromcode;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import demo.text.TextUtils;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/**
 * Антипример (сценарий A): сгенерировано по реализации TextUtils через prompts/generate-from-code.md.
 * Запускается только в профиле demo-from-code.
 */
@Tag("from-code")
class TextUtilsFromCodeTest {

    @Test
    void sameReferenceIsEqual() {
        String s = "abc";
        assertTrue(TextUtils.equals(s, s));
    }

    @Test
    void bothNullAreEqual() {
        assertTrue(TextUtils.equals(null, null));
    }

    @Test
    void firstNullIsNotEqual() {
        assertFalse(TextUtils.equals(null, "abc"));
    }

    @Test
    void secondNullIsNotEqual() {
        assertFalse(TextUtils.equals("abc", null));
    }

    @Test
    void differentCaseIsEqual() {
        assertTrue(TextUtils.equals("ABC", "abc"));
    }

    @Test
    void differentTextIsNotEqual() {
        assertFalse(TextUtils.equals("abc", "abd"));
    }
}
