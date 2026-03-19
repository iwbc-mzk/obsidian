---
tags:
  - article
  - Python
aliases: []
slug: 2e3f4a5b-6c7d-8e9f-0a1b-2c3d4e5f6a7b
created: 2026-03-19
updated: 2026-03-19 Thu 23:22
---

`__all__` はモジュールやパッケージが外部に対して公開する「公開API」を明示的に定義する仕組み。`from module import *` 実行時にロードされる識別子を制限できる。

## モジュールレベルでの公開API制限

```python
"""モジュールの説明文"""

# __all__ はドキュメント文字列の直後、import文の前に配置する
__all__ = ["PublicClass", "public_function"]

class PublicClass:
    pass

def public_function():
    return "This is a public API"

def _internal_function():
    # アンダースコアで始まる名前は通常公開されない
    pass

def hidden_function():
    # __all__ に含まれていないため、import * では無視される
    pass
```

### 挙動の違い

```python
# ワイルドカードインポート → __all__ に含まれるものだけがインポートされる
from mymodule import *
# PublicClass と public_function のみ使用可能

# 明示的なインポート → __all__ に関係なくインポート可能
from mymodule import hidden_function  # これは可能
```

**`__all__` は厳密なアクセス制限ではなく、外部への「公開API案内板」**。明示的なインポートは制限されない。

## パッケージ（`__init__.py`）での再エクスポート

複雑な内部構造を隠しつつ、パッケージのトップレベルから使える機能を整理できる。

```
my_package/
├── __init__.py
├── sub_module_a.py  # func_a が定義されている
└── sub_module_b.py  # func_b が定義されている
```

```python
# my_package/__init__.py
from .sub_module_a import func_a
from .sub_module_b import func_b

__all__ = ["func_a", "func_b"]
```

これにより利用者は内部構造を意識せず使える。

```python
# 長い記法
from my_package.sub_module_a import func_a

# __init__.py の __all__ により簡潔に書ける
from my_package import func_a
```

## 公開APIを「なし」に設定する

すべて内部用のモジュールであることを明示する場合は空リストを設定する。

```python
__all__ = []  # このモジュールには公開APIがないことを示す
```

## アンダースコアとの併用

`__all__` が定義されていない場合でも、先頭にアンダースコア（`_`）を付けた名前は `import *` でエクスポートされない慣習がある。

```python
def _internal():  # import * では無視される
    pass

def public():  # import * でエクスポートされる
    pass
```

## 配置場所（PEP 8）

[[PEP 8 インポートの記述規則]] に基づき、`__all__` はモジュールのドキュメント文字列の直後、かつインポート文の前に配置する。

## 関連

- [[PEP 8 インポートの記述規則]]
- [[Pythonのパッケージ階層とトップレベルパッケージ]]
- [[Python 絶対インポートと相対インポート]]

引用元: NotebookLM
