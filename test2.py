import requests

# リクエストデータの準備
data = {
    "d1": 10.0,  # 例：d1, d2, d3, d4 の値を適切に設定してください
    "d2": 15.0,
    "d3": 20.0,
    "d4": 25.0
}

# APIエンドポイントのURL
url = "http://localhost:8000/math_coordinates"  # ローカルで実行している場合

# POSTリクエストを送信
response = requests.post(url, json=data)

# レスポンスの表示
if response.status_code == 200:
    result = response.json()
    print("推定された位置座標:", result["estimated_position"])
else:
    print("APIリクエストが失敗しました。ステータスコード:", response.status_code)
