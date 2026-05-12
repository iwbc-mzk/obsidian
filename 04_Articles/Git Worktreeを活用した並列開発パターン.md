---
tags:
  - article
  - Git
aliases: []
slug: e7f2a6b5-b8c9-0d14-2345-6f7a8b9c0d15
created: 2026-05-11
updated: 2026-05-11 Mon 23:44
---

# Git Worktreeを活用した並列開発パターン

[[Git Worktreeの基本コマンドと使い方]] の応用編。実際の開発シナリオでの活用パターンを紹介する。

## パターン1：緊急修正への対応

リファクタリング作業中に緊急の修正依頼が来た場合。

**問題点（従来の方法）:**
作業ツリーが複雑な状態（新規ファイル、移動ファイル、削除ファイルが混在）だと、`git stash` で何かを壊すリスクがある。

**Git Worktreeを使った解決:**

```bash
# 1. 現在の作業はそのまま
# 2. 緊急修正用のworktreeを作成
git worktree add -b hotfix/critical-bug ../emergency main

# 3. emergency フォルダに移動して修正
cd ../emergency
# ... 修正作業 ...

# 4. コミット・マージ後にworktreeを削除
git worktree remove ../emergency

# 5. 元のフォルダで即座にリファクタリング再開
```

**メリット:** 元の作業ディレクトリに一切影響を与えずに緊急対応できる。

## パターン2：複数機能の並行開発

```
# ユーザー認証システム用のworktree
git worktree add ../auth-system feature/user-authentication

# 商品検索機能用のworktree
git worktree add ../search-feature feature/product-search
```

3つの独立した作業環境が手に入る：
- メインディレクトリ：小さな修正や緊急対応
- `../auth-system`：認証機能開発
- `../search-feature`：検索機能開発

それぞれで独立してコミットでき、同時にテストを走らせることも可能。

## パターン3：バージョン比較とデバッグ

「前のバージョンでは動いていたのに、最新版で動かなくなった」の調査。

```bash
# 過去の安定版
git worktree add ../stable-version v2.1.0

# 問題が発生したバージョン
git worktree add ../problem-version v2.2.0
```

3つの異なるバージョンのコードを同時に開き、並べて比較できる。

## AI エージェントとの組み合わせ

Claude Code などの AI エージェントで複数 Issue を並列処理する場合にも有効。

```
1. GitHub Issueを取得
2. git worktreeでworktreeを作成（Issue単位）
3. Issueの内容に基づいて実装
4. Pull requestを作成
5. worktreeをクリーンアップ
```

Issue 1つにつき worktree が1つ作られ、それぞれが独立したディレクトリで動くためコンフリクトなく並列実行できる。

詳細は [[Claude CodeスキルによるGit Worktree運用自動化]] を参照。

引用元: [Git Worktreeをわかりやすく解説](https://zenn.dev/hiraoku/articles/56f4f9ffc6d186)
