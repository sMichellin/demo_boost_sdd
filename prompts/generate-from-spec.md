# Промпт: тесты из спецификации

> Сценарий демо B, слайд 9. Оракул берётся из сценариев спеки, а не из кода.
> В промпт идут **только сценарии и сигнатуры**, исходный код реализации не передаётся.

## Вход

1. Сценарии из `openspec/specs/text-equality/spec.md` и `openspec/specs/auth-lockout/spec.md`.
2. Сигнатуры:
   - `demo.text.TextUtils.equals(String, String): boolean`
   - `demo.auth.LoginService(Map<String, String> passwords)`
   - `demo.auth.LoginService.login(String user, String password): LoginResult` (`SUCCESS` / `FAILURE` / `LOCKED`)
   - `demo.auth.LoginService.isLocked(String user): boolean`
   - `demo.auth.LoginService.failedAttempts(String user): int`

## Промпт

```text
Вот сценарии из openspec/specs/text-equality/spec.md и
openspec/specs/auth-lockout/spec.md:

<вставить сценарии>

Вот сигнатуры:
<вставить сигнатуры из раздела «Вход»>

Для каждого сценария напиши один JUnit 5 тест в src/test/java/demo/fromspec/,
пометь его @Tag("<ID сценария>"), в @DisplayName продублируй заголовок
сценария. GIVEN превращай в подготовку данных, WHEN в вызов, ожидаемые
значения бери только из THEN. Код реализации не читай.
Если сценарий можно понять больше чем одним способом, не пиши тест,
а задай вопрос (правило из AGENTS.md).
```

## Запуск

```bash
mvn -B test   # на коде с дефектами: красный, падают TXT-EQ-01 и AUTH-LOCK-01
```
