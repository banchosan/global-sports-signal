# ==========================================
# APIのstatisticsから
# 指定したスタッツを探す
# ==========================================
def get_stat(statistics, stat_name):

    for stat in statistics:
        if stat["type"] == stat_name:

            # データがNoneなら0として扱う
            if stat["value"] is None:
                return 0

            return stat["value"]

    # そもそも項目が存在しない場合
    return 0


# ==========================================
# APIレスポンスを
# 自分たちのsnapshot形式に変換する
# ==========================================
def build_snapshot(
    fixture_id,
    minute,
    home_team,
    away_team,
    home_score,
    away_score,
    statistics_response,
):

    # APIレスポンスの
    # HOME / AWAY のstatisticsを取り出す
    home_stats = statistics_response["response"][0]["statistics"]
    away_stats = statistics_response["response"][1]["statistics"]

    # 必要なスタッツを探す
    home_shots = get_stat(home_stats, "Total Shots")
    away_shots = get_stat(away_stats, "Total Shots")

    home_sog = get_stat(home_stats, "Shots on Goal")
    away_sog = get_stat(away_stats, "Shots on Goal")

    home_corners = get_stat(home_stats, "Corner Kicks")
    away_corners = get_stat(away_stats, "Corner Kicks")

    home_xg = get_stat(home_stats, "expected_goals")
    away_xg = get_stat(away_stats, "expected_goals")

    # ======================================
    # 自分たちの統一形式にする
    # ======================================
    snapshot = {
        "fixture_id": fixture_id,
        "minute": minute,

        "home_team": home_team,
        "away_team": away_team,

        "home_score": home_score,
        "away_score": away_score,

        "home_shots": int(home_shots),
        "away_shots": int(away_shots),

        "home_shots_on_goal": int(home_sog),
        "away_shots_on_goal": int(away_sog),

        "home_corners": int(home_corners),
        "away_corners": int(away_corners),

        "home_xg": float(home_xg),
        "away_xg": float(away_xg),
    }

    return snapshot