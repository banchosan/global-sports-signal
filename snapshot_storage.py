import json
from pathlib import Path


# ==========================================
# snapshotをJSONファイルとして保存する
# ==========================================
def save_live_snapshot(snapshot):

    folder = Path("data/live_snapshots")
    folder.mkdir(parents=True, exist_ok=True)

    fixture_id = snapshot["fixture_id"]
    minute = snapshot["minute"]

    filename = folder / f"{fixture_id}_{minute}.json"

    # 同じ試合・同じminuteは二重保存しない
    if filename.exists():
        print("⏭️ SNAPSHOT ALREADY EXISTS:", filename)
        return

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(
            snapshot,
            f,
            ensure_ascii=False,
            indent=2
        )

    print("💾 SNAPSHOT SAVED:", filename)