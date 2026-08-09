---
slug: 47e3240b-f6da-4b12-b9e5-269ed6608a84
tags:
  - article
  - SQL
  - データベース
  - CHECK制約
created: 2026-08-09
updated: 2026-08-09 Sun 10:44
---

# SQLのCHECK制約の基礎と書き方

**CHECK制約**は、データの追加・更新時にその内容が特定の条件を満たしているかを検証し、不適切なデータが保存されるのを防ぐSQLの制約。

## 役割とメリット

- **データの整合性と正確性の維持**：データベースレベルでルールを強制するため、アプリケーション側のチェック漏れや一括登録時でもデータの品質を保てる
- **詳細な制限**：単なるデータ型（数値など）の制限だけでなく、「価格は0以上」や「年齢は18歳以上」といった具体的な条件を自由に設定できる
- **システムの信頼性向上**：誤ったデータによるシステムの誤動作を未然に防ぐことができる

## 書き方

大きく分けて2つの設定方法がある。

### 1. テーブル作成時に設定する

- **列制約**：カラムごとに、そのカラムの定義に続けて記述する
- **表制約**：特定のカラムの定義とは別に、複数のカラムを組み合わせて記述する

```sql
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    price      NUMERIC CHECK (price >= 0),          -- 列制約
    stock      INT,
    CONSTRAINT ck_stock_range CHECK (stock BETWEEN 0 AND 9999)  -- 表制約
);
```

### 2. 既存のテーブルに追加する

`ALTER TABLE`を使って後から制約を追加できる。

```sql
ALTER TABLE products ADD CONSTRAINT ck_price_positive CHECK (price >= 0);
```

制約に名前（`ck_price_positive`など）をつけておくと、後で削除する際に管理しやすい。

## よく使われる条件式の例

- **範囲指定**：`CHECK (score BETWEEN 0 AND 100)`
- **特定の値のみ許可**：`CHECK (gender IN ('M', 'F'))`
- **複数の条件を組み合わせ**：`CHECK (age >= 18 AND status = 'active')`

## 関連

- [[SQLのCHECK制約とNULL値の扱い]]
- [[SQLのCHECK制約における主要DBの実装差異]]
- [[BigQueryにおけるデータバリデーション手法]]

引用元: NotebookLM
