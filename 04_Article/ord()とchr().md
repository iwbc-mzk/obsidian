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
