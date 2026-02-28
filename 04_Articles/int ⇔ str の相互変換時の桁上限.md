---
tags:
  - Python
  - IT
created: 2025-01-25 Sat 20:54
updated: 2026-02-28 Sat 10:56
---

## 概要

桁数の大きい str を int 型に変換しようとした際に下記のようなエラーが発生することがある。

> ValueError: Exceeds the limit (4300) for integer string conversion: value has 16394 digits

これは変換時の __桁数の上限 (4300 桁)__ を超えているために生じている。

```Python
ss = int("2" * 10**4)
print(ss)

"""
Traceback (most recent call last):
  File "C:\github\atcoder\arc\arc154\a\main.py", line 31, in <module>
    ss = int("2" * 10**4)
         ^^^^^^^^^^^^^^^^
ValueError: Exceeds the limit (4300) for integer string conversion: value has 10000 digits
"""
```

## 対応方法

sys モジュールの `set_int_max_str_digits` で上限の桁数を指定できる。  
上限を取り外したい場合は 0 を指定する。

```Python
import sys
sys.set_int_max_str_digits(0)   

ss = int("2" * 10**4)
print(ss)  # ok
```

## 参考

- [Built-in Types — Python 3.11.6 documentation](https://docs.python.org/3/library/stdtypes.html#integer-string-conversion-length-limitation)
- [Python Insider: Python releases 3.10.7, 3.9.14, 3.8.14, and 3.7.14 are now available](https://blog.python.org/2022/09/python-releases-3107-3914-3814-and-3714.html)
- [python - ValueError: Exceeds the limit (4300) for integer string conversion - Stack Overflow](https://stackoverflow.com/questions/73693104/valueerror-exceeds-the-limit-4300-for-integer-string-conversion)
