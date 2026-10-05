package demo.fromspec;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import demo.text.TextUtils;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** Tests derived from openspec/specs/text-equality/spec.md. */
class TextEqualitySpecTest {

    @Test
    @Tag("TXT-EQ-01")
    @DisplayName("TXT-EQ-01 different case is not equal")
    void differentCaseIsNotEqual() {
        assertFalse(TextUtils.equals("ABC", "abc"));
    }

    @Test
    @Tag("TXT-EQ-02")
    @DisplayName("TXT-EQ-02 both null are equal")
    void bothNullAreEqual() {
        assertTrue(TextUtils.equals(null, null));
    }

    @Test
    @Tag("TXT-EQ-03")
    @DisplayName("TXT-EQ-03 null and non-null are not equal")
    void nullAndNonNullAreNotEqual() {
        assertFalse(TextUtils.equals(null, "abc"));
    }

    @Test
    @Tag("TXT-EQ-04")
    @DisplayName("TXT-EQ-04 same characters in the same case are equal")
    void sameCharactersSameCaseAreEqual() {
        // The scenario asks for two separate instances
        assertTrue(TextUtils.equals(new String("abc"), new String("abc")));
    }
}
