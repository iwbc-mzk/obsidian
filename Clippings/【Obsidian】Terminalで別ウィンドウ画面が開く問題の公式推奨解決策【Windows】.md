---
title: 【Obsidian】Terminalで別ウィンドウ画面が開く問題の公式推奨解決策【Windows】
source: https://qiita.com/saka-guti/items/547f46708e0213212879
author:
  - "[[saka-guti]]"
published: 2025-07-18
created: 2026-02-28
description: はじめに Obsidianのコミュニティプラグイン「Terminal」は、Obsidian内で直接コマンドを実行できる非常に便利なツールです。しかし、Windows環境で利用すると、ターミナルを開くたびに別ウィンドウでターミナルが起動してしまい、そちらを閉じるとObsid...
tags:
  - clippings
updated: 2026-02-28 Sat 11:20
---
![](https://relay-dsp.ad-m.asia/dmp/sync/bizmatrix?pid=c3ed207b574cf11376&d=x18o8hduaj&uid=588130)

[@saka-guti](https://qiita.com/saka-guti)

8

投稿日

## はじめに

Obsidianのコミュニティプラグイン「Terminal」は、Obsidian内で直接コマンドを実行できる非常に便利なツールです。しかし、Windows環境で利用すると、ターミナルを開くたびに **別ウィンドウでターミナルが起動してしまい、そちらを閉じるとObsidian内のターミナルも固まってしまう** という厄介な問題がありました。

今回は、この問題を解決するためにプラグイン開発者が推奨している、 **Pythonを使ったスマートな公式解決策** をご紹介します。

## 対象読者

- WindowsでObsidianを利用している方
- Terminalプラグインで別ウィンドウ問題に悩まされている方
- 標準のPowerShellやコマンドプロンプトを使い続けたい方

## 前提条件

この記事では、お使いのPCで以下の準備が完了していることを前提としています。

- Obsidianがインストール済みであること
- コミュニティプラグイン「Terminal」がインストール済みであること
- **Python 3.10以降** がインストール済みで、コマンドプロンプトやPowerShellから `python` および `pip3` コマンドが利用できること

コマンドプロンプトやPowerShellを開き、以下のコマンドを実行してください。

cmd

```bash
python --version
```

`Python 3.10.x` のようにバージョンが表示されればOKです。

## 問題の原因と解決策

この問題は、Obsidianがターミナルのプロセスをうまく管理できないために発生します。そこで、Pythonとそのライブラリの力を借りて、Obsidianにターミナルプロセスを直接制御させることで、別ウィンドウの起動を防ぎます。

手順は以下の2ステップです。

1. 指定されたPythonライブラリをインストールする
2. ObsidianのTerminalプラグイン設定でPythonのパスを構成する

## ステップ1：必須ライブラリのインストール

まず、プラグインがターミナルを制御するために必要なPythonライブラリをインストールします。

コマンドプロンプトやPowerShellで、以下のコマンドをコピーして実行してください。開発者が指定するバージョンを正確にインストールします。

cmd

```bash
pip3 install psutil==5.9.5 pywinctl==0.0.50 typing_extensions==4.7.1
```

`Successfully installed ...` のようなメッセージが表示されれば成功です。

## ステップ2：ObsidianのTerminalプラグイン設定

次に、Obsidian側で設定を行います。

1. Obsidianの `設定` を開きます  
	[![setting.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/691672/5733f37e-1d5e-4418-81aa-241b6084e217.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F691672%2F5733f37e-1d5e-4418-81aa-241b6084e217.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=a2034840ebe85df77cc6eedbbf4337e5)
2. `コミュニティプラグイン` の `Terminal` 内の `Profiles` 横の **メニューアイコン** をクリックします  
	[![terminal.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/691672/73da7b1c-62ad-44d6-beb0-c017992ec705.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F691672%2F73da7b1c-62ad-44d6-beb0-c017992ec705.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=d7698540646acb75b2395f272273f920)
3. `win32IntegratedDefault` 横の **編集アイコン** をクリックします  
	※ **External** は外部ウィンドウとして開くため、 **Integrated** を選択してください。  
	※ `Prepend(またはAppend)` でPowerShellやBashなどを選択することも可能です。  
	※利用しないターミナルは **削除アイコン「ー」** をクリックして消しておくと後のメニュー表示で探しやすくなります。  
	[![profiles.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/691672/f4d9019a-5105-46cd-8d00-a238d518fede.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F691672%2Ff4d9019a-5105-46cd-8d00-a238d518fede.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=1b0deec865b1dd1b9d55d99b743c02c8)
4. `Python executable` に **Pythonの実行ファイルパス** を入力後、右の **Checkアイコン** をクリックして、右上のポップアップ表示にエラーが出ていなければ成功です  
	[![python.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/691672/bdbe6de9-b8e1-42c0-8bd9-e1397b207b53.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F691672%2Fbdbe6de9-b8e1-42c0-8bd9-e1397b207b53.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=f1061bce08bcdab6b2ea0dd43dba660d)
	- 環境変数(PATH)に登録されていれば、 `python` と入力するだけで動作することがあります  
		※うまくいかない場合は、 `where python` コマンドで表示されるフルパスを入力してください
	- `Name` を入力すると後のメニュー表示で探しやすくなります。
5. 開いたダイアログをすべて閉じて、 `terminal` を開いてください  
	[![open.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/691672/4bad2523-8604-4954-b7c2-2452ba2ccfb3.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F691672%2F4bad2523-8604-4954-b7c2-2452ba2ccfb3.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=fb15be6a9ecf6cec32f331aea01ff286)
6. 先ほど設定したターミナルを選択してください  
	[![select.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/691672/88fa867d-0349-4f13-8613-989cf6e266fe.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F691672%2F88fa867d-0349-4f13-8613-989cf6e266fe.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=90d97af4511b38b028187e2e1dbdd716)
7. ターミナルがObsidian内部で開き、 **外部ウィンドウは表示されない** はずです  
	[![cmd.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/691672/b9c7b8c3-671f-4400-b680-ccc5fafb6927.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F691672%2Fb9c7b8c3-671f-4400-b680-ccc5fafb6927.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=3d2425ca9edaea8890fef628783d62c6)

## まとめ

ObsidianのTerminalプラグインが **Windowsで別ウィンドウを起動してしまう問題** に対し、Pythonを使った公式推奨の解決策を紹介しました。

ぜひお試しいただき、快適なObsidianライフをお送りください！

[2](https://qiita.com/saka-guti/items/#comments)

コメント一覧へ移動

X（Twitter）でシェアする

Facebookでシェアする

はてなブックマークに追加する

[8](https://qiita.com/saka-guti/items/547f46708e0213212879/likers)

いいねしたユーザー一覧へ移動

5