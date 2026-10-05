package demo.fromspec;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;

import demo.auth.LoginService;
import demo.text.TextUtils;
import java.util.Map;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/**
 * Тесты-пустышки (сценарий E): вызывают весь код и носят теги сценариев,
 * но проверяют только отсутствие исключений. Line coverage высокий, mutation score низкий.
 */
class WeakCoverageTest {

    @Test
    @Tag("TXT-EQ-01")
    @Tag("TXT-EQ-02")
    @Tag("TXT-EQ-03")
    @Tag("TXT-EQ-04")
    void textUtilsDoesNotThrow() {
        assertDoesNotThrow(() -> {
            TextUtils.equals("ABC", "abc");
            TextUtils.equals(null, null);
            TextUtils.equals(null, "abc");
            TextUtils.equals(new String("abc"), new String("abc"));
        });
    }

    @Test
    @Tag("AUTH-LOCK-01")
    @Tag("AUTH-LOCK-02")
    void loginServiceDoesNotThrow() {
        assertDoesNotThrow(() -> {
            LoginService service = new LoginService(Map.of("alice", "correct-horse"));
            service.login("alice", "correct-horse");
            for (int i = 0; i < 6; i++) {
                service.login("alice", "wrong");
            }
            service.isLocked("alice");
            service.failedAttempts("alice");
        });
    }
}
