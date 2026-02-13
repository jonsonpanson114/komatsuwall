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

    if ENRICHED_DATA_PATH.exists():
        print("[Enricher] 既存の enriched_data.json を使用します。")
        with open(ENRICHED_DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"{RAW_DATA_PATH} が見つかりません。先に scraper.py を実行してください。"
        )

    with open(RAW_DATA_PATH, "r", encoding="utf-8") as f:
        cases = json.load(f)

    enriched = []
    for case in cases:
        case_enriched = {**case, "descriptions": []}
        for img_path in case.get("local_image_paths", []):
            if not Path(img_path).exists():
                print(f"[Enricher] 画像が見つかりません: {img_path}")
                continue

            print(f"[Enricher] 説明文生成中: {img_path}")
            desc = generate_description(
                model=model,
                image_path=img_path,
                project_name=case.get("project_name", "不明"),
                products=case.get("products", []),
                location=case.get("location", "不明"),
            )
            case_enriched["descriptions"].append(
                {"image_path": img_path, "description": desc}
            )
            time.sleep(1)

        enriched.append(case_enriched)

    with open(ENRICHED_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(enriched, f, ensure_ascii=False, indent=2)

    print(f"[Enricher] 完了: {len(enriched)} 件を {ENRICHED_DATA_PATH} に保存。")
    return enriched


if __name__ == "__main__":
    run_enricher()
