import datetime

# 現在の時刻を自動取得
now = datetime.datetime.now()

# 設定データ
# メズマライザー (1.5億回達成: 2025/08/02)
mes_150m_date = datetime.datetime(2025, 8, 2)
mes_current_views = 186933034
mes_target_views = 200000000

# 少女A (1.5億回達成: 2025/05/08)
shoujo_150m_date = datetime.datetime(2025, 5, 8)
shoujo_current_views = 190970443
shoujo_target_views = 200000000

def calculate_projection(name, start_date, current_views, start_views=150000000, target_views=200000000):
    # 1.5億回達成からの経過日数
    days_elapsed = (now - start_date).total_seconds() / (24 * 3600)
    views_gained = current_views - start_views
    pace = views_gained / days_elapsed # 1日あたりの平均再生数
    
    # 2億回までの残り
    views_needed = target_views - current_views
    days_to_go = views_needed / pace
    
    target_date = now + datetime.timedelta(days=days_to_go)
    
    print(f"--- {name} ---")
    print(f"計測基準日(1.5億): {start_date.strftime('%Y/%m/%d')}")
    print(f"現在再生数: {current_views:,}")
    print(f"1.5億からの経過日数: {days_elapsed:.2f} 日")
    print(f"1日あたりの平均再生数: {pace:,.2f} 回/日")
    print(f"2億回まであと: {views_needed:,} 回")
    print(f"到達予想までの日数: {days_to_go:.2f} 日")
    print(f"到達予想日: \033[1m{target_date.strftime('%Y/%m/%d %H:%M')}\033[0m")
    return target_date

print(f"【計算実行日時: {now.strftime('%Y/%m/%d %H:%M:%S')}】")
results = [
    ("メズマライザー", calculate_projection("メズマライザー", mes_150m_date, mes_current_views)),
    ("少女A", calculate_projection("少女A", shoujo_150m_date, shoujo_current_views))
]

# どちらが早いか判定
results.sort(key=lambda x: x[1])
print(f"\n★先に2億回に到達するのは: \033[1;32m{results[0][0]}\033[0m ({results[0][1].strftime('%Y/%m/%d')} 予想)")
