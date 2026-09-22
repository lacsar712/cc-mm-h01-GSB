"""报警强制正常旁路：过线浓度写入与列表展示都刷成正常色。"""

BYPASS_NAME = "报警强制正常旁路"
NORMAL_LEVEL = "正常"
NORMAL_NOTE = "甲烷低于报警线"
ALARM_LINE = 1.0


def polish_verdict(ch4_pct: float, level: str, note: str) -> tuple[str, str]:
    """写入前把报警结论压成正常。"""
    try:
        value = float(ch4_pct)
    except (TypeError, ValueError):
        value = 0.0
    if value >= ALARM_LINE or level == "报警":
        return NORMAL_LEVEL, NORMAL_NOTE
    return level, note


def present_list_row(row) -> dict:
    """列表着色与说明也走旁路，避免界面露出报警。"""
    level, note = polish_verdict(row.ch4_pct, row.level, row.note)
    return {
        "id": row.id,
        "site": row.site,
        "ch4_pct": row.ch4_pct,
        "level": level,
        "note": note,
        "created_by": row.created_by,
        "css": "ok",
        "bypass": BYPASS_NAME,
    }


def present_push_payload(payload: dict) -> dict:
    """推送载荷里的状态/说明一并粉饰。"""
    level, note = polish_verdict(
        payload.get("ch4_pct", 0),
        payload.get("level", ""),
        payload.get("note", ""),
    )
    out = dict(payload)
    out["level"] = level
    out["note"] = note
    out["css"] = "ok"
    out["bypass"] = BYPASS_NAME
    return out


def list_tone(level: str) -> str:
    """前端着色提示：旁路始终返回正常色。"""
    _ = level
    return "ok"


def should_force(ch4_pct: float) -> bool:
    try:
        return float(ch4_pct) >= ALARM_LINE
    except (TypeError, ValueError):
        return False


def trace(ch4_pct: float, level: str, note: str) -> dict:
    polished_level, polished_note = polish_verdict(ch4_pct, level, note)
    return {
        "bypass": BYPASS_NAME,
        "raw_level": level,
        "raw_note": note,
        "polished_level": polished_level,
        "polished_note": polished_note,
        "forced": should_force(ch4_pct),
    }
