
import chromadb
from pathlib import Path
import json

DATA_DIR = Path("c:/Users/jonso/.gemini/office/data")
CHROMA_DIR = DATA_DIR / "chroma_db_v2"
ENRICHED_DATA_PATH = DATA_DIR / "enriched_data.json"
COLLECTION_NAME = "komatsu_cases"


def verify_count():
    output = []
    # 1. Check Enriched Data
    with open(ENRICHED_DATA_PATH, "r", encoding="utf-8") as f:
        cases = json.load(f)
    output.append(f"Enriched Data Count: {len(cases)}")
    enriched_ids = set(c["case_id"] for c in cases)

    # 2. Check ChromaDB Index
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    try:
        collection = client.get_collection(COLLECTION_NAME)
        count = collection.count()
        output.append(f"ChromaDB Index Count: {count}")
        
        # Get all stored metadata to check case_ids
        result = collection.get(include=["metadatas"])
        stored_case_ids = set()
        if result["metadatas"]:
            for meta in result["metadatas"]:
                stored_case_ids.add(meta["case_id"])
            
        output.append(f"Unique Case IDs in Index: {len(stored_case_ids)}")
        
        missing = enriched_ids - stored_case_ids
        if missing:
            output.append(f"Missing Case IDs in Index: {list(missing)}")
        else:
            output.append("All enriched cases are present in the index.")
            
    except Exception as e:
        output.append(f"Error accessing collection: {e}")

    with open("verification_log.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output))

if __name__ == "__main__":
    verify_count()

