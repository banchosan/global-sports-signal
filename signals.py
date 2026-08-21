# --------------------------------------------------
# 60→70分の差分からコーナーシグナルを判定
# --------------------------------------------------
def detect_corner_signal(diff):
    home_score = 0
    away_score = 0

    if (
        diff["home_shots"] >= 4
        and diff["home_corners"] >= 2
    ):
        home_score += 1

    if (
        diff["home_sog"] >= 2
        and diff["home_xg"] >= 0.4
    ):
        home_score += 1

    if (
        diff["away_shots"] <= 1
        and diff["away_corners"] == 0
    ):
        home_score += 1

    if (
        diff["away_shots"] >= 4
        and diff["away_corners"] >= 2
    ):
        away_score += 1

    if (
        diff["away_sog"] >= 2
        and diff["away_xg"] >= 0.4
    ):
        away_score += 1

    if (
        diff["home_shots"] <= 1
        and diff["home_corners"] == 0
    ):
        away_score += 1

    return home_score, away_score


# --------------------------------------------------
# 60→70と70→80の両方を見て
# 継続的なゴール圧力を判定
# --------------------------------------------------
def detect_goal_signal(diff_60_70, diff_70_80):
    home_score = 0
    away_score = 0

    if (
        diff_60_70["home_shots"] >= 4
        and diff_60_70["home_sog"] >= 2
        and diff_60_70["home_xg"] >= 0.4
    ):
        home_score += 1

    if (
        diff_70_80["home_shots"] >= 4
        and diff_70_80["home_sog"] >= 2
        and diff_70_80["home_xg"] >= 0.4
    ):
        home_score += 1

    if (
        diff_60_70["away_shots"] <= 1
        and diff_70_80["away_shots"] <= 1
    ):
        home_score += 1

    if (
        diff_60_70["away_shots"] >= 4
        and diff_60_70["away_sog"] >= 2
        and diff_60_70["away_xg"] >= 0.4
    ):
        away_score += 1

    if (
        diff_70_80["away_shots"] >= 4
        and diff_70_80["away_sog"] >= 2
        and diff_70_80["away_xg"] >= 0.4
    ):
        away_score += 1

    if (
        diff_60_70["home_shots"] <= 1
        and diff_70_80["home_shots"] <= 1
    ):
        away_score += 1

    return home_score, away_score


# --------------------------------------------------
# 80分時点で負けているチームが
# 継続して押しているか判定
# --------------------------------------------------
def detect_comeback_signal(
    snapshot_60,
    snapshot_80,
    diff_60_70,
    diff_70_80
):
    home_score = 0
    away_score = 0

    # 80分時点でホームが負けている
    if snapshot_80["home_score"] < snapshot_80["away_score"]:
        if (
            diff_60_70["home_shots"] >= 4
            and diff_60_70["home_sog"] >= 2
        ):
            home_score += 1

        if (
            diff_70_80["home_shots"] >= 4
            and diff_70_80["home_sog"] >= 2
        ):
            home_score += 1

        if (
            diff_60_70["home_xg"] >= 0.4
            and diff_70_80["home_xg"] >= 0.4
        ):
            home_score += 1

    # 80分時点でアウェイが負けている
    if snapshot_80["away_score"] < snapshot_80["home_score"]:
        if (
            diff_60_70["away_shots"] >= 4
            and diff_60_70["away_sog"] >= 2
        ):
            away_score += 1

        if (
            diff_70_80["away_shots"] >= 4
            and diff_70_80["away_sog"] >= 2
        ):
            away_score += 1

        if (
            diff_60_70["away_xg"] >= 0.4
            and diff_70_80["away_xg"] >= 0.4
        ):
            away_score += 1

    return home_score, away_score