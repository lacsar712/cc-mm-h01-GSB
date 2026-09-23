import pytest

from app.rules import classify


@pytest.mark.parametrize(
    "ch4_pct, expected_level, expected_note",
    [
        (1.0, "报警", "甲烷达到报警线"),
        (1.4, "报警", "甲烷达到报警线"),
        (0.35, "正常", "甲烷低于报警线"),
    ],
)
def test_classify_at_and_around_alarm_line(ch4_pct, expected_level, expected_note):
    level, note = classify(ch4_pct)
    assert level == expected_level
    assert note == expected_note
