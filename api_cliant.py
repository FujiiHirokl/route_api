# ファイル: api_cliant.py
# 作成者: 藤井広輝
# 更新日: 2023/8/30
# 説明: API呼び出しサンプルプログラム

#必要なライブラリをインポート
import tkinter as tk
import requests

# FastAPIサーバーのURLを設定
api_url = "http://localhost:8000/device_get"  # FastAPIサーバーのURLを適切に設定してください

# 取得ボタンがクリックされたときの処理を定義
def get_data():
    """
    取得ボタンがクリックされたときに実行される関数。
    FastAPIエンドポイントからデータを取得し、ラベルに表示する。
    """
    try:
        # HTTP GETリクエストを送信
        response = requests.get(api_url)

        # レスポンスのステータスコードを確認
        if response.status_code == 200:
            # データをJSON形式で取得
            data = response.json()
            # データをラベルに表示
            result_label.config(text="取得したデータ: " + str(data))
        else:
            result_label.config(text="エラー：HTTPリクエストが失敗しました。ステータスコード: " + str(response.status_code))

    except requests.exceptions.RequestException as e:
        result_label.config(text="エラー：リクエストが失敗しました。詳細: " + str(e))

# Tkinterウィンドウの設定
window = tk.Tk()  # Tkinterウィンドウを作成
window.title("データ取得アプリ")  # ウィンドウのタイトルを設定

# ウィンドウの幅と高さを指定
window.geometry("400x200")  # 幅400ピクセル、高さ200ピクセル

# ラベルを作成
result_label = tk.Label(window, text="")  # ラベルを作成し、初期テキストは空に設定
result_label.pack(pady=10)  # ラベルをウィンドウに配置

# 取得ボタンを作成
get_button = tk.Button(window, text="データを取得", command=get_data)  # ボタンを作成し、クリック時にget_data関数を呼び出すように設定
get_button.pack()  # ボタンをウィンドウに配置

# ウィンドウを表示
window.mainloop()  # Tkinterウィンドウを表示してイベントループを開始
