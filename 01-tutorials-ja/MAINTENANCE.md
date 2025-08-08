# 日本語版メンテナンス手順

## 概要
このディレクトリは `01-tutorials` の日本語版です。原文の更新に追従しながら継続的に翻訳作業を行うための仕組みを提供します。

## ディレクトリ構成
```
01-tutorials-ja/
├── README.md                    # 日本語版メインREADME
├── MAINTENANCE.md              # このファイル
├── sync-status.json            # 同期状況管理
├── scripts/                    # メンテナンス用スクリプト
│   ├── check-updates.py        # 更新チェック
│   ├── sync-structure.py       # 構造同期
│   └── translation-status.py   # 翻訳状況確認
├── glossary/                   # 翻訳用語集
│   ├── technical-terms.json    # 技術用語統一翻訳
│   └── style-guide.md         # 翻訳スタイルガイド
└── [各チュートリアルディレクトリ]
```

## 定期メンテナンス手順

### 1. 更新チェック（週次推奨）
```bash
cd 01-tutorials-ja
python scripts/check-updates.py
```

### 2. 構造同期（新規ファイル/ディレクトリ追加時）
```bash
python scripts/sync-structure.py
```

### 3. 翻訳状況確認
```bash
python scripts/translation-status.py --format table
```

### 4. 翻訳作業
1. 更新が必要なファイルを特定
2. 原文と日本語版を比較
3. 翻訳作業実施
4. メタデータファイル更新

## 翻訳ガイドライン

### ファイル命名規則
- ディレクトリ名・ファイル名: 英語のまま維持
- 内容のみ日本語化

### 翻訳対象
- README.mdファイル
- Jupyterノートブック（.ipynb）のマークダウンセルとコメント
- Pythonファイル内のコメントとdocstring

### 維持するもの
- 技術ファイル名（.sh, .json, .py等）
- 設定ファイルの内容
- コード自体の変数名や関数名

## メタデータ管理

各翻訳ファイルには以下の情報を記録：
- 原文の最終更新日時
- 翻訳完了日時
- 翻訳者情報
- レビュー状況

## トラブルシューティング

### 同期エラーが発生した場合
1. `sync-status.json` の内容を確認
2. 原文ディレクトリの存在確認
3. 権限問題の確認

### 翻訳の品質管理
1. 用語集との整合性確認
2. スタイルガイドの遵守
3. 技術的正確性の検証
