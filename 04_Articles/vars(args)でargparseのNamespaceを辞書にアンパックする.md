---
tags:
  - article
  - Python
  - argparse
  - CLI
source:
created: 2026-03-10 Tue 23:10
updated: 2026-03-10 Tue 23:10
---

## 概要

`argparse` の `parse_args()` が返す `Namespace` オブジェクトを、`vars()` を使って辞書に変換し、`**` でアンパックしてロジック関数に渡すテクニック。

[[Pythonのargparse設計パターン - get_args・main・logicの分離]] で示す設計パターンにおける、より高度な引数の受け渡し方法。

## 基本的な使い方

```python
# 1. パース結果 (Namespace)
args = parser.parse_args()

# 2. 辞書に変換 (vars)
args_dict = vars(args)  # {'env': 'prod', 'count': 10} となる

# 3. アンパックして関数に投入 (**)
# 内部で logic_function(env='prod', count=10) として実行される
logic_function(**args_dict)
```

> **仕組み**: Pythonのオブジェクトは内部的に `__dict__` 属性で値を管理しており、組み込み関数 `vars()` はこの `__dict__` を返す。

## メリット

### 1. ロジックとCLIの完全な分離（疎結合）

`main(args)` のように `Namespace` オブジェクトを直接渡すと、受け取り側の関数は `argparse` の仕様に依存してしまう。

`vars(args)` でアンパックすれば、ロジック関数は `argparse` の存在を一切知る必要がない。

```python
# 悪い例: Namespaceへの依存
def run(args):
    env = args.env  # argparseの属性名に依存

# 良い例: 具体的な引数を明示
def run(env, date, count):  # 何が必要か一目瞭然
    pass
```

### 2. 関数シグネチャの明確化

| 方法 | シグネチャ | 何が必要かわかるか |
|------|-----------|-----------------|
| Namespace直接渡し | `def run(args):` | ❌ 不明 |
| アンパック | `def run(env, date, count):` | ✅ 明確 |

### 3. テストの容易性

アンパックして個別の値を受け取る構成にすると、ユニットテストで `argparse.Namespace` を模倣（モック）する必要がなくなる。

```python
# テストがシンプルになる
def test_run_process():
    run_process("dev", "2025-03-10", 10)  # 単純な値を渡すだけ
```

### 4. データクラスへの橋渡し

`vars(args)` で取得した辞書を型定義されたデータクラスに変換することで、型安全なオブジェクトとして保持できる。

```python
from dataclasses import dataclass

@dataclass
class Config:
    env: str
    date: str
    count: int

def main():
    args = get_args()
    config = Config(**vars(args))
    run_process(config)
```

## 実装例（推奨パターン）

```python
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="データの集計を行うツール")
    parser.add_argument("--env", default="dev")
    parser.add_argument("--date", required=True)
    parser.add_argument("--count", type=int, default=10)
    return parser.parse_args()

def run_process(env, date, count):
    print(f"環境: {env}, 日付: {date}, 件数: {count}")

def main():
    args = get_args()

    # vars(args)で辞書に変換してアンパック
    run_process(**vars(args))

if __name__ == "__main__":
    main()
```

## 注意点

- `argparse` の引数名（`--my-arg`）はアンダースコア形式（`my_arg`）で辞書に格納される
- 受け取り側の関数の引数名が `argparse` の定義と一致している必要がある
- 引数の追加・削除時は関数シグネチャとの整合性を保つこと

## 関連記事

- [[Pythonのargparse設計パターン - get_args・main・logicの分離]]

引用元: NotebookLM
