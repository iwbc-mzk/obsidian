---
tags:
  - article
  - Python
aliases: []
slug: 4b5c6d7e-8f9a-0b1c-2d3e-4f5a6b7c8d9e
created: 2026-03-19
updated: 2026-03-19 Thu 23:22
---

**srcレイアウト**とは、プロジェクトのルート直下に `src/` ディレクトリを作成し、その中に実際のソースコード（パッケージ）を配置するディレクトリ構成。現代のPython開発で推奨される「王道」の構成。

## 標準的なディレクトリ構成

```
my_project/
├── pyproject.toml      # プロジェクトの設定ファイル
├── README.md
├── src/                # ソースコードのルート
│   └── my_app/         # 実際のパッケージ名
│       ├── __init__.py
│       ├── main.py
│       └── utils.py
├── tests/              # テストコード（src の外に配置）
└── docs/               # ドキュメント
```

## srcレイアウトを採用する主なメリット

### 1. 「インストールされていないパッケージ」の誤インポート防止

Pythonはカレントディレクトリにあるフォルダを優先的にインポートする。コードがルート直下にあると、インストール設定が間違っていても「たまたまそこにあるから」動いてしまい、配布先でエラーになることがある。

`src/` を挟むことで、**正しくインストール（開発モード等）しない限りインポートできない制約**が生まれ、配布時と同じクリーンな環境での動作を保証できる。

### 2. テストと本番コードの完全分離

本番コード（`src/`）とテストコード（`tests/`）がディレクトリレベルで分離されるため、テスト用ヘルパーを誤って本番コードで使うミスを防げる。

### 3. 配布・パッケージ化の信頼性

`pip` での配布や CI でのテスト実行時に、実際のユーザーが利用する状態とほぼ同じ条件で動作確認できる。

## 開発の開始手順

```toml
# pyproject.toml の例
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "my_app"
version = "0.1.0"

[tool.setuptools.packages.find]
where = ["src"]
```

```bash
# 開発モードでインストール（editable install）
pip install -e .
# または
poetry install
```

インストール後は絶対インポートで参照できる。

```python
from my_app.utils import function_a
```

## core / infra 分離の考え方

srcレイアウト内でコードをさらに「役割」で分ける設計。

```
src/
└── my_app/
    ├── core/       # ビジネスロジック（外部依存なし・テストしやすい）
    │   └── logic.py
    └── infra/      # 外部との接続（DB・API・ファイルI/O）
        └── db.py
```

- **core/**: 計算ルールや判定ロジック。純粋なPythonに近いほどユニットテストしやすい
- **infra/**: 環境によって変更されやすい処理。テストでのモックも分離しやすい

## 関連

- [[Python 絶対インポートと相対インポート]]
- [[Pythonのパッケージ階層とトップレベルパッケージ]]
- [[poetryの仮想環境作成パスをプロジェクト直下に設定する方法]]

引用元: NotebookLM
