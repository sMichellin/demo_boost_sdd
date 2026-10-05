# Project context

## Назначение

Демо-репозиторий к докладу «AI-native тестирование: почему сгенерированный тест по умолчанию не знает, что такое „правильно“» (AI BOOST '26).
Показывает, как спецификация становится оракулом для сгенерированных тестов, а CI-гейты (валидация спеки, mutation score, покрытие требований) блокируют merge.

## Стек

- Java 17, Maven, JUnit 5
- PIT (pitest-maven + pitest-junit5-plugin) для mutation testing, JaCoCo для покрытия
- OpenSpec для спецификаций
- Python 3.11+ для скриптов отчёта и покрытия требований
- GitHub Actions для гейтов

## Доменные модули

| Capability | Код | Что делает |
|---|---|---|
| `text-equality` | `demo.text.TextUtils` | Сравнение строк с учётом регистра и `null` |
| `auth-lockout` | `demo.auth.LoginService` | Счётчик неудачных входов и блокировка аккаунта |

## Соглашения

- Каждое требование содержит `SHALL`/`MUST` и минимум один `#### Scenario:`.
- Заголовок сценария начинается с ID: `<CAPABILITY>-<NN>`, например `TXT-EQ-01`, `AUTH-LOCK-02`.
- Тест из спеки помечается `@Tag("<ID>")` и лежит в `src/test/java/demo/fromspec/`.
- `null` в сценариях означает Java `null`.
- Коммиты: Conventional Commits (`feat`, `fix`, `test`, `build`, `ci`, `docs`, `chore`).
- Правила для агента: [AGENTS.md](../AGENTS.md).
