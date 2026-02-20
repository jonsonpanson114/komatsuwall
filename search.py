"""
ChromaDB + Gemini Embedding によるベクトル検索モジュール。
"""

import io
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import chromadb
import google.generativeai as genai

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

load_dotenv()

DATA_DIR = Path(__file__).parent / "data"
ENRICHED_DATA_PATH = DATA_DIR / "enriched_data.json"
CHROMA_DIR = DATA_DIR / "chroma_db_v2"

COLLECTION_NAME = "komatsu_cases"
EMBEDDING_MODEL = "models/gemini-embedding-001"


def ensure_local_index() -> None:
    """Windows/Linuxの互換性対策: ローカルDBが正常でなければエクスポート済みのJSONから即座に再構築する"""
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    
    try:
        if COLLECTION_NAME in [c.name for c in client.list_collections()]:
            col = client.get_collection(COLLECTION_NAME)
            if col.count() > 0:
                # Test read to catch Rust panic on Linux
                col.get(limit=1, include=["metadatas"])
                return
    except Exception:
        pass
        
    print("[Search] 互換性エラーまたはローカルDB未構築を検知。エクスポートデータから復元します...")
    
    try:
        if COLLECTION_NAME in [c.name for c in client.list_collections()]:
            client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    EXPORT_PATH = DATA_DIR / "chroma_export.json"
    if not EXPORT_PATH.exists():
        raise RuntimeError(f"復元ファイル {EXPORT_PATH} が存在しません。")
        
    with open(EXPORT_PATH, "r", encoding="utf-8") as f:
        records = json.load(f)
        
    col = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    
    ids = [str(r["id"]) for r in records]
    documents = [r["document"] for r in records]
    metadatas = [r["metadata"] for r in records]
    embeddings = [r["embedding"] for r in records]
    
    batch_size = 200
    for i in range(0, len(ids), batch_size):
        col.add(
            ids=ids[i:i+batch_size],
            documents=documents[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size],
            embeddings=embeddings[i:i+batch_size]
        )
    print(f"[Search] {len(records)}件のインデックスを復元完了。")


def configure_api():
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY または GEMINI_API_KEY 環境変数を設定してください。"
        )
    genai.configure(api_key=api_key)


def get_embedding(text: str) -> list[float]:
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text,
        task_type="retrieval_document",
    )
    return result["embedding"]


def get_query_embedding(text: str) -> list[float]:
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text,
        task_type="retrieval_query",
    )
    return result["embedding"]


def build_index() -> chromadb.Collection:
    configure_api()

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    existing = [c.name for c in client.list_collections()]
    if COLLECTION_NAME in existing:
        print(f"[Search] 既存コレクションを削除して再構築します。")
        client.delete_collection(COLLECTION_NAME)

    if not ENRICHED_DATA_PATH.exists():
        raise FileNotFoundError(
            f"{ENRICHED_DATA_PATH} が見つかりません。先に enricher.py を実行してください。"
        )

    with open(ENRICHED_DATA_PATH, "r", encoding="utf-8") as f:
        cases = json.load(f)

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    doc_id = 0
    import time
    
    log_file = open("rebuild_progress.log", "w", encoding="utf-8")
    def log(msg):
        print(msg)
        log_file.write(msg + "\n")
        log_file.flush()

    total_descriptions = sum(len(c.get("descriptions", [])) for c in cases)
    log(f"[Search] Total descriptions to index: {total_descriptions}")

    for case in cases:
        for desc_entry in case.get("descriptions", []):
            description = desc_entry.get("description", "")
            if not description:
                continue

            # Use pre-calculated refined products from enriched_data.json
            refined_products = desc_entry.get("refined_products", [])
            
            metadata = {
                "case_id": case.get("case_id", ""),
                "project_name": case.get("project_name", ""),
                "products": "、".join(refined_products), 
                "location": case.get("location", ""),
                "image_path": desc_entry.get("image_path", ""),
                "url": case.get("url", ""),
            }

            try:
                embedding = get_embedding(description)
                time.sleep(0.5) # Rate limit handling
            except Exception as e:
                log(f"[Search] Embedding Error for {metadata['image_path']}: {e}")
                continue

            collection.add(
                ids=[str(doc_id)],
                documents=[description],
                embeddings=[embedding],
                metadatas=[metadata],
            )
            doc_id += 1
            if doc_id % 10 == 0:
                log(f"[Search] インデックス追加: {metadata['project_name']} ({doc_id}/{total_descriptions})")

    log(f"[Search] インデックス構築完了: {doc_id} 件")
    log_file.close()

    print(f"[Search] インデックス構築完了: {doc_id} 件")
    return collection


