## 概要

$P$ と互いに素である整数 $A$ に対して

$$
A \times N = 1\quad (\textrm{mod} \quad P)
$$

となるような 1 以上 $P$ 未満の整数 $N$ が必ず存在する。  
このような $N$ ことを __mod $M$ での $A$ の mod 逆元__ といい下記のように表す。

$$
A^{-1}\quad (\textrm{mod} \quad P)
$$

## 求め方

$P$ と互いに素である整数 $A$ に対して、下記のような 1 次方程式を考える。

$$
Ax + Py = 1
$$

この時両辺の mod $P$ をとると

$$
Ax = 1 \quad (\textrm{mod} \quad P)
$$

したがって 1 次方程式 $Ax+Py=1$ の解 $x$ が __A の逆元__ になることがわかる。 $A, P$ は $\textrm{gcd}(A, P) = 1$ (互いに素) であるのでこの 1 次方程式は [[拡張ユークリッドの互除法]] を用いて求めることができる。

```Python
# ax + by = gcd(a, b) = d となる d, x, yを返す
def extGCD(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return (a, 1, 0)

    # a = qb + r => rx + b(qx + y) = d
    q, r = a // b, a % b
    d, y, x = extGCD(b, r)
    y -= q * x

    return (d, x, y)

# mod 61における25の逆元は22
extGCD(25, 61)[1] # 22
```
