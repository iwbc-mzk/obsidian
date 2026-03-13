---
slug: 12c2cb77-1a21-4860-a297-46f0a584241c
tags:
  - Python
  - IT
created: 2025-01-25 Sat 20:54
updated: 2026-03-13 Fri 14:05
---

## 概要

#### ord()

1 文字の Unicode 文字列を表す文字列に対して、その文字の Unicode コードポイントを表す整数を返す。chr() の逆。  
例) ord("a") => 97

#### chr()

Unicode コードポイントが整数 i である文字を表す文字列を返す。ord() の逆。  
例) chr(97) => "a"

## 利用例

ord() と chr() をうまく利用すればアルファベットの列挙等を簡単に行える。

```Python
alphabet = ""
for i in range(26):
	alphabet += chr(ord("a") + i)

print(alphabet)  # => abcdefghijklmnopqrstuvwxyz
```
