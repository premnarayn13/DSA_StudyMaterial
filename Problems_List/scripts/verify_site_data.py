import json
import pathlib
import sys

def main():
    root = pathlib.Path(__file__).resolve().parent.parent
    data_path = root / "site" / "data.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    problems = data["problems"]
    
    assert len(problems) == data["meta"]["problemCount"], f"Problem count mismatch: {len(problems)} != {data['meta']['problemCount']}"
    assert [p["order"] for p in problems] == list(range(1, len(problems) + 1)), "Order sequence invalid"
    assert all(p["url"].startswith("http") for p in problems), "Invalid URLs found"
    assert len({p["id"] for p in problems}) == len(problems), "Duplicate problem IDs found"
    assert [s["n"] for s in data["meta"]["steps"]] == list(range(1, data["meta"]["stepCount"] + 1)), "Step numbers sequence invalid"
    
    step_title_map = {s["n"]: s["title"] for s in data["meta"]["steps"]}
    for p in problems:
        expected_title = step_title_map[p["step"]]
        assert p["stepTitle"] == expected_title, f"Mismatch for {p['id']}: {p['stepTitle']} != {expected_title}"
        assert p["difficulty"] in ("", "Easy", "Medium", "Hard"), f"Invalid difficulty: {p['difficulty']}"
        assert p["platform"] in ("leetcode", "gfg", "takeuforward"), f"Invalid platform: {p['platform']}"
        
    print(f"{len(problems)} problems, {len(data['meta']['steps'])} modules verified successfully.")

if __name__ == "__main__":
    main()

