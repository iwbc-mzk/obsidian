## 概要

2 進数の値 $x$ に対して

> $x \& (-x)$

を計算すると右側から最初に 1 が立っているアドレスのみを残してほかのビットが 0 で埋まった値が返ってくる。

```Python
print(bin(11&-11), bin(11), bin(-11))  # 0b1 0b1011 -0b1011
print(bin(30&-30), bin(30), bin(-30))  # 0b10 0b11110 -0b11110

a = 5
for _ in range(5):
	print(a, bin(a), bin(a&-a), a&-a)
	a += a & -a
"""
5 0b101 0b1 1
6 0b110 0b10 2
8 0b1000 0b1000 8
16 0b10000 0b10000 16
32 0b100000 0b100000 32
"""
```
