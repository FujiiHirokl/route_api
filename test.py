import requests
import json

def main():
    url = 'http://192.0.0.1:8000/'# 先ほどターミナルに出力されたURL
    data = {
        'cost': 100,
        'tax_rate': 0.1
    }

    # ここでAPIを呼び出す,データはjson形式ではないとエラーが起きる
    res = requests.post(url, json.dumps(data))
    print(res.json())

if __name__ == '__main__':
    main()