import datetime
import urllib.request
import re
import json
import time
import os
import sys

# 設定データ
CONFIG = {
    "mesmerizer": {
        "name": "メズマライザー",
        "url": "https://www.youtube.com/watch?v=19y8YTbvri8",
        "start_date": datetime.datetime(2025, 8, 2),
        "start_views": 150000000,
        "target_views": 200000000,
        "id": "mesmerizer"
    },
    "shoujoa": {
        "name": "少女A",
        "url": "https://www.youtube.com/watch?v=AqI97zHMoQw",
        "start_date": datetime.datetime(2025, 5, 8),
        "start_views": 150000000,
        "target_views": 200000000,
        "id": "shoujoa"
    }
}

def fetch_view_count(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            # "viewCount":"187078179" の形式を探す
            match = re.search(r'viewCount":"(\d+)"', html)
            if match:
                return int(match.group(1))
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None

def calculate_projection(now, data):
    name = data["name"]
    start_date = data["start_date"]
    current_views = data["current_views"]
    start_views = data["start_views"]
    target_views = data["target_views"]

    days_elapsed = (now - start_date).total_seconds() / (24 * 3600)
    views_gained = current_views - start_views
    pace = views_gained / days_elapsed
    
    views_needed = target_views - current_views
    days_to_go = views_needed / pace
    target_date = now + datetime.timedelta(days=days_to_go)
    
    return {
        "name": name,
        "current_views": current_views,
        "pace": pace,
        "views_needed": views_needed,
        "days_to_go": days_to_go,
        "target_date": target_date
    }

def update_index_html(results):
    index_path = "index.html"
    if not os.path.exists(index_path):
        return

    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()

        for res in results:
            # 1. HTML内の表示用数値を更新
            pattern = rf'id="views-{res["id"]}" class="views-count">[\d,]+<'
            replacement = f'id="views-{res["id"]}" class="views-count">{res["current_views"]:,}<'
            content = re.sub(pattern, replacement, content)

            # 2. JS内のデータを更新
            js_pattern = rf'id: \'{res["id"]}\',\s+name: \'.*?\',\s+start: new Date\(\'.*?\'\),\s+current: \d+'
            js_replacement = f"id: '{res['id']}',\n                    name: '{res['name']}',\n                    start: new Date('{res['start_date'].strftime('%Y/%m/%d')}'),\n                    current: {res['current_views']}"
            content = re.sub(js_pattern, js_replacement, content)

        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error updating index.html: {e}")
        return False

def main():
    now = datetime.datetime.now()
    print(f"\n【YouTubeから最新データを取得中... {now.strftime('%Y/%m/%d %H:%M:%S')}】")
    
    results_for_html = []
    
    for key, data in CONFIG.items():
        views = fetch_view_count(data["url"])
        if views:
            data["current_views"] = views
            res = calculate_projection(now, data)
            res["id"] = data["id"]
            res["start_date"] = data["start_date"]
            results_for_html.append(res)
            
            print(f"--- {res['name']} ---")
            print(f"現在再生数: {res['current_views']:,}")
            # print(f"1日平均: {res['pace']:,.2f} 回/日") # 出力を簡潔に
            print(f"到達予想: {res['target_date'].strftime('%Y/%m/%d %H:%M')}")
        else:
            print(f"--- {data['name']} ---")
            print("再生数の取得に失敗しました。")

    if results_for_html:
        if update_index_html(results_for_html):
            print("index.html を更新しました。")

if __name__ == "__main__":
    if "--loop" in sys.argv:
        print("ループモードで起動しました。2分ごとにYouTubeの再生数を取得して index.html を更新します。")
        print("終了するには Ctrl+C を押してください。")
        try:
            while True:
                main()
                time.sleep(120)
        except KeyboardInterrupt:
            print("\n終了します。")
    else:
        main()
        print("\n※ 'python3 calculate_200m.py --loop' で自動更新モードになります。")
