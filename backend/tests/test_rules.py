from app.rules import classify


def test_exactly_one_percent_is_alarm():
    """刚好 1%：踩线即报警。"""
    assert classify(1.0) == ("报警", "甲烷达到报警线")


def test_well_above_one_percent_is_alarm():
    """明显高于 1%：报警。"""
    assert classify(1.4) == ("报警", "甲烷达到报警线")


def test_well_below_one_percent_is_normal():
    """明显低于 1%：正常。"""
    assert classify(0.35) == ("正常", "甲烷低于报警线")
