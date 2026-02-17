
import json
from pathlib import Path

DATA_DIR = Path("c:/Users/jonso/.gemini/office/data")
ENRICHED_DATA_PATH = DATA_DIR / "enriched_data.json"




def inspect_missing():
    with open(ENRICHED_DATA_PATH, "r", encoding="utf-8") as f:
        cases = json.load(f)
    for case_id in ["1702", "1703"]:
        for case in cases:
            if case["case_id"] == case_id:
                descs = case.get("descriptions", [])
                valid_count = sum(1 for d in descs if d.get("description"))
                print(f"ID: {case_id}, Total Descs: {len(descs)}, Valid Descs: {valid_count}")
                if len(descs) > 0:
                    print(f"First Desc Snippet: '{descs[0].get('description')[:20]}'")

if __name__ == "__main__":
    inspect_missing()



