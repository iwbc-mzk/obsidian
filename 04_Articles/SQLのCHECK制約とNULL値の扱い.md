---
slug: d92f3b08-7647-4f3c-9c51-f33276f7a471
tags:
  - article
  - SQL
  - データベース
  - CHECK制約
created: 2026-08-09
updated: 2026-08-09 Sun 10:44
---

# SQLのCHECK制約とNULL値の扱い

[[SQLのCHECK制約の基礎と書き方|CHECK制約]]は「FALSE（偽）」と評価された場合にのみデータを拒否する。この評価ルールにより、NULL値の扱いには落とし穴がある。

## NULLは制約をパスする

NULLを含む比較式は、多くの場合「UNKNOWN（不明）」と評価される。CHECK制約は条件式がFALSEの場合のみ違反とみなすため、**UNKNOWNと評価される場合は制約違反とみなされず、そのまま保存が許可される**。

つまり、CHECK制約だけではNULLの混入を防ぐことはできない。NULLも禁止したい場合は、**NOT NULL制約**を併用するのが一般的。

```sql
-- price が NULL の場合、この CHECK 制約は違反とならず保存できてしまう
ALTER TABLE products ADD CONSTRAINT ck_price_positive CHECK (price >= 0);

-- NULL も防ぎたい場合は NOT NULL を併用する
ALTER TABLE products ALTER COLUMN price SET NOT NULL;
```

## ALTER TABLEで追加した場合の既存レコードへの影響

`ALTER TABLE`でCHECK制約を追加すると、データベースは通常、**既存のすべてのレコードがその条件を満たしているか**を検証する。

- 条件に違反するレコードが1つでも存在する場合、エラーが発生して制約の追加自体が失敗する
- 対策として、制約を適用する前に既存データを修正して条件を満たすようにしておく必要がある
- 一方、既存レコードにNULLが含まれている場合は、それが「偽」と判定されない限りエラーにならず、そのまま制約を追加できる

## 関連

- [[SQLのCHECK制約の基礎と書き方]]
- [[SQLのCHECK制約における主要DBの実装差異]]

引用元: NotebookLM
