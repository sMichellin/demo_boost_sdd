# Proposal: add-lockout-reset

## Why
A locked account stays locked forever, so every lockout turns into a support ticket.
Users should regain access on their own after a fixed cool-down period.

## What Changes
- Account lockout is lifted automatically 15 minutes after it was applied.
- New scenario AUTH-LOCK-03 defines the unlock behaviour.

## Impact
- Affected specs: `auth-lockout`
- Affected code: `demo.auth.LoginService` (needs a clock to measure the lockout period)
