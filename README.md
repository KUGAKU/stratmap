# stratmap

ビジネス戦略の仮説を、軸に分解して可視化するツール集。

## Tools

| ツール | 概要 |
|--------|------|
| [想定顧客マッピング](src/customer-hypothesis.html) | 17軸で顧客仮説をレーダー／バブルチャートで可視化 |

## 今後追加予定

- 提供価値マッピング
- 提供方法・チャネル整理
- 競合ポジショニング
- ビジネスモデルキャンバス

## GitHub Pages

`main` ブランチの `index.html` が公開エントリポイント。

Settings → Pages → Source: `main` / `/ (root)` で有効化。

## Dev

依存ライブラリなし。HTMLファイルを直接ブラウザで開くだけで動く。

```shell
stratmap/
├── index.html          # トップページ
├── src/
│   └── customer-hypothesis.html
└── README.md
```
