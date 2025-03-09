---
created: 2025-01-25 Sat 20:54
updated: 2025-03-09 Sun 17:39
---
## 概要

2 項係数 ${}_nC_{k}$ を素数 $P$ で割った余りを単純に計算する場合、$\frac{n!}{k!(n - k)!}$ を計算した後に $P$ で割って余りを求めることになるが、$n$ の値によっては非常に大きな値を扱うことになる上、1 つの 2 項係数を求めるのに計算量 $O(n)$ かかることになる。  
2 項係数を高速に求めるアルゴリズムは複数あるが、$n, k$ のサイズや $P$ が素数かどうかによって最適なアルゴリズムが異なる。

## アルゴリズム

### $k \leq n \leq 10^7$ で $P$ が素数の時

前処理を行い、その結果を利用して高速に 2 項係数を求める方法。  
$i$ の階乗を P で割った余りを $\textrm{fact}[i]$、その逆元を $\textrm{fact\_inv}[i]$、$i$ の逆元を $\textrm{inv}[i]$ としたときに以下のように計算する。

- 前処理
	- $i$ が 0 から $n$ まで $\textrm{fact}[i], \textrm{fact\_inv}[i], \textrm{inv}[i]$ を計算して結果を保存しておく (メモ化・動的計画法)
- クエリ
	- ${}_nC_k$ を素数 $P$ で割った余りを下記で求める  
	  ${}_nC_k=\textrm{fact}[n]\times\textrm{fact\_inv}[k]\times\textrm{fact\_inv}[n - k] \quad(\textrm{mod} P)$

階乗の逆元については以下のように求められる。  
※ $[\frac{P}{i+1}]$ は P を i+1 で割った数の小数点以下を切り捨てた数

- $\textrm{inv}[i+1]$:
	- $(i+1)^{-1} \equiv -(P\%(i+1))^{-1} \times [\frac{P}{i+1}] \quad (\textrm{mod}P)$
- $\textrm{fact\_inv}[i+1]$:
	- $((i+1)!)^{-1} \equiv (i!)^{-1} \times (i + 1)^{-1} \quad (\textrm{mod}P)$

求め方は [参考リンク](https://algo-logic.info/combination/#) を参照

#### 計算量

- 前処理: $O(n)$
- クエリ: $O(1)$

ただし、$n$ が非常に大きい場合などは階乗と逆元を保存するためのメモリが不足する可能性がある。

#### 実装例

```Python
fact = [1, 1]
fact_inv = [1, 1]
inv = [None, 1]
P = 113

for i in range(2, 11):
    fact.append(fact[i - 1] * i % P)
    inv.append(P - inv[P % i] * (P // i) % P)
    fact_inv.append(fact_inv[i - 1] * inv[i] % P)

# [1, 1, 2, 6, 24, 7, 42, 68, 92, 37, 31]
print(fact)

# [1, 1, 57, 19, 33, 97, 35, 5, 43, 55, 62]
print(fact_inv)

# [None, 1, 57, 38, 85, 68, 19, 97, 99, 88, 34]
print(inv)

# 10C3
n = 10
k = 3
print(fact[n] * fact_inv[k] * fact_inv[n - k] % P)  # 7
```

## 参考

- [競プロでよく使う二項係数(nCk)を素数(p)で割った余りの計算と逆元のまとめ | アルゴリズムロジック](https://algo-logic.info/combination/#)
