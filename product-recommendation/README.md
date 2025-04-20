# 商品推薦システム (Product Recommendation System)

## 概要

このプロジェクトは、Eコマースサイトを想定した商品推薦システムのバックエンドとフロントエンドのサンプル実装です。ユーザーの（ダミー）購入履歴や評価に基づいて、関連商品を推薦する機能を提供します。

バックエンドは Python の FastAPI フレームワーク、フロントエンドは JavaScript/TypeScript の Next.js フレームワークを使用して構築されています。

## 主な技術スタック

* **バックエンド:** FastAPI, SQLAlchemy, Uvicorn, Python
* **フロントエンド:** Next.js, React, Material UI (MUI), TypeScript
* **データベース:** PostgreSQL 13
* **推薦ロジック:** (現在はダミーデータですが、基本的な協調フィルタリング等を実装想定)
* **コンテナ化:** Docker, Docker Compose
* **パッケージ管理:** Poetry (バックエンド), Yarn (フロントエンド)

## 機能・仕様

* **バックエンド API (`backend`):**
    * FastAPI を使用した RESTful API。
    * SQLAlchemy を用いて PostgreSQL データベースと連携。
    * 商品のリスト取得、詳細取得 API を提供。
    * （ダミーの）商品推薦 API を提供。
    * コンテナ起動時にデータベースのテーブル作成と初期データ投入を実行。
* **フロントエンド UI (`frontend`):**
    * Next.js (React) によるユーザーインターフェース。
    * バックエンド API から商品情報や推薦情報を取得して表示。
    * Material UI を使用した基本的なデザイン。
* **データベース (`db`):**
    * PostgreSQL を使用し、商品・ユーザー・購入履歴データを管理。
    * Docker コンテナ内で動作し、データは Docker Volume (`postgres_data`) に永続化。
* **バッチ処理 (`batch`):**
    * データベースの購入履歴データを基に推薦モデルを（再）学習するバッチプロセス（現在はサンプル実装）。
    * コンテナ起動後、DB準備完了を待ってから初回学習を実行し、その後 24 時間ごとに学習を繰り返すループ処理。
    * 学習済みモデルは Docker Volume (`model_data`) 内の `/app/models/recommender.pkl` に保存（される想定）。

## 起動方法

### 前提条件

* Docker Desktop または Docker Engine および Docker Compose がインストールされていること。
* Git がインストールされていること。
* ホストマシンのポート 3000 および 8000 が空いていること。

### セットアップと実行

1.  **リポジトリのクローン:**
    ```bash
    git clone <リポジトリのURL>
    cd product-recommendation
    ```

2.  **環境変数について:**
    * このプロジェクトの基本的な設定（データベース接続情報、API URLなど）は `docker-compose.yml` 内の `environment` セクションに直接記述されています。
    * 通常、本番環境などでは `.env` ファイルを使用して機密情報を管理しますが、このサンプルでは簡単のため直接記述しています。必要に応じて `.env` ファイルを使うように変更してください。
    * `docker-compose.yml` 内で設定されている主な環境変数:
        * `DATABASE_URL`: バックエンドとバッチがDB接続に使用。
        * `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`: DBコンテナの初期設定およびバッチの待機処理で使用。
        * `NEXT_PUBLIC_API_URL`: フロントエンドコンテナ（サーバーサイド）がバックエンドAPIを呼び出す際に使用。
        * `MODEL_PATH`: バッチ処理がモデルを保存/ロードするパス。

3.  **コンテナのビルドと起動:**
    ```bash
    docker-compose up --build
    ```
    * 初回起動時または `--build` オプションを付けた場合、各サービスの Docker イメージがビルドされます。
    * `-d` オプションをつけるとバックグラウンドで起動します (`docker-compose up --build -d`)。

4.  **アクセス:**
    * **フロントエンド:** Web ブラウザで `http://localhost:3000` にアクセスします。
    * **バックエンド API (Swagger UI):** Web ブラウザで `http://localhost:8000/docs` にアクセスすると、利用可能な API のドキュメントが表示され、試すことができます。
    * **バックエンド API (ルート):** `http://localhost:8000/`
    * **バックエンド API (ヘルスチェック):** `http://localhost:8000/health`

5.  **停止:**
    * コンテナを停止するには、`docker-compose up` を実行したターミナルで `Ctrl + C` を押すか、別のターミナルから以下を実行します。
        ```bash
        docker-compose down
        ```
    * データベースのデータやモデルデータを完全に削除したい場合は、`-v` オプションを付けてください。
        ```bash
        docker-compose down -v
        ```

## 使用方法

1.  ブラウザで `http://localhost:3000` にアクセスします。
2.  トップページや商品一覧ページで、商品情報や（ダミーの）推薦情報が表示されることを確認します。
3.  API を直接試したい場合は `http://localhost:8000/docs` を利用します。
    * 例: `GET /api/v1/products/` で商品リストを取得できます。
    * 例: `GET /api/v1/recommendations/` で（ダミーの）推薦リストを取得できます。

## 開発について

* **バックエンド:** `./backend` ディレクトリ内で開発を行います。FastAPI のエンドポイント追加や修正は `backend/app/api/v1/endpoints/` 内のファイルで行い、`backend/app/api/v1/api.py` でルーターをインクルードします。依存関係は `backend/pyproject.toml` で管理されており、`poetry install` や `poetry add` を使用します。
* **フロントエンド:** `./frontend` ディレクトリ内で開発を行います。UI の変更は `frontend/app/` や `frontend/components/` 内のファイルで行います。依存関係は `frontend/package.json` で管理されており、`yarn install` や `yarn add` を使用します。
* **バッチ:** バッチ処理のロジックは `./backend/app/batch/` や `./backend/app/ml/` 内にあります。実行スクリプトは `./scripts/run_batch.sh` です。
