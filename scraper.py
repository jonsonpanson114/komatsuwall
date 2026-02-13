"""
小松ウオール工業 施工事例スクレイパー
一覧ページから詳細ページを巡回し、画像・メタデータを収集する。
"""

import json
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.komatsuwall.co.jp"
SEARCH_URL = f"{BASE_URL}/case/search/"
DATA_DIR = Path(__file__).parent / "data"
IMAGES_DIR = DATA_DIR / "images"
RAW_DATA_PATH = DATA_DIR / "raw_data.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def get_detail_links(max_pages: int = 5) -> list[str]:
    """一覧ページから詳細ページへのリンクを取得する。"""
    links = []
    for page in range(1, max_pages + 1):
        url = f"{SEARCH_URL}?page={page}" if page > 1 else SEARCH_URL
        print(f"[Scraper] 一覧ページ取得中: {url}")
        try:
            resp = requests.get(url, headers=HEADERS, timeout=30)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"[Scraper] ページ取得エラー: {e}")
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        page_links = []
        for a_tag in soup.select("a[href*='/case/detail/']"):
            href = a_tag.get("href", "")
            full_url = urljoin(BASE_URL, href)
            if full_url not in links and full_url not in page_links:
                page_links.append(full_url)

        if not page_links:
            print(f"[Scraper] ページ {page} にリンクなし。終了。")
            break

        links.extend(page_links)
        print(f"[Scraper] {len(page_links)} 件のリンクを取得 (合計: {len(links)})")
        time.sleep(1)

    return links


def scrape_detail(url: str) -> dict | None:
    """詳細ページから物件名、場所、製品名、画像URLを取得する。"""
    print(f"[Scraper] 詳細ページ取得中: {url}")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[Scraper] 取得エラー: {e}")
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    project_el = soup.select_one("h4.c-label-row span.main")
    project_name = project_el.get_text(strip=True) if project_el else "不明"

    location_el = soup.select_one("h4.c-label-row span.sub")
    location = location_el.get_text(strip=True) if location_el else "不明"

    product_els = soup.select("div.info-area1 h5")
    products = [el.get_text(strip=True) for el in product_els] if product_els else []

    image_els = soup.select("div.slider-for figure.slider-item img")
    image_urls = []
    for img in image_els:
        src = img.get("src", "")
        if src:
            image_urls.append(urljoin(BASE_URL, src))

    case_id = url.rstrip("/").split("/")[-1]

    return {
        "case_id": case_id,
        "url": url,
        "project_name": project_name,
        "location": location,
        "products": products,
        "image_urls": image_urls,
    }


def download_images(case: dict) -> list[str]:
    """事例の画像をローカルにダウンロードし、パスのリストを返す。"""
    local_paths = []
    for idx, img_url in enumerate(case.get("image_urls", [])):
        filename = f"{case['case_id']}_{idx}.jpg"
        filepath = IMAGES_DIR / filename
        if filepath.exists():
            local_paths.append(str(filepath))
            continue
        try:
            resp = requests.get(img_url, headers=HEADERS, timeout=30)
            resp.raise_for_status()
            filepath.write_bytes(resp.content)
            local_paths.append(str(filepath))
            print(f"[Scraper] 画像保存: {filename}")
        except requests.RequestException as e:
            print(f"[Scraper] 画像DLエラー ({img_url}): {e}")
    return local_paths


def run_scraper(max_pages: int = 1000) -> list[dict]:
    """スクレイピングのメインフロー。"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # 既存データの読み込み (再開用)
    existing_cases = []
    scraped_urls = set()
    if RAW_DATA_PATH.exists():
        print("[Scraper] 既存の raw_data.json を読み込みます。")
        try:
            with open(RAW_DATA_PATH, "r", encoding="utf-8") as f:
                existing_cases = json.load(f)
                for case in existing_cases:
                    scraped_urls.add(case["url"])
        except json.JSONDecodeError:
            print("[Scraper] JSON破損の可能性があります。バックアップを作成して新規作成します。")
            if RAW_DATA_PATH.stat().st_size > 0:
                RAW_DATA_PATH.rename(RAW_DATA_PATH.with_suffix(".json.bak"))

    detail_links = get_detail_links(max_pages=max_pages)
    print(f"[Scraper] 合計 {len(detail_links)} 件のリンクが見つかりました。")

    # 新規リンクのみ抽出
    new_links = [link for link in detail_links if link not in scraped_urls]
    print(f"[Scraper] 新規取得対象: {len(new_links)} 件 (スキップ: {len(detail_links) - len(new_links)} 件)")

    cases = existing_cases
    for i, link in enumerate(new_links):
        case = scrape_detail(link)
        if case:
            local_paths = download_images(case)
            case["local_image_paths"] = local_paths
            cases.append(case)
            
            # 1件ごとに保存 (データ保護)
            with open(RAW_DATA_PATH, "w", encoding="utf-8") as f:
                json.dump(cases, f, ensure_ascii=False, indent=2)
            
            print(f"[Scraper] 進捗: {i + 1}/{len(new_links)} 件完了 (保存済み)")
        
        time.sleep(1)

    print(f"[Scraper] 全完了: {len(cases)} 件を {RAW_DATA_PATH} に保存しました。")
    return cases


if __name__ == "__main__":
    run_scraper(max_pages=1000)