def search(query: str, n_results: int = 12) -> list[dict]:
    configure_api()

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    existing = [c.name for c in client.list_collections()]
    if COLLECTION_NAME not in existing:
        raise RuntimeError("インデックスが未構築です。先にインデックスを構築してください。")

    collection = client.get_collection(COLLECTION_NAME)
    query_embedding = get_query_embedding(query)

    # Fetch more results to allow for deduplication
    fetch_count = min(n_results * 5, collection.count())
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=fetch_count,
        include=["documents", "metadatas", "distances"],
    )

    search_results = []
    
    # Deduplication: Group by case_id, keep the best score
    unique_cases = {}
    
    if results and results["ids"] and results["ids"][0]:
        for i, doc_id in enumerate(results["ids"][0]):
            meta = results["metadatas"][0][i]
            case_id = meta.get("case_id", "")
            distance = results["distances"][0][i] if results["distances"] else 0
            
            result_obj = {
                "id": doc_id,
                "case_id": case_id,
                "project_name": meta.get("project_name", ""),
                "products": meta.get("products", ""),
                "location": meta.get("location", ""),
                "image_path": meta.get("image_path", ""),
                "url": meta.get("url", ""),
                "description": results["documents"][0][i],
                "distance": distance,
            }
            
            if case_id not in unique_cases:
                unique_cases[case_id] = result_obj
            else:
                # Update if new one is better (lower distance)
                if distance < unique_cases[case_id]["distance"]:
                    unique_cases[case_id] = result_obj

    # Convert to list, sort by distance, and slice
    search_results = list(unique_cases.values())
    search_results.sort(key=lambda x: x["distance"])
    
    return search_results[:n_results]


def get_similar_by_id(case_id: str, n_results: int = 6) -> list[dict]:
    """
    指定された case_id のベクトルを使って類似案件を検索する (More Like This)
    """
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_collection(COLLECTION_NAME)

    # まず対象のドキュメント（Embedding）を取得
    # メタデータで検索
    target_docs = collection.get(
        where={"case_id": case_id},
        include=["embeddings"]
    )

    embeddings = target_docs.get("embeddings")
    if embeddings is None or len(embeddings) == 0:
        return []

    # 最初のEmbeddingを使って検索 (1つの事例に複数の画像/説明がある場合は平均するか、最初の一つを使う)
    # ここでは単純化のため最初のEmbeddingを使用
    query_embedding = target_docs["embeddings"][0]

    # Fetch more results to allow for deduplication
    fetch_count = min((n_results + 1) * 5, collection.count())

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=fetch_count,
        include=["documents", "metadatas", "distances"],
    )
    
    search_results = []
    unique_cases = {}
    
    if results and results["ids"] and results["ids"][0]:
        for i, doc_id in enumerate(results["ids"][0]):
            meta = results["metadatas"][0][i]
            res_case_id = meta.get("case_id", "")
            distance = results["distances"][0][i]
            
            # 自分自身は除外
            if res_case_id == case_id:
                continue
                
            result_obj = {
                "id": doc_id,
                "case_id": res_case_id,
                "project_name": meta.get("project_name", ""),
                "products": meta.get("products", ""),
                "location": meta.get("location", ""),
                "image_path": meta.get("image_path", ""),
                "url": meta.get("url", ""),
                "description": results["documents"][0][i],
                "distance": distance,
            }
            
            if res_case_id not in unique_cases:
                unique_cases[res_case_id] = result_obj
            else:
                 # Update if new one is better (lower distance)
                if distance < unique_cases[res_case_id]["distance"]:
                    unique_cases[res_case_id] = result_obj

    # Convert to list, sort by distance, and slice
    search_results = list(unique_cases.values())
    search_results.sort(key=lambda x: x["distance"])
    
    return search_results[:n_results]


def get_all_items(n_results: int = 300) -> list[dict]:
    """
    インデックスされている全ての（または指定数の）データを取得する。
    デフォルトの表示や「全件表示」に使用。APIキー不要（ChromaDB読み込みのみ）。
    """
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_collection(COLLECTION_NAME)
    
    # peekだとランダムではないが、全件取得には使える
    # limitより多い場合はgetを使う
    count = collection.count()
    limit = min(n_results, count)
    
    results = collection.get(
        limit=limit,
        include=["documents", "metadatas"]
    )
    
    search_results = []
    unique_cases = {}
    
    if results and results["ids"]:
        for i, doc_id in enumerate(results["ids"]):
            meta = results["metadatas"][i]
            case_id = meta.get("case_id", "")
            
            result_obj = {
                "id": doc_id,
                "case_id": case_id,
                "project_name": meta.get("project_name", ""),
                "products": meta.get("products", ""),
                "location": meta.get("location", ""),
                "image_path": meta.get("image_path", ""),
                "url": meta.get("url", ""),
                "description": results["documents"][i],
                "distance": 0.0, # distance lookup not applicable
            }
            
            if case_id not in unique_cases:
                unique_cases[case_id] = result_obj
            # No distance sorting needed for 'all' view, just distinct case_ids
            
    return list(unique_cases.values())

if __name__ == "__main__":
    build_index()
    results = search("明るく開放的なオフィス空間")
    for r in results:
        print(f"  {r['project_name']} (距離: {r['distance']:.4f})")
