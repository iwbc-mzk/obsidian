---
title: CalibreでKindleをPDF化する方法 2025
source: https://qiita.com/NanakiOhashi-JP/items/c65d1abcf116288c632d
author:
  - "[[NanakiOhashi-JP]]"
published: 2025-05-14
created: 2025-09-27
description: Calibreを使ってKindleをPDF化する方法 免責事項：この方法はあくまで個人利用のためにPDF化が必要な方のためとなっています。版権元の許可なく第三者に配布・販売する行為は法律で固く禁じられています。またここで紹介する方法はこれらの違法行為を助長することが目的で...
tags:
  - clippings
updated: 2025-09-27 Sat 22:45
---
![](https://relay-dsp.ad-m.asia/dmp/sync/bizmatrix?pid=c3ed207b574cf11376&d=x18o8hduaj&uid=588130)

## Calibreを使ってKindleをPDF化する方法

免責事項：この方法はあくまで個人利用のためにPDF化が必要な方のためとなっています。版権元の許可なく第三者に配布・販売する行為は法律で固く禁じられています。またここで紹介する方法はこれらの違法行為を助長することが目的ではありません。

## １．事前準備

まず必要なプログラムをダウンロードしていきます。

► Calibre: [https://calibre-ebook.com/download](https://calibre-ebook.com/download)

お使いのOSのアイコンからダウンロードしてください。  
自分はWindows環境で行っているので他OSでの動作は保証しかねます。

► KFX inputプラグイン: [https://www.mobileread.com/forums/showthread.php?t=291290](https://www.mobileread.com/forums/showthread.php?t=291290)  
少し分かりづらいですが、サイトを少しスクロールすると

[![スクリーンショット 2025-05-13 234105.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/4008111/6bfe2d3f-fa80-40df-9153-3833f71cef0f.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F4008111%2F6bfe2d3f-fa80-40df-9153-3833f71cef0f.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=5d45c101dcc175bc9e5f00a45c925841)

このような箇所が出てきますので、ここのKFX input.zipをクリックしてダウンロードしてください。

► deDRM プラグイン V10.0.9 (10.1.0 用 RC1)\*:

スクロールして下のAssetsからDeDRM\_tools\_10.0.9.zipをクリックしてダウンロードしてください。

[![スクリーンショット 2025-05-13 235116.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/4008111/84cf8c1c-dc0e-4897-9644-92343c353b4b.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F4008111%2F84cf8c1c-dc0e-4897-9644-92343c353b4b.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=98e82378958abc634310b12f799a1882)

► Kindle for PC バージョン。 2.4.0 (別名 2.4.70904): [https://kindle-for-pc.en.uptodown.com/windows/download/1016990853](https://kindle-for-pc.en.uptodown.com/windows/download/1016990853)

面倒くさいですが、Kindleのバージョンを固定しなければならないのでこのサイトから2.4.0をダウンロードしてください。もしすでにKindleが入っている場合は、一度アンインストールしてください。

► DNSB の disabled\_k4pc\_download.bat： [https://www.mobileread.com/forums/showthread.php?p=4444671#post4444671](https://www.mobileread.com/forums/showthread.php?p=4444671#post4444671)

Kindleの自動アップデートをキャンセルするための実行ファイルです。

[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/4008111/45d7f3bc-458c-4f09-85b6-422d8fddb43d.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F4008111%2F45d7f3bc-458c-4f09-85b6-422d8fddb43d.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=19b31da9b22fd52b8d23193d97f9e8d1)

## 2.環境構築

さて、色々ダウンロードしましたが、まずはCalibreをインストールしましょう。  
言語に縛りはありません、使いやすい言語を使用してください。

次にDeDRM\_tools\_10.0.9を解凍してください。  
⚠ KFX Input.zipは解凍しないでください！

Calibreが無事にインストールできたら、早速Calibreを開きましょう。  
開くとこのような画面が出てくると思います。

[![スクリーンショット 2025-05-13 235931.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/4008111/70c1df02-e7e2-4b14-84d9-ce355b87f122.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F4008111%2F70c1df02-e7e2-4b14-84d9-ce355b87f122.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=43ce3171f863f47e9d01ecd452b8f5b4)

上のツールバーから「環境設定」を開いてください。

[![スクリーンショット 2025-05-14 000003.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/4008111/52375ae3-dfc0-4c8c-a470-e961a026d01e.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F4008111%2F52375ae3-dfc0-4c8c-a470-e961a026d01e.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=5ed345a95543ca76998a36166175ad89)

下の方の「高度な設定」→「プラグイン」を開きましょう。

[![スクリーンショット 2025-05-14 000011.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/4008111/92fe3caf-20a2-4050-9c00-913e76b5086b.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F4008111%2F92fe3caf-20a2-4050-9c00-913e76b5086b.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=86b0ccea3efaf6d468d82e22df71c681)

右下の「ファイルからプラグインを読み込む」を選択し、解凍したフォルダの中の\\DeDRM\_tools\_10.0.9\\DeDRM\_plugin.zipとKFX Input.zipを読み込みましょう。  
２つのプラグインを読み込めたらCalibreを再起動して、再び「プラグイン」を開いて正しく読み込めたか確認しましょう。  
「ユーザーがインストールしたプラグインのみを表示する」にチェックをいれ、DeDRM, KFX Inputが入っていることを確認してください。

[![スクリーンショット 2025-05-14 000115.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/4008111/1370d46e-9b90-49be-8ff4-c761e082d520.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F4008111%2F1370d46e-9b90-49be-8ff4-c761e082d520.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=198a19a8d2a9261f821f1b3b5283bf7b)

Calibreの設定は以上です。

次にKindleをインストールしましょう。

まずは自動アップデートを止めるために、disable\_k4pc\_download.batを実行してください。  
Windowdsだと警告が出るかもしれませんが、「詳細」を押して実行してください。

プログラムが実行したら、ターミナルが起動します。  
ここでターミナルに任意の入力をすれば完了です。

ではKindleのインストーラーを実行してインストールしてください。

インストールが完了したら上のメニューバーから「ツール」→「オプション」を開いてください。  
そうしたら、「更新がある場合は自動的にインストールする」のチェックボックスを外してください。

[![スクリーンショット 2025-05-14 001244.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/4008111/f1a3f332-30e2-492a-837b-20e00a6d3594.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F4008111%2Ff1a3f332-30e2-492a-837b-20e00a6d3594.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=69a38470c9393c75550fcdc987d35184)

その後、お使いのAmazonアカウントでサインインをしてください。  
サインインが完了すると、ホーム画面にKindle Booksが一覧で表示されているはずです。

## 3.変換

PDF化したい本の表紙を右クリックし、ダウンロードしてください。

[![スクリーンショット 2025-05-14 001507.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/4008111/a41710f3-a718-43a2-b490-b64445644d98.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F4008111%2Fa41710f3-a718-43a2-b490-b64445644d98.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=5885366153998d90fddd832d59f4dfd2)

ダウンロードが完了したら、通常では /ドキュメント/My Kindle Content/　にフォルダが追加されているはずです。

※もし見つからなければ「ツール」→「オプション」→「コンテンツ」にパスが書いてありますので、確認してください。  
[![スクリーンショット 2025-05-14 001834.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/4008111/549f69b6-1b83-4b69-9104-325be61a03c4.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F4008111%2F549f69b6-1b83-4b69-9104-325be61a03c4.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=4bce27c033f93ab06bc68ed20eb09a24)

/My Kindle Contentを開くとダウンロードした本の数だけ意味不明なフォルダがあると思います。  
それぞれが１つの本のデータになりますが、どれがどれかファイル名で判断するのは困難なので、Calibreにいれて確認するのが一番手っ取り早いです。  
適当な本が入っているだろうフォルダを開いてください。この様になっているはずです。  
[![スクリーンショット 2025-05-14 002030.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/4008111/02f24512-adfd-457f-bc7f-4e3ab3cbe102.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F4008111%2F02f24512-adfd-457f-bc7f-4e3ab3cbe102.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=159c405c8bd02ffd5c4be51dcd6a50e7)  
.azw 拡張子のファイルがあるはずです。無ければKindleのバージョンを変えてみるか、再度、本をダウンロードし直してみてください。  
この.azw ファイルをCalibreに直接ドラッグ＆ドロップしてください。  
[![スクリーンショット 2025-05-14 002421.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/4008111/4e117151-6f7c-4774-9bcf-54413a53beaa.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F4008111%2F4e117151-6f7c-4774-9bcf-54413a53beaa.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=877082b6290080cd786b98a799adf1a3)  
このように本の表紙が見られれば成功です。

Calibreで変換したい本を選択した後、ツールバーから「本の変換」をクリックしてください。  
[![スクリーンショット 2025-05-14 002548.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/4008111/ee2a9411-0986-477c-9e64-9707b57cd2b4.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F4008111%2Fee2a9411-0986-477c-9e64-9707b57cd2b4.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=080bf562751b8a572cc4fbe3bc98365d)  
このような画面が出てくると思います。  
右上の「出力形式」をクリックするとプルダウンメニューが出てきます。  
変換したい拡張子を選択しましょう。  
細かい設定はここでは省きます。

さて右下の「✓OK」をクリックしたら変換が開始します。  
変換が完了したら、完了した本を選択して「ディスクに保存」で保存先を指定できます。

これでうまく行ったら万歳！変換しまくってPDFライフを楽しみましょう。

うまくいかなかった人がいると思います。僕もそうでした。  
これはKFX（本のファイル）が文字を文字情報ではなく、PDF自体で埋め込んでいるのが原因です。

安心してください。みなさんがインストールしたプラグイン、KFX Inputには対策があります。

また「環境設定」を開きましょう。  
[![スクリーンショット 2025-05-14 000003.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/4008111/5026f765-3251-4089-a250-9859227d1fd4.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F4008111%2F5026f765-3251-4089-a250-9859227d1fd4.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=18aada73b228265e004f18d3b95c0d4d)  
今度は「プラグイン」ではなく、「インタフェース」→「ツールバー＆メニュー」を開きましょう。  
[![スクリーンショット 2025-05-14 003351.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/4008111/2a839004-d1f1-4ad7-8990-06dae027080d.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F4008111%2F2a839004-d1f1-4ad7-8990-06dae027080d.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=ae87147700f2cc8350d4dd7db4904101)  
「カスタマイズするツールバーまたはメニューをクリックして選択」をクリックして「メインツールバー」を開きましょう。  
[![スクリーンショット 2025-05-14 003507.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/4008111/3c9f2852-476f-4f98-9aa3-192f6c08e24c.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F4008111%2F3c9f2852-476f-4f98-9aa3-192f6c08e24c.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=2ebd3a220649b65fa4c39dc424912d5e)  
左の「使用できるアクション」から「From KFX」を探し、ダブルクリックして、右の「現在のアクション」に追加してください。追加できたら右下の「✓適用」を押して、Calibreのホームに戻りましょう。

上のツールバーに「From KFX」が追加されたと思います。  
[![スクリーンショット 2025-05-14 003733.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/4008111/9d49211d-5999-4b15-9b70-f8ba0fac2974.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F4008111%2F9d49211d-5999-4b15-9b70-f8ba0fac2974.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=187ecb2b0a5304c9f27dd0875d4a9f12)

あとは簡単、PDF化したい本を選択して、この「From KFX」をクリックしましょう。  
そうしたら、「EPUB」とか「PDF」とか変換したい形式を選べます。  
「PDF」を選択して、あとはOKを押しましょう。

うまく行ったはずです。  
あとは「ディスクに保存」したら完了です。

最後にPDF化自体は違法ではありません。ただしこれらを第三者に配布ないしは売買する行為は違法行為となります。間違っても個人利用の範囲を超えないよう注意してください。

それでは、お疲れ様でした！

[0](https://qiita.com/NanakiOhashi-JP/items/#comments)

コメント一覧へ移動

X（Twitter）でシェアする

Facebookでシェアする

はてなブックマークに追加する

[12](https://qiita.com/NanakiOhashi-JP/items/c65d1abcf116288c632d/likers)

いいねしたユーザー一覧へ移動

9