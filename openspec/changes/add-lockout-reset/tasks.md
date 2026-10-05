# Tasks

## 1. Implementation
- [ ] 1.1 Inject a `java.time.Clock` into `LoginService` and record the lockout time
- [ ] 1.2 Treat an account as unlocked once 15 minutes have passed since lockout

## 2. Tests
- [ ] 2.1 Generate a test for AUTH-LOCK-03 from the scenario (prompts/generate-from-spec.md)
- [ ] 2.2 `mvn -B test` and the PIT gate are green
