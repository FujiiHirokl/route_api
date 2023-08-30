# route_api

**AGVプログラムAPI** - このプロジェクトの簡単な説明

## 目次

- [概要](#概要)
- [エンドポイント](#エンドポイント)
- [依存関係](#依存関係)
- [設定](#設定)
- [使用方法](#使用方法)
- [貢献](#貢献)
- [ライセンス](#ライセンス)

## 概要

このプロジェクトは、FastAPIを使用してAPIを実装し、MySQLデータベースとやり取りするためのものです。主な機能は以下の通りです。

- データベースからデータを取得するエンドポイント
- デバイスの情報を取得するエンドポイント
- デバイスの座標を更新するエンドポイント
- 測定データから位置座標を推定するエンドポイント

## エンドポイント

### `GET /get_all_data`

全てのデータを取得するエンドポイントです。

### `GET /get_all_data_mame`

経路名を取得するエンドポイントです。

### `GET /get_route_data/{route_number}`

指定された経路番号のxとyを順番の順に取得するエンドポイントです。

### `GET /device_get`

マイクの情報を取得するエンドポイントです。

### `POST /update_coordinates`

デバイスの座標を更新するエンドポイントです。

### `POST /math_coordinates`

測定データから位置座標を推定するエンドポイントです。

## 依存関係

このプロジェクトは以下のライブラリに依存しています。

- `numpy`
- `fastapi`
- `pydantic`
- `mysql-connector-python`

## 設定

このプロジェクトは、MySQLデータベースへの接続情報を含んでいます。必要に応じて、接続情報を変更してください。

## 使用方法

1. 依存関係をインストールします。以下のコマンドを実行してください。

    ```
    pip install numpy　uvicorn fastapi pydantic mysql-connector-python
    ```

2. プロジェクトディレクトリに移動します。

3. FastAPIアプリケーションを起動します。

    ```
    #自分のPC内で使う場合
    uvicorn main:app --host 127.0.0.1 --port 8000 --reload
    #内部ネットワークに公開する場合
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```

4. APIエンドポイントにアクセスしてください。

## 貢献

プロジェクトに貢献したい場合は、プルリクエストを送信してください。バグ修正、新機能の提案、ドキュメンテーションの改善など、どのような貢献も歓迎します。

## ライセンス

このプロジェクトはMITライセンスの下で提供されています。詳細については、[LICENSE.md](LICENSE.md)ファイルをご覧ください。
