---
tags:
  - article
  - 競技プログラミング
  - BFS
  - 動的計画法
created: 2026-03-11
updated: 2026-03-11 Wed 23:36
source: https://qiita.com/drken/items/0c7bab0384438f285f93
---

## 概要

[[01-BFS|BFS（幅優先探索）]]で最短距離を求めた後、**経路そのもの**を復元する方法。

[[動的計画法の最適解復元]]の方法 2（伝播元メモ方式）を適用する。

## 問題例: 迷路の最短路

```text
8 8
.#....#G
.#.#....
...#.##.
# .##...#
...###.#
.#.....#
...#.#..
S.......
```

'S' から 'G' へ至る最短手数と、その具体的な経路を求める。

![迷路BFS探索の様子](https://qiita-image-store.s3.amazonaws.com/0/182963/a80102a4-8576-3ddb-16cf-289d150275cb.jpeg)

出典: [意外と解説がない！動的計画法で得た最適解を「復元」する一般的な方法](https://qiita.com/drken/items/0c7bab0384438f285f93)

BFS で各マスへの最短手数を求めると、この例では 'G' まで 16 手。

## アルゴリズム

### キーアイデア

BFS でテーブルを更新する際に、**どのマスから伝播してきたか**を記録する。

```cpp
vector<vector<int>> prev_x(height, vector<int>(width, -1));
vector<vector<int>> prev_y(height, vector<int>(width, -1));
```

テーブル更新時に 2 行追加するだけ:

```cpp
if (dist[next_x][next_y] == -1) {
    que.push(make_pair(next_x, next_y));
    dist[next_x][next_y] = dist[x][y] + 1;
    prev_x[next_x][next_y] = x;  // 伝播元の縦座標をメモ
    prev_y[next_x][next_y] = y;  // 伝播元の横座標をメモ
}
```

### 経路復元

ゴールから `prev` 配列を逆に辿る:

```cpp
int x = gx, y = gy;
while (x != -1 && y != -1) {
    field[x][y] = 'o';  // 通過したことを示す
    int px = prev_x[x][y];
    int py = prev_y[x][y];
    x = px, y = py;
}
```

![経路復元の矢印テーブル](https://qiita-image-store.s3.amazonaws.com/0/182963/a30f0802-d258-db99-f6cf-655967d49521.jpeg)

出典: [意外と解説がない！動的計画法で得た最適解を「復元」する一般的な方法](https://qiita.com/drken/items/0c7bab0384438f285f93)

## 完全な実装 (C++)

```cpp
#include <iostream>
#include <queue>
#include <vector>
#include <string>
#include <iomanip>
using namespace std;

const int dx[4] = { 1, 0, -1, 0 };
const int dy[4] = { 0, 1, 0, -1 };

int main() {
    int height, width;
    cin >> height >> width;

    vector<string> field(height);
    for (int h = 0; h < height; ++h) cin >> field[h];

    int sx, sy, gx, gy;
    for (int h = 0; h < height; ++h) {
        for (int w = 0; w < width; ++w) {
            if (field[h][w] == 'S') { sx = h; sy = w; }
            if (field[h][w] == 'G') { gx = h; gy = w; }
        }
    }

    // 最短距離テーブル
    vector<vector<int>> dist(height, vector<int>(width, -1));
    dist[sx][sy] = 0;

    // 経路復元用テーブル
    vector<vector<int>> prev_x(height, vector<int>(width, -1));
    vector<vector<int>> prev_y(height, vector<int>(width, -1));

    queue<pair<int, int>> que;
    que.push({sx, sy});

    while (!que.empty()) {
        auto [x, y] = que.front();
        que.pop();

        for (int d = 0; d < 4; ++d) {
            int nx = x + dx[d], ny = y + dy[d];
            if (nx < 0 || nx >= height || ny < 0 || ny >= width) continue;
            if (field[nx][ny] == '#') continue;

            if (dist[nx][ny] == -1) {
                que.push({nx, ny});
                dist[nx][ny] = dist[x][y] + 1;
                prev_x[nx][ny] = x;  // 伝播元をメモ
                prev_y[nx][ny] = y;
            }
        }
    }

    // 最短距離を出力
    for (int h = 0; h < height; ++h) {
        for (int w = 0; w < width; ++w) {
            if (field[h][w] != '.' && field[h][w] != 'G')
                cout << setw(3) << field[h][w];
            else
                cout << setw(3) << dist[h][w];
        }
        cout << "\n";
    }

    // 経路復元
    int x = gx, y = gy;
    while (x != -1 && y != -1) {
        field[x][y] = 'o';
        int px = prev_x[x][y];
        int py = prev_y[x][y];
        x = px; y = py;
    }
    for (int h = 0; h < height; ++h) {
        for (int w = 0; w < width; ++w) cout << setw(3) << field[h][w];
        cout << "\n";
    }
}
```

## 出力例

```text
  9  #  9 10 11 12  # 16
  8  #  8  # 12 13 14 15
  7  6  7  # 13  #  # 16
  #  5  #  # 12 11 10  #
  3  4  5  #  #  #  9  #
  2  #  4  5  6  7  8  #
  1  2  3  #  5  #  7  8
  S  1  2  3  4  5  6  7

  .  #  o  o  o  .  #  o
  .  #  o  #  o  o  o  o
  .  o  o  #  .  #  #  .
  #  o  #  #  .  .  .  #
  o  o  .  #  #  #  .  #
  o  #  .  .  .  .  .  #
  o  .  .  #  .  #  .  .
  o  .  .  .  .  .  .  .
```

引用元: [意外と解説がない！動的計画法で得た最適解を「復元」する一般的な方法](https://qiita.com/drken/items/0c7bab0384438f285f93)
