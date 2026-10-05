# text-equality Specification

## Purpose
Compare two strings for equality in a null-safe, case-sensitive way.

## Requirements

### Requirement: Case-sensitive equality
The system SHALL treat two strings as equal only if they contain
the same characters in the same case.

#### Scenario: TXT-EQ-01 different case is not equal
- **WHEN** comparing "ABC" and "abc"
- **THEN** the result is false

#### Scenario: TXT-EQ-02 both null are equal
- **WHEN** comparing null and null
- **THEN** the result is true

#### Scenario: TXT-EQ-03 null and non-null are not equal
- **WHEN** comparing null and "abc"
- **THEN** the result is false

#### Scenario: TXT-EQ-04 same characters in the same case are equal
- **WHEN** comparing two separate string instances "abc" and "abc"
- **THEN** the result is true
