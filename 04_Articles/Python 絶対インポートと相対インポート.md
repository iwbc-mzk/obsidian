---
tags:
  - article
  - Python
aliases: []
slug: f3a2b1c0-d4e5-4f6a-8b9c-0d1e2f3a4b5c
created: 2026-03-19
updated: 2026-03-19 Thu 23:36
---

Pythonのインポートには **絶対インポート** と **相対インポート** の2種類がある。用途に応じた使い分けが保守性に直結する。

## 絶対インポート

プロジェクトのルート（`sys.path` に含まれるディレクトリ）からのフルパスを指定する。

```python
# main.py から utils.py の関数を呼ぶ
from my_app.utils import function_a

# main.py から models/user.py のクラスを呼ぶ
from my_app.models.user import User
```

- どこから呼んでも同じパスで参照できる
- [[PEP 8 インポートの記述規則]] で公式に推奨されている
- IDEの補完・静的解析ツールとの相性が良い

## 相対インポート

現在のファイルの位置を基準にドット（`.`）で指定する。パッケージ内のモジュール間連携で便利。

```python
# 同じパッケージ内の __init__.py を参照
from . import something

# 同階層の別モジュールを参照
from .utils import function_a

# 親パッケージのモジュールを参照
from ..utils import function_a
```

### 相対インポートの注意点

相対インポートを含むファイルを直接 `python user.py` のように実行すると `ImportError` が発生する。

```bash
# 誤った実行方法（ImportError になる）
python src/my_app/models/user.py

# 正しい実行方法（-m オプションでパッケージとして実行）
python -m my_app.models.user
```

**理由**: 直接実行するとスクリプトとして動作し、親パッケージが不明になるため相対インポートが解決できない。

## 比較まとめ

| 項目 | 絶対インポート | 相対インポート |
|------|--------------|--------------|
| 記法 | `from my_app.utils import f` | `from ..utils import f` |
| 推奨度 | PEP 8 公式推奨 | パッケージ内のみ可 |
| リファクタリング | パッケージ名変更で全修正必要 | 相対位置が変わらなければ影響なし |
| 直接実行 | 可能 | `-m` オプション必須 |

## 関連

- [[PEP 8 インポートの記述規則]]
- [[Pythonのパッケージ階層とトップレベルパッケージ]]
- [[Python srcレイアウト]]

引用元: NotebookLM
