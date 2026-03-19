---
tags:
  - article
  - Python
aliases: []
slug: 6c7d8e9f-0a1b-2c3d-4e5f-6a7b8c9d0e1f
created: 2026-03-19
updated: 2026-03-19 Thu 23:36
---

PEP 8（Pythonの公式スタイルガイド）では、インポートの記述方法について明確な規則が定められている。

## インポートのグループ分けと順序

ソースコードの冒頭で、以下の順序でインポートをグループ分けし、**各グループの間に空行を1行**入れる。

```python
# 1. 標準ライブラリ
import os
import sys
from pathlib import Path

# 2. サードパーティライブラリ
import numpy as np
import pandas as pd
import requests

# 3. ローカルアプリケーション固有のインポート（自作モジュール）
from my_app.utils import function_a
from my_app.models.user import User
```

各グループ内では **アルファベット順** に並べることが推奨されている。

## `__all__` の配置規則

モジュールレベルの「ダンダー名」（`__all__`、`__version__` など）は、**ドキュメント文字列の直後、かつインポート文（`from __future__` を除く）の前に配置**する。

```python
"""モジュールの説明文"""

__all__ = ["PublicClass", "public_function"]
__version__ = "1.0.0"

import os
import sys

from my_app.utils import function_a
```

## ワイルドカードインポートの回避

`from module import *` は、どの名前が現在の名前空間に存在するかを不明瞭にするため **原則として避ける**。

```python
# 非推奨（何がインポートされるか不明瞭）
from my_app.utils import *

# 推奨（明示的に指定）
from my_app.utils import function_a, function_b
```

## 1行1インポート

複数のモジュールを1行にまとめるのは非推奨。

```python
# 非推奨
import os, sys

# 推奨
import os
import sys
```

`from` を使う場合は例外的に複数を1行にまとめることもある。

```python
# 許容される
from pathlib import Path, PurePath
```

## 関連

- [[Python 絶対インポートと相対インポート]]
- [[Python `__all__` による公開APIの制御]]

引用元: NotebookLM
