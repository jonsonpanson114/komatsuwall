
import json
from pathlib import Path

DATA_DIR = Path("c:/Users/jonso/.gemini/office/data")
RAW_DATA_PATH = DATA_DIR / "raw_data.json"
ENRICHED_DATA_PATH = DATA_DIR / "enriched_data.json"

def check_missing():
    with open(RAW_DATA_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
    
    with open(ENRICHED_DATA_PATH, "r", encoding="utf-8") as f:
        enriched = json.load(f)
    
    raw_ids = {item["case_id"] for item in raw}
    enriched_ids = {item["case_id"] for item in enriched}
    
    missing = raw_ids - enriched_ids
    
    print(f"Total Raw: {len(raw)}")
    print(f"Total Enriched: {len(enriched)}")
    print(f"Missing Count: {len(missing)}")
    print("Missing IDs:", list(missing))

if __name__ == "__main__":
    check_missing()
