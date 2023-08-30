import requests

# FastAPIサーバーのURL
api_url = "http://localhost:8000/device_get"  # FastAPIサーバーのURLを適切に設定してください

try:
    # HTTP GETリクエストを送信
    response = requests.get(api_url)

    # レスポンスのステータスコードを確認
    if response.status_code == 200:
        # データをJSON形式で取得
        data = response.json()
        # データの処理
        print("取得したデータ:", data)
    else:
        print("エラー:HTTPリクエストが失敗しました。ステータスコード:", response.status_code)

except requests.exceptions.RequestException as e:
    print("エラー：リクエストが失敗しました。詳細:", e)

