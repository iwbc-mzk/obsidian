---
tags:
  - article
  - Windows
  - CLI
aliases: []
slug: b0c5d9e8-e1f2-3a47-5678-9c0d1e2f3a48
created: 2026-05-11
updated: 2026-05-11 Mon 23:45
---

# wgetをWindowsで使う

## 概要

`wget` は Linux のコマンドだが、Windows でも Chocolatey を使ってインストールして利用できる。Webページをローカルに保存するのに便利。

## インストール（Chocolatey経由）

### 1. Chocolateyのインストール

PowerShell（管理者）で実行：

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; `
[System.Net.ServicePointManager]::SecurityProtocol = `
[System.Net.ServicePointManager]::SecurityProtocol -bor 3072; `
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### 2. PowerShellを再起動してwgetをインストール

```powershell
choco install wget
```

## PowerShellでの注意点

PowerShell では `wget` が `Invoke-WebRequest` のエイリアスになっているため、そのまま実行すると本物の wget が動かない場合がある。

```powershell
# これは動かない可能性がある
wget --version

# 拡張子付きで実行
wget.exe --version

# またはエイリアスを解除
Remove-Item alias:wget
```

## 基本コマンド

### 1ページを見た目そのまま保存

CSS・画像つきでローカルに保存する：

```bash
wget.exe --page-requisites --convert-links --no-parent --adjust-extension --directory-prefix=wbackup https://example.com/page.html
```

| オプション | 説明 |
|-----------|------|
| `--page-requisites` | ページ表示に必要なファイル（CSS、画像など）をすべて取得 |
| `--convert-links` | リンクをローカルパスに変換 |
| `--no-parent` | 指定URLの親ディレクトリには遡らない |
| `--adjust-extension` | ファイルに適切な拡張子を付与 |
| `--directory-prefix` | 保存先ディレクトリを指定 |

保存先は実行ディレクトリ配下の `wbackup` フォルダ。

### 保存先をカスタム指定

デスクトップに保存する場合：

```bash
wget.exe ... --directory-prefix="$env:USERPROFILE\Desktop\my_backup"
```

## バッチファイル化で簡単操作

```bat
@echo off
set /p target_url=保存したいURL:
set /p save_dir=保存先フォルダ名:

wget.exe --page-requisites --convert-links --no-parent --adjust-extension --directory-prefix="%save_dir%" "%target_url%"

echo 完了しました：%save_dir%
pause
```

ダブルクリックで実行可能。コマンドを覚えなくてもよい。

引用元: [wgetでホームページをそのまま残す：Windows環境での使い方メモ](https://zenn.dev/hydrangea01/articles/943a94869919a1)
