---
tags:
  - 2025-02-25
  - Python
  - IT
link: "[[2025-02-25]]"
created: 2025-03-09 Sun 23:33
updated: 2026-02-28 Sat 10:56
---
poetry の仮想環境作成パスをプロジェクト直下に設定する。  
下記はローカル（プロジェクト単位）設定。プロジェクト単位で設定する場合は --local を付けずに実行する。

```shell
poetry config virtualenvs.in-project true --local
```

[Poetry: 最初にこれだけおぼえておけば一応使えるメモ](https://zenn.dev/pollenjp/articles/2022-05-29-beginning-poetry#virtualenv%E8%A8%AD%E5%AE%9A)
