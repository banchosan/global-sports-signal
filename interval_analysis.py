import json


def load_snapshot(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_diff(old, new):
    return {
        "minutes": new["minute"] - old["minute"],

        "home_shots": new["home_shots"] - old["home_shots"],
        "away_shots": new["away_shots"] - old["away_shots"],

        "home_sog": (
            new["home_shots_on_goal"]
            - old["home_shots_on_goal"]
        ),
        "away_sog": (
            new["away_shots_on_goal"]
            - old["away_shots_on_goal"]
        ),

        "home_corners": new["home_corners"] - old["home_corners"],
        "away_corners": new["away_corners"] - old["away_corners"],

        "home_xg": new["home_xg"] - old["home_xg"],
        "away_xg": new["away_xg"] - old["away_xg"],
    }


# ==========================================
# 差分スタッツを見やすく表示する関数
# ==========================================
def print_interval(title, diff):
    print()
    print(f"=== {title} ===")
    print("Shots:", diff["home_shots"], "-", diff["away_shots"])
    print("Shots on Goal:", diff["home_sog"], "-", diff["away_sog"])
    print("Corners:", diff["home_corners"], "-", diff["away_corners"])
    print(
        "xG:",
        round(diff["home_xg"], 2),
        "-",
        round(diff["away_xg"], 2)
    )


# ==========================================
# ここからJSONを読み込む
# ==========================================
snapshot_60 = load_snapshot("data/snapshots/team_a_60.json")
snapshot_70 = load_snapshot("data/snapshots/team_a_70.json")
snapshot_80 = load_snapshot("data/snapshots/team_a_80.json")


diff_60_70 = calculate_diff(snapshot_60, snapshot_70)
diff_70_80 = calculate_diff(snapshot_70, snapshot_80)
diff_60_80 = calculate_diff(snapshot_60, snapshot_80)

# ==========================================
# 計算したスタッツを表示
# ==========================================
print_interval("60 → 70", diff_60_70)
print_interval("70 → 80", diff_70_80)
print_interval("60 → 80", diff_60_80)




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


home_corner_score, away_corner_score = detect_corner_signal(diff_60_70)

print()
print("=== CORNER SIGNAL ===")
print("Home Corner Score:", home_corner_score)
print("Away Corner Score:", away_corner_score)

if home_corner_score >= 2:
    print("🚩 HOME CORNER SIGNAL")

if away_corner_score >= 2:
    print("🚩 AWAY CORNER SIGNAL")

def detect_goal_signal(diff_60_70, diff_70_80):
    home_score = 0
    away_score = 0

    # 60→70でホームが強く押している
    if (
        diff_60_70["home_shots"] >= 4
        and diff_60_70["home_sog"] >= 2
        and diff_60_70["home_xg"] >= 0.4
    ):
        home_score += 1

    # 70→80でもホームの圧力が継続
    if (
        diff_70_80["home_shots"] >= 4
        and diff_70_80["home_sog"] >= 2
        and diff_70_80["home_xg"] >= 0.4
    ):
        home_score += 1

    # 相手がほとんど攻撃できていない
    if (
        diff_60_70["away_shots"] <= 1
        and diff_70_80["away_shots"] <= 1
    ):
        home_score += 1

    # Away側も同じ考え方
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


home_goal_score, away_goal_score = detect_goal_signal(
    diff_60_70,
    diff_70_80
)

print()
print("=== GOAL SIGNAL ===")
print("Home Goal Score:", home_goal_score)
print("Away Goal Score:", away_goal_score)

if home_goal_score >= 2:
    print("🔥 HOME GOAL SIGNAL")

if away_goal_score >= 2:
    print("🔥 AWAY GOAL SIGNAL")

def detect_comeback_signal(snapshot_60, snapshot_80, diff_60_70, diff_70_80):
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

    # 80分時点でAwayが負けている
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


home_comeback_score, away_comeback_score = detect_comeback_signal(
    snapshot_60,
    snapshot_80,
    diff_60_70,
    diff_70_80
)

print()
print("=== COMEBACK SIGNAL ===")
print("Home Comeback Score:", home_comeback_score)
print("Away Comeback Score:", away_comeback_score)

if home_comeback_score >= 2:
    print("⚡ HOME COMEBACK SIGNAL")

if away_comeback_score >= 2:
    print("⚡ AWAY COMEBACK SIGNAL")