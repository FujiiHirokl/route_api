import requests

def main():
    url = 'http://127.0.0.1:8000/update_coordinates'
    data = {
        'device_id': 4,
        'new_x': 490,
        'new_y': 490
    }
    res = requests.post(url, json=data)  # 辞書形式のデータを直接渡す
    print(res.json())

if __name__ == '__main__':
    main()
