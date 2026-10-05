## MODIFIED Requirements

### Requirement: Account lockout
The system SHALL lock the account after 5 failed logins
and SHALL unlock it after 15 minutes.

#### Scenario: AUTH-LOCK-01 lockout on sixth attempt
- **GIVEN** 5 failed logins
- **WHEN** a 6th attempt is made
- **THEN** the account is locked

#### Scenario: AUTH-LOCK-02 successful login resets counter
- **GIVEN** 4 failed logins
- **WHEN** a successful login is made
- **THEN** the failed-login counter is reset to 0

#### Scenario: AUTH-LOCK-03 unlock after timeout
- **GIVEN** a locked account
- **WHEN** 15 minutes have passed
- **THEN** the user can log in again
