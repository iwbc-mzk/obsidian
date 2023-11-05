## 概要

確率 $p(p\neq 0)$ で成功する試行を成功するまでに行う時の試行回数 (最後の成功した回を含む) の**期待値は $\frac{1}{p}$ になる**

## 証明

求める期待値を $X$ とする。1 回試行した時、成功時はそこで終了、失敗した時は全く同じ状況でやり直しとなる。したがって下記のような等式が成り立つ。

$$
X = 1 + (1 - p)X
$$

これを変形すると $X=\frac{1}{p}$ となる。

## 参考

- [解説 - AtCoder Beginner Contest 194](https://atcoder.jp/contests/abc194/editorial/823)
- [Journey [AtCoder Beginner Contest 194 D] - はまやんはまやんはまやん](https://blog.hamayanhamayan.com/entry/2021/03/07/000733)
