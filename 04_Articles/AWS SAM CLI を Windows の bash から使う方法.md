---
tags:
  - article
  - AWS
  - SAM
  - Windows
  - Shell
aliases: []
slug: a3f8b2c1-d4e5-6f70-8901-2b3c4d5e6f71
created: 2026-05-11
updated: 2026-05-11 Mon 23:42
---

# AWS SAM CLI を Windows の bash から使う方法

## 問題

AWS SAM CLI の Windows 版をインストールすると `sam.cmd` が追加され、PowerShell やコマンドプロンプトからは使えるが、Git Bash や WSL2 などの bash 環境からは `.cmd` ファイルを実行できない。

## 環境

- Windows 10/11
- SAM CLI（Windows 版インストーラでインストール済み）
- Git Bash または WSL2

## 原因

デフォルトインストール先（`C:\Program Files\Amazon\AWSSAMCLI\bin`）には `sam.cmd` のみが配置されており、bash からは実行できない。

`sam.cmd` の中身は Python を呼び出しているだけ：

```bat
@rem
@echo off

setlocal

"%~dp0/../runtime/python.exe" -m samcli %*
```

## 解決方法：同等のシェルスクリプトを作成する

同じディレクトリに `sam` という名前のシェルスクリプトを作成する。

```bash
#!/bin/bash

SELF_DIR=$(dirname "$0")

"$SELF_DIR/../runtime/python.exe" -m samcli $*
```

**配置先：** `C:\Program Files\Amazon\AWSSAMCLI\bin\sam`（拡張子なし）

これで bash から `sam` コマンドが使えるようになる。

## まとめ

| 方法 | 対応シェル |
|------|-----------|
| `sam.cmd` | PowerShell / コマンドプロンプト |
| `sam`（シェルスクリプト） | Git Bash / WSL2 |

引用元: [【AWS】aws-sam-cli をWindowsでbashから使うメモ](https://qiita.com/umaxyon/items/b887010f916bcb96bcbd)
