"""
Gemini 2.5 Flash Lite を使用した画像説明文・タグ生成モジュール。
"""

import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

load_dotenv()

DATA_DIR = Path(__file__).parent / "data"
RAW_DATA_PATH = DATA_DIR / "raw_data.json"
ENRICHED_DATA_PATH = DATA_DIR / "enriched_data.json"

PROMPT_TEMPLATE = """この画像は『{project_name}』の施工事例で、使用製品は『{products}』、場所は『{location}』です。
これらを踏まえた上で、この空間の『雰囲気』『配色』『デザインの特徴』『利用シーン』を詳細に記述し、検索用のキーワードを生成してください。
事実は正確に、感性は豊かに記述してください。"""


def configure_api():
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY または GEMINI_API_KEY 環境変数を設定してください。"
        )
    genai.configure(api_key=api_key)


def generate_description(
    model: genai.GenerativeModel,
    image_path: str,
    project_name: str,
    products: list[str],
    location: str,
) -> str:
    prompt = PROMPT_TEMPLATE.format(
        project_name=project_name,
        products="、".join(products) if products else "不明",
        location=location,
    )
    try:
        img = Image.open(image_path)
        response = model.generate_content([prompt, img])
        return response.text.strip()
    except Exception as e:
        print(f"[Enricher] 生成エラー ({image_path}): {e}")
        return ""


def run_enricher() -> list[dict]:
    configure_api()
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    # 既存データの読み込み (再開用)
    enriched_map = {}
    if ENRICHED_DATA_PATH.exists():
        print("[Enricher] 既存の enriched_data.json を読み込みます。")
        try:
            with open(ENRICHED_DATA_PATH, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
                for item in existing_data:
                    enriched_map[item["case_id"]] = item
        except json.JSONDecodeError:
            print("[Enricher] JSON破損。バックアップして新規作成します。")
            ENRICHED_DATA_PATH.rename(ENRICHED_DATA_PATH.with_suffix(".json.bak"))

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"{RAW_DATA_PATH} が見つかりません。先に scraper.py を実行してください。"
        )

    with open(RAW_DATA_PATH, "r", encoding="utf-8") as f:
        raw_cases = json.load(f)

    print(f"[Enricher] 合計 {len(raw_cases)} 件のデータを処理対象とします。")

    enriched_list = []
    
    for i, case in enumerate(raw_cases):
        case_id = case["case_id"]
        
        # 既に処理済みで、画像数も一致しているか確認
        if case_id in enriched_map:
            existing_case = enriched_map[case_id]
            # 画像パスのリストが存在し、処理済みの説明文数と一致すればスキップ
            raw_img_count = len(case.get("local_image_paths", []))
            enriched_desc_count = len(existing_case.get("descriptions", []))
            
            if raw_img_count == enriched_desc_count:
                enriched_list.append(existing_case)
                # print(f"[Enricher] スキップ (完了済み): {case_id}")
                continue
        
        # ここに来たら処理が必要
        print(f"[Enricher] 処理中 ({i+1}/{len(raw_cases)}): {case['project_name']}")
        
        case_enriched = {**case, "descriptions": []}
        
        # 既存の説明文があれば引き継ぐ (部分的な再開用)
        existing_descs = {}
        if case_id in enriched_map:
             for desc in enriched_map[case_id].get("descriptions", []):
                 existing_descs[desc["image_path"]] = desc["description"]

        for img_path in case.get("local_image_paths", []):
            if not Path(img_path).exists():
                print(f"[Enricher] 画像が見つかりません: {img_path}")
                continue

            # 既にこの画像の生成済みデータがあればそれを使う
            if img_path in existing_descs:
                description = existing_descs[img_path]
            else:
                print(f"  - 生成中: {Path(img_path).name}")
                description = generate_description(
                    model=model,
                    image_path=img_path,
                    project_name=case.get("project_name", "不明"),
                    products=case.get("products", []),
                    location=case.get("location", "不明"),
                )
                time.sleep(2) # レート制限への配慮

            case_enriched["descriptions"].append(
                {"image_path": img_path, "description": description}
            )
        
        enriched_list.append(case_enriched)
        
        # 1件ごとに保存
        with open(ENRICHED_DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(enriched_list, f, ensure_ascii=False, indent=2)

    print(f"[Enricher] 全完了: {len(enriched_list)} 件を {ENRICHED_DATA_PATH} に保存しました。")
    return enriched_list


if __name__ == "__main__":
    run_enricher()
