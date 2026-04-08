# stratmap AI インタビュー

対話を通じてビジネス戦略の仮説を整理し、戦略マップにマッピングする AI インタビューツール。

## 技術スタック

- Python 3.11
- FastAPI + Uvicorn
- Anthropic Claude API

## セットアップ

### 1. 環境変数の設定

```bash
cp .env.example .env
```

`.env` を編集して Anthropic API キーを設定する。

```
ANTHROPIC_API_KEY=sk-ant-...
```

### 2. 依存関係のインストール

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. サーバー起動

```bash
uvicorn main:app --reload
```

http://localhost:8000 にアクセスするとチャット UI が開く。

## API エンドポイント

| メソッド | パス | 説明 |
|---------|------|------|
| POST | `/session` | 新規セッション作成 |
| POST | `/session/{id}/message` | メッセージ送信 |
| GET | `/session/{id}` | セッション状態取得 |
| GET | `/session/{id}/export` | JSON エクスポート |
| GET | `/session/{id}/report` | HTML レポート表示 |
