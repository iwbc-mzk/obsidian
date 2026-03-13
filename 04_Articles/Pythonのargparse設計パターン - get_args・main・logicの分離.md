---
slug: 9027751c-7b41-4a21-a0c3-2b9461826877
tags:
  - article
  - Python
  - argparse
  - CLI
source:
created: 2026-03-10 Tue 23:09
updated: 2026-03-13 Fri 14:05
---

## 概要

Pythonの `argparse` を使ったコマンドライン引数の解析処理を、テスト可能で再利用性の高い構成に設計するパターン。

## 問題：パース処理をどこに書くべきか

`if __name__ == "__main__":` の直下にすべてのパース処理を書き込むと以下の問題が生じる。

- **テストが困難**: `if __name__ == "__main__":` ブロック内のコードは、他のファイルからインポートした際に実行されないため、ユニットテストで検証できない
- **再利用性が低い**: 他のスクリプトからインポートして利用する際、コマンドラインを経由せずに引数を渡せない
- **グローバル変数の発生リスク**: ブロック内で直接変数を定義するとグローバル変数になる可能性がある

## ベストプラクティス：CLIとロジックを分離する

### 推奨される関数の役割分担

| 関数 | 役割 |
|------|------|
| `get_args()` | `argparse` を使って引数を定義・パースする |
| `run_process(param1, param2, ...)` | 実際の処理ロジック（`argparse` に依存しない） |
| `main()` | `get_args()` を呼び出し、結果を `run_process()` に配分する差配役 |
| `if __name__ == "__main__":` | `main()` の呼び出しのみ |

### 推奨テンプレート

```python
import argparse

def get_args():
    """引数の定義とパースを行う関数"""
    parser = argparse.ArgumentParser(description="データの集計を行うツール")

    # 型変換(type)やデフォルト値(default)をここで完結させる
    parser.add_argument("--env", default="dev", help="実行環境（dev/prod）")
    parser.add_argument("--date", required=True, help="処理対象の日付（YYYY-MM-DD）")
    parser.add_argument("--count", type=int, default=10, help="処理件数")

    return parser.parse_args()

def run_process(env, date, count):
    """
    実際のロジックを担当する関数。
    argparseに依存せず、具体的な引数を明示的に受け取る。
    """
    print(f"環境: {env}, 日付: {date}, 件数: {count} で処理を開始します...")
    # ここに具体的な処理を記述する

def main():
    """
    プログラムの起点となる差配役（ディスパッチャ）。
    引数を取得し、各関数に必要な値を渡す。
    """
    args = get_args()

    # 方法A: 必要な引数を個別に明示して渡す（最も推奨：可読性が高い）
    run_process(
        env=args.env,
        date=args.date,
        count=args.count
    )

    # 方法B: 辞書展開（アンパック）を使って渡す（引数が多い場合に便利）
    # params = vars(args)
    # run_process(**params)

if __name__ == "__main__":
    # スクリプトとして実行された時のみmainを呼び出す
    main()
```

## メリット

### 1. テストの容易性

`get_args()` と `run_process()` を個別にユニットテストできる。

- `run_process()` は `argparse.Namespace` オブジェクトを模倣（モック）せずとも、単純な値を渡すだけでテスト可能

### 2. 再利用性とモジュール化

`run_process()` は `argparse` に依存しないため、他スクリプトから直接インポートして利用できる。

```python
from script import run_process
run_process("prod", "2025-03-10", 100)
```

### 3. グローバル変数の回避

`main()` 内で変数を定義することで、変数のスコープを関数内に限定できる。

### 4. `if __name__ == "__main__":` との組み合わせが必須

`argparse` と `if __name__ == "__main__":` を組み合わせないと、他スクリプトがこのモジュールをインポートしただけで引数のパース（とエラー時のプログラム終了）が実行されてしまう。

## 関連記事

- [[vars(args)でargparseのNamespaceを辞書にアンパックする]]

引用元: NotebookLM
