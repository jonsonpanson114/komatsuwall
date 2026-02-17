
import chromadb
from pathlib import Path
import json
import traceback

DATA_DIR = Path("c:/Users/jonso/.gemini/office/data")
ENRICHED_DATA_PATH = DATA_DIR / "enriched_data.json"
CHROMA_DIR = DATA_DIR / "chroma_db_v2"
COLLECTION_NAME = "komatsu_cases_debug"

def debug_build():
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    try:
        client.delete_collection(COLLECTION_NAME)
    except:
        pass
        
    collection = client.create_collection(name=COLLECTION_NAME)
    
    with open(ENRICHED_DATA_PATH, "r", encoding="utf-8") as f:
        cases = json.load(f)
    
    print(f"Loaded {len(cases)} cases.")
    
    # Try adding the first item
    try:
        case = cases[0]
        desc_entry = case["descriptions"][0]
        description = desc_entry["description"]
        refined_products = desc_entry.get("refined_products", [])
        
        metadata = {
            "case_id": str(case.get("case_id", "")),
            "project_name": str(case.get("project_name", "")),
            "products": "、".join(refined_products), 
            "location": str(case.get("location", "")),
            "image_path": str(desc_entry.get("image_path", "")),
            "url": str(case.get("url", "")),
        }
        
        print("Metadata:", json.dumps(metadata, ensure_ascii=False, indent=2))
        
        # Fake embedding for test
        embedding = [0.1] * 768 
        
        collection.add(
            ids=["test_0"],
            documents=[description],
            embeddings=[embedding],
            metadatas=[metadata],
        )
        print("Successfully added one item.")
        
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    debug_build()
