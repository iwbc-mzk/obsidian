---
tags:
  - セキュリティ
aliases:
  - JSON Injection
slug: 086a5fe6-9f72-4a88-967a-6328c67e0370
created: 2025-01-25 Sat 20:54
updated: 2026-03-18 Wed 17:36
---
## 概要

script 要素を利用して JSON を読み込むことでブラウザに他サービスが提供する JSON ファイルを読み込ませ、その内容を不正に入手する手法。

```html
<script src="https://api.example.com/v1/users/me" type="application/javascript"></script>
```

読み込んだ JSON が JavaScript として正しい文法になっている場合に発生する。

>[!warning]  
> API の認証手段としてクッキーではなく、リクエストヘッダへ認証情報付与を利用している場合は発生しない
