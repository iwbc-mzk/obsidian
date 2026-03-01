---
tags:
  - article
  - IT
  - Markdown
source: https://qiita.com/h1na/items/d305d49b5a27e92d132a
created: 2026-03-01
updated: 2026-03-01 Sun 18:26
---

# Markdownの参照スタイルリンク記法

Markdownでは一般的なインラインリンク記法に加え、**参照スタイルリンク**（Reference-style links）という記法が利用できる。本文中のURLをまとめて管理でき、可読性が向上する。

## 一般的なインラインリンク記法

```md
[タイトル](URL)
```

シンプルで使いやすいが、URLが本文中に大量に含まれる場合や、同じリンクを複数回使う場合に煩雑になる。

## 参照スタイルリンク記法

本文中にはIDを使ってマークし、URLの定義は別の場所（通常は文末）にまとめる記法。

### 基本的な書き方

```md
[タイトル][1]

[1]: https://example.com
```

IDは数値以外の文字列でも使える。一度定義したIDは使い回し可能。

### IDを省略する記法

テキスト自体をIDとして使用できる。

```md
[google][]

[google]: https://www.google.com
```

### title属性を付ける

URLの後にクォートでタイトル（HTMLの `title` 属性）を付けることができる。書き方は3種類。

```md
[foo]: http://example.com/ "Optional Title Here"
[foo]: http://example.com/ 'Optional Title Here'
[foo]: http://example.com/ (Optional Title Here)
```

### 画像への適用

参照スタイルは画像にも使える。

```md
![alt][image]

[image]: https://example.com/image.png "画像タイトル"
```

IDを数値にする書き方も可能。

```md
![がぞー][5]

[5]: https://example.com/image.png "画像タイトル"
```

## メリット

- 本文の可読性が上がる（URLが本文中に埋め込まれない）
- 同じURLを複数箇所で使い回せる
- URLの管理を文末に一元化できる

引用元: [意外と知られてないっぽいMarkdownのリンクの書き方](https://qiita.com/h1na/items/d305d49b5a27e92d132a)
