---
tags:
  - article
  - Python
aliases: []
slug: 8f9a0b1c-2d3e-4f5a-6b7c-8d9e0f1a2b3c
created: 2026-03-19
updated: 2026-03-19 Thu 23:22
---

Pythonのパッケージ構造では、**トップレベルパッケージ**とその下の**サブパッケージ**が階層を形成する。この階層構造がインポートの起点と相対インポートの限界を決める。

## トップレベルパッケージとは

`sys.path`（検索パス）に含まれるディレクトリの直下にあるパッケージが **トップレベルパッケージ**。

```
src/ (← sys.path に追加されるルート)
└── my_app/           ← これがトップレベルパッケージ
    ├── __init__.py
    ├── utils.py
    └── models/       ← これは my_app のサブパッケージ
        ├── __init__.py
        └── user.py
```

- **絶対インポートの起点**: `from my_app.models.user import User` の `my_app` がトップレベル
- **相対インポートの限界点**: `..` で遡れる「壁」。トップレベルより外へは出られない

## サブパッケージの判断基準

`models/` フォルダが `my_app/` の中に物理的に配置されており、かつ `my_app/` 自体も `__init__.py` を持つ場合、`models` は独立したトップレベルではなく `my_app` のサブパッケージとして扱われる。

```python
# models が my_app のサブパッケージである証拠：
# 他の場所から参照する際に my_app を起点とする
from my_app.models.user import User
#    ^^^^^^ トップレベル
#           ^^^^^^ サブパッケージ
```

## `user.py` から親階層の `utils.py` をインポートできる理由

```python
# user.py (src/my_app/models/user.py) から
from ..utils import function_a  # 相対インポートで親へ遡れる
```

`my_app` がトップレベルパッケージとして `models` と `utils` の両方をその傘下に収めているため、サブパッケージ間での相対インポートが可能。

## `models` がトップレベルになってしまうケース

`src/my_app/` ディレクトリ自体を `sys.path` に追加した場合、`models` がトップレベルとして振る舞う。

**問題点**:
- `models` が最上位になると、`utils.py` はパッケージ外の存在となる
- `..utils` の相対インポートが `ImportError` になる
- これが `sys.path.append()` を避けるべき理由の一つ

## `__init__.py` の役割

`__init__.py` を配置することでPythonはそのディレクトリを「パッケージ」と認識する。

```python
# __init__.py 内で __all__ を定義して公開APIを制御できる
from .sub_module_a import func_a
__all__ = ["func_a"]
```

- Python 3.3以降は必須ではないが、IDEの補完・pytest等の動作安定のために配置を推奨
- [[Python `__all__` による公開APIの制御]] を使って再エクスポートの整理もできる

## 関連

- [[Python 絶対インポートと相対インポート]]
- [[Python `__all__` による公開APIの制御]]
- [[Python srcレイアウト]]

引用元: NotebookLM
