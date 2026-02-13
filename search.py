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
CHROMA_DIR = DATA_DIR / "chroma_db"

COLLECTION_NAME = "komatsu_cases"
EMBEDDING_MODEL = "models/gemini-embedding-001"


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
        collection = client.get_collection(COLLECTION_NAME)
        if collection.count() > 0:
            print(f"[Search] 既存インデックスを使用 ({collection.count()} 件)")
            return collection
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
    for case in cases:
        for desc_entry in case.get("descriptions", []):
            description = desc_entry.get("description", "")
            if not description:
                continue

            embedding = get_embedding(description)
            metadata = {
                "case_id": case.get("case_id", ""),
                "project_name": case.get("project_name", ""),
                "products": "、".join(case.get("products", [])),
                "location": case.get("location", ""),
                "image_path": desc_entry.get("image_path", ""),
                "url": case.get("url", ""),
            }

            collection.add(
                ids=[str(doc_id)],
                documents=[description],
                embeddings=[embedding],
                metadatas=[metadata],
            )
            doc_id += 1
            print(f"[Search] インデックス追加: {metadata['project_name']} ({doc_id})")

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

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n_results, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    search_results = []
    if results and results["ids"] and results["ids"][0]:
        for i, doc_id in enumerate(results["ids"][0]):
            meta = results["metadatas"][0][i]
            search_results.append(
                {
                    "id": doc_id,
                    "project_name": meta.get("project_name", ""),
                    "products": meta.get("products", ""),
                    "location": meta.get("location", ""),
                    "image_path": meta.get("image_path", ""),
                    "url": meta.get("url", ""),
                    "description": results["documents"][0][i],
                    "distance": results["distances"][0][i],
                }
            )

    return search_results


if __name__ == "__main__":
    build_index()
    results = search("明るく開放的なオフィス空間")
    for r in results:
        print(f"  {r['project_name']} (距離: {r['distance']:.4f})")
