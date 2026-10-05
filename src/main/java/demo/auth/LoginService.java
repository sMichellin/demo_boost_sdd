package demo.auth;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

/** In-memory login with a failed-attempt counter and account lockout. */
public class LoginService {

    static final int MAX_FAILED_ATTEMPTS = 5;

    private final Map<String, String> passwords;
    private final Map<String, Integer> failedAttempts = new HashMap<>();
    private final Set<String> lockedUsers = new HashSet<>();

    public LoginService(Map<String, String> passwords) {
        this.passwords = Map.copyOf(passwords);
    }

    public LoginResult login(String user, String password) {
        if (lockedUsers.contains(user)) {
            return LoginResult.LOCKED;
        }
        if (password != null && password.equals(passwords.get(user))) {
            failedAttempts.remove(user);
            return LoginResult.SUCCESS;
        }
        int attempts = failedAttempts.merge(user, 1, Integer::sum);
        if (attempts >= MAX_FAILED_ATTEMPTS) {
            lockedUsers.add(user);
        }
        return LoginResult.FAILURE;
    }

    public boolean isLocked(String user) {
        return lockedUsers.contains(user);
    }

    public int failedAttempts(String user) {
        return failedAttempts.getOrDefault(user, 0);
    }
}
