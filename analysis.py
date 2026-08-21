# ==========================================
# 2つのスナップショットを比較して
# その時間帯に増えたスタッツを計算する
# ==========================================
def calculate_diff(old, new):
    return {
        # 何分間の差分なのか
        "minutes": new["minute"] - old["minute"],

        # シュート数の増加
        "home_shots": new["home_shots"] - old["home_shots"],
        "away_shots": new["away_shots"] - old["away_shots"],

        # 枠内シュート数の増加
        "home_sog": (
            new["home_shots_on_goal"]
            - old["home_shots_on_goal"]
        ),
        "away_sog": (
            new["away_shots_on_goal"]
            - old["away_shots_on_goal"]
        ),

        # コーナー数の増加
        "home_corners": new["home_corners"] - old["home_corners"],
        "away_corners": new["away_corners"] - old["away_corners"],

        # xGの増加
        "home_xg": new["home_xg"] - old["home_xg"],
        "away_xg": new["away_xg"] - old["away_xg"],
    }