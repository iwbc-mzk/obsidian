---
tags:
  - article
  - Python
  - Windows
aliases: []
slug: a9b4c8d7-d0e1-2f36-4567-8b9c0d1e2f37
created: 2026-05-11
updated: 2026-05-11 Mon 23:44
---

# WindowsでPythonコマンドがMicrosoft Storeを開く問題の解決方法

## 問題

PowerShell やコマンドプロンプトで `python` コマンドを実行すると Python が実行されず、Microsoft Store が開いてしまう。

## 原因

`python.exe` が2箇所に存在し、Microsoft Store 版が優先されてしまうため。

```
C:\Users\<ユーザー名>\AppData\Local\Programs\Python\Python312\python.exe  ← 本物
C:\Users\<ユーザー名>\AppData\Local\Microsoft\WindowsApps\python.exe      ← スタブ（Store へのリンク）
```

環境変数 Path の順序で本物が上にあっても、Windows Apps の方が優先されることがある。

## 解決方法

### 方法1：Microsoft Store版のPythonショートカットを削除（推奨）

管理者権限のコマンドプロンプトで実行：

```cmd
del C:\Users\<ユーザー名>\AppData\Local\Microsoft\WindowsApps\python.exe
del C:\Users\<ユーザー名>\AppData\Local\Microsoft\WindowsApps\python3.exe
```

削除できない場合は、ファイルの所有権と権限を変更する：

1. `C:\Users\<ユーザー名>\AppData\Local\Microsoft\WindowsApps` に移動
2. `python.exe` を右クリック → プロパティ → セキュリティ → 詳細設定
3. 所有者を自分のアカウントに変更
4. フルコントロールのアクセス許可を付与
5. ファイルを削除

### 方法2：環境変数 Path の順序を確認

1. システムの環境変数 → ユーザー環境変数 → Path
2. 以下のパスが含まれているか確認：
   - `C:\Users\<ユーザー名>\AppData\Local\Programs\Python\PythonXX\`
   - `C:\Users\<ユーザー名>\AppData\Local\Programs\Python\PythonXX\Scripts\`
3. 含まれていない場合は「新規」で追加

## 動作確認

```cmd
> python --version
Python 3.12.4
```

正しいバージョンが表示されれば解決。

引用元: [【備忘録】WindowsでPythonコマンドを実行するとMicrosoft Storeを開く問題の解決方法](https://qiita.com/itsutose/items/ec84158ec29dc4882087)
