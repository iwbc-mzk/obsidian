---
slug: 84f2474f-71d8-4697-852c-563a07c169c0
tags:
  - article
  - SQL
  - データベース
  - CHECK制約
created: 2026-08-09
updated: 2026-08-09 Sun 10:44
---

# SQLのCHECK制約における主要DBの実装差異

[[SQLのCHECK制約の基礎と書き方|CHECK制約]]は各データベース製品によってサポート状況や制限事項が異なる。

## MySQL

長らく構文はあっても無視されていたが、**バージョン8.0.16（あるいは8.0.15）以降**で全ストレージエンジンにおいて正式にサポートされるようになった。

## SQL Server

制約内で**サブクエリや他のテーブルを参照することができない**。単純な条件式に限定されるため、複雑なロジックが必要な場合はトリガーやビューの利用が検討される。

## Oracle

カラム定義に続けて記述する際、`CONSTRAINT`句を省略できるなど、構文を簡略化して記述することが可能。

```sql
-- Oracle では CONSTRAINT 句を省略した簡略記法が可能
CREATE TABLE products (
    price NUMBER CHECK (price >= 0)
);
```

## PostgreSQL

条件式がNULL（UNKNOWN）と評価された場合も制約をパスする仕様（→ [[SQLのCHECK制約とNULL値の扱い]]）。また、制約内で**CASE式**を使用できるため、複数のカラムが絡む複雑な条件も記述できる。

```sql
-- PostgreSQL: CASE式を使った複雑な条件例
ALTER TABLE orders ADD CONSTRAINT ck_discount_valid CHECK (
    CASE
        WHEN status = 'promo' THEN discount BETWEEN 0 AND 50
        ELSE discount = 0
    END
);
```

## BigQuery

標準のCHECK制約自体がサポートされていない。詳細は[[BigQueryにおけるデータバリデーション手法]]を参照。

## 関連

- [[SQLのCHECK制約の基礎と書き方]]
- [[SQLのCHECK制約とNULL値の扱い]]
- [[BigQueryにおけるデータバリデーション手法]]

引用元: NotebookLM
