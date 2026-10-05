package demo.fromspec;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import demo.auth.LoginResult;
import demo.auth.LoginService;
import java.util.Map;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;

/** Tests derived from openspec/specs/auth-lockout/spec.md. */
class AuthLockoutSpecTest {

    private static final String USER = "alice";
    private static final String PASSWORD = "correct-horse";
    private static final String WRONG_PASSWORD = "wrong";

    private final LoginService service = new LoginService(Map.of(USER, PASSWORD));

    @Test
    @Tag("AUTH-LOCK-01")
    @DisplayName("AUTH-LOCK-01 lockout on sixth attempt")
    void lockoutOnSixthAttempt() {
        // GIVEN 5 failed logins
        failLogins(5);

        // WHEN a 6th attempt is made (even with the right password)
        LoginResult result = service.login(USER, PASSWORD);

        // THEN the account is locked
        assertEquals(LoginResult.LOCKED, result);
        assertTrue(service.isLocked(USER));
    }

    @Test
    @Tag("AUTH-LOCK-02")
    @DisplayName("AUTH-LOCK-02 successful login resets counter")
    void successfulLoginResetsCounter() {
        // GIVEN 4 failed logins
        failLogins(4);
        assertEquals(4, service.failedAttempts(USER));

        // WHEN a successful login is made
        assertEquals(LoginResult.SUCCESS, service.login(USER, PASSWORD));

        // THEN the failed-login counter is reset to 0
        assertEquals(0, service.failedAttempts(USER));
    }

    private void failLogins(int count) {
        for (int i = 0; i < count; i++) {
            assertEquals(LoginResult.FAILURE, service.login(USER, WRONG_PASSWORD));
        }
    }
}
