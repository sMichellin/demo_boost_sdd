# auth-lockout Specification

## Purpose
Protect accounts from password guessing by locking them after repeated failed logins.

## Requirements

### Requirement: Account lockout
The system SHALL lock the account after 5 failed logins.

#### Scenario: AUTH-LOCK-01 lockout on sixth attempt
- **GIVEN** 5 failed logins
- **WHEN** a 6th attempt is made
- **THEN** the account is locked

#### Scenario: AUTH-LOCK-02 successful login resets counter
- **GIVEN** 4 failed logins
- **WHEN** a successful login is made
- **THEN** the failed-login counter is reset to 0
