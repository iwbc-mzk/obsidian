---
tags:
  - article
  - Obsidian
source: https://qiita.com/saka-guti/items/547f46708e0213212879
created: 2026-02-28 Sat 12:14
updated: 2026-02-28 Sat 12:17
---

# ObsidianのTerminalプラグインでWindowsで別ウィンドウが開く問題の解決策

## 問題

Windows環境でObsidianのコミュニティプラグイン「Terminal」を使うと、ターミナルを開くたびに**別ウィンドウ**でターミナルが起動してしまう。そちらを閉じるとObsidian内のターミナルも固まる。

## 原因

ObsidianがWindows環境でターミナルプロセスをうまく管理できないため。Pythonとライブラリを経由させることでプロセスを直接制御させる。

## 前提条件

- Python 3.10以降がインストール済み
- `python` および `pip3` コマンドが使用可能

```bash
# バージョン確認
python --version
# => Python 3.10.x のように表示されればOK
```

## 解決手順

### ステップ1: 必須ライブラリのインストール

```bash
pip3 install psutil==5.9.5 pywinctl==0.0.50 typing_extensions==4.7.1
```

`Successfully installed ...` のようなメッセージが表示されれば成功。

### ステップ2: ObsidianのTerminalプラグイン設定

1. Obsidianの `設定` を開く
2. `コミュニティプラグイン` → `Terminal` → `Profiles` 横の**メニューアイコン**をクリック
3. `win32IntegratedDefault` 横の**編集アイコン**をクリック
   - **Integrated** を選択（Externalは外部ウィンドウで開くため非推奨）
4. `Python executable` にPythonの実行ファイルパスを入力
   - PATHに登録済みなら `python` のみで動作する場合あり
   - うまくいかない場合は `where python` コマンドでフルパスを確認

```bash
# フルパスの確認
where python
```

5. Checkアイコンをクリックして検証（右上ポップアップにエラーが出なければ成功）
6. ダイアログを閉じてTerminalを開き、設定したターミナルを選択

## 結果

ターミナルがObsidian内部で開き、外部ウィンドウが表示されなくなる。
