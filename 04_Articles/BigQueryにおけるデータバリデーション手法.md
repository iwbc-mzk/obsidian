---
slug: a2d61b4b-56a7-41c0-9acd-fa5b6cd73221
tags:
  - article
  - SQL
  - BigQuery
  - データベース
  - CHECK制約
  - dbt
created: 2026-08-09
updated: 2026-08-09 Sun 10:44
---

# BigQueryにおけるデータバリデーション手法

BigQueryでは標準的な[[SQLのCHECK制約の基礎と書き方|CHECK制約]]は**サポートされていない**。

## 制約の強制力

BigQueryでは主キー（Primary Key）や外部キー（Foreign Key）を定義できるが、これらは**「強制されない（Not Enforced）」**状態。データの整合性を守るためではなく、クエリの最適化（Joinの省略など）のために使われる。

唯一データベースレベルで強制できるのは、カラムのモードを`REQUIRED`に設定することによる**NOT NULL制約**のみ。

```sql
CREATE TABLE mydataset.products (
    product_id INT64 NOT NULL, -- REQUIRED モードになり、NULL を防ぐ
    price FLOAT64
);
```

## 代替となるデータバリデーション手法

### 1. ERROR関数による手動チェック

SQLクエリ内で特定の条件（例：価格がマイナス）を満たした場合に、意図的にエラーを発生させて処理を止める方法。このクエリをスケジュール設定しておけば、異常検知時に通知を飛ばすことも可能。

```sql
SELECT
    IF(price < 0, ERROR("価格は0以上である必要があります"), price) AS price
FROM `your_project.dataset.table`
```

### 2. dbtによるテスト（Singular Test）

dbtを使用している場合、`tests/`ディレクトリにSQLファイルを作成する。このクエリが**1行でも結果を返すと「失敗」**と判定される。

```sql
-- tests/assert_no_negative_price.sql
SELECT
    order_id,
    price
FROM {{ ref('orders') }}
WHERE price < 0
```

### 3. Data Validation Tool（DVT）の活用

Googleが提供するオープンソースのCLIツール。テーブル間の行数一致や、特定カラムの集計値が正しいかなどを自動で検証できる。

```bash
# テーブル間の行数やカラムの一致を検証するコマンド例
data-validation run \
  --type Column \
  --source-conn $SOURCE_CONN --target-conn $BQ_CONN \
  --tables-list source_db.table=bq_dataset.table
```

## 関連

- [[SQLのCHECK制約の基礎と書き方]]
- [[SQLのCHECK制約における主要DBの実装差異]]

引用元: NotebookLM
