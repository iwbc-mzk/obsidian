---
tags:
  - article
  - Shell
  - Linux
aliases: []
slug: c5d0e4f3-f6a7-8b92-0123-4d5e6f7a8b93
created: 2026-05-11
updated: 2026-05-11 Mon 23:43
---

# シェルリダイレクトの応用 - tee・ヒアドキュメント・exec

[[ファイルディスクリプタとシェルリダイレクトの基礎]] の続き。実務でよく使うリダイレクト応用テクニックをまとめる。

## パイプと tee コマンド

パイプ `|` を使うと、コマンドの stdout を次のコマンドの stdin に渡せる。

### tee：画面表示しつつファイルにも保存

パイプで繋ぐと出力が次のコマンドに渡ってしまい、画面には表示されなくなる。「画面でも確認したいし、ログファイルにも保存したい」場合は `tee` が便利。

```bash
# コマンドの実行結果を画面に表示しつつ、result.txt にも保存
ls -l | tee result.txt

# 追記モード（-a オプション）
echo "New entry" | tee -a result.txt
```

## ヒアドキュメント（Here Document）

スクリプト内に複数行テキストを埋め込んだり、対話的コマンドに自動入力を与える場合に使う。

```bash
# cat コマンドに複数行のテキストを渡す
cat << EOF > config.txt
Host example.com
    User admin
    Port 22
EOF
```

- `EOF` は終端文字列（End Marker）で、任意の文字列（`END`、`LIMIT` など）が使える
- `EOF` が最も慣用的

### ヒアドキュメントでファイル作成

```bash
cat << 'EOF' > script.sh
#!/bin/bash
echo "Hello, World!"
EOF
```

シングルクォートで囲むと変数展開を防げる。

## exec によるログ出力の恒久化

スクリプト内の全出力をログファイルに保存したい場合、`exec` でシェル自体の FD を操作する。

```bash
#!/bin/bash

LOG_FILE="script.log"

# 標準出力(1)と標準エラー出力(2)をログファイルに向ける
exec 1>>"$LOG_FILE" 2>&1

echo "これはログファイルに書き込まれます"
echo "エラーもログファイルへ" >&2
```

この設定以降、スクリプト内の全出力が自動的に `script.log` に追記される。

## 実務での使いどころ

| シナリオ | 使うテクニック |
|----------|---------------|
| cronのログ集約 | `2>&1` または `&>` |
| Docker / CI の実行ログ | `tee` で画面+ファイル |
| サーバ起動スクリプト | `exec` でFD恒久変更 |
| スクリプトへの設定埋め込み | ヒアドキュメント |
| 出力を完全に捨てる | `> /dev/null 2>&1` |

引用元: [シェルスクリプト ファイル記述子とリダイレクトの仕組み](https://qiita.com/yam_dev/items/d5ca43563331bc3f80df) / [FDリダイレクトとは？](https://zenn.dev/waffledog/scraps/f017f8c5068674)
