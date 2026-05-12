---
tags:
  - article
  - Git
aliases: []
slug: d6e1f5a4-a7b8-9c03-1234-5e6f7a8b9c04
created: 2026-05-11
updated: 2026-05-11 Mon 23:43
---

# Git Worktreeの基本コマンドと使い方

## Git Worktreeとは

1つのリポジトリに対して**複数の作業ディレクトリ（working tree）**を持てる Git の機能。それぞれのディレクトリが独立したブランチを持つため、ブランチを切り替えずに複数ブランチを同時に作業できる。

従来は別ブランチで作業するために `git stash` や `git switch` が必要だったが、worktree を使えばディレクトリごとブランチを分離できる。

## 基本コマンド

### worktree の作成

```bash
# 1. 新しいブランチを自動作成して作業開始（フォルダ名 = ブランチ名）
git worktree add ../feature-name

# 2. 既存のブランチで作業開始
git worktree add ../work-folder existing-branch

# 3. ブランチ名を明示的に指定して作成
git worktree add -b new-branch-name ../folder-name

# 4. 特定のブランチから新しいブランチを作成
git worktree add -b new-branch ../folder-name main

# 5. 実験用の一時的な環境（ブランチに紐付かない）
git worktree add --detach ../experiment
```

### worktree の確認

```bash
# 一覧表示
git worktree list

# 出力例
# /path/to/main-project        abc1234 [main]
# /path/to/feature-work        def5678 [feature/new-feature]
# /path/to/experiment          abc1234 (detached HEAD)

# 詳細情報付きで表示
git worktree list --verbose
```

### worktree の削除

```bash
# 通常の削除（未保存の変更がある場合は拒否）
git worktree remove ../folder-name

# 強制削除（未保存の変更があっても削除）
git worktree remove --force ../folder-name
```

### メンテナンス

```bash
# 手動削除されたworktreeの管理ファイルをクリーンアップ
git worktree prune
```

定期的に実行するとよい。

## 高度な機能

### worktree のロック

ポータブルデバイスやネットワーク共有上のworktreeが一時的に利用不可の場合、管理ファイルが自動削除されるのを防ぐ。

```bash
git worktree lock --reason "USBドライブ上のため一時的に利用不可" ../portable-work
```

### worktree の修復

手動でworktreeを移動した場合、接続が切れることがある。

```bash
git worktree repair ../moved-worktree
```

## 注意事項

| 制限事項 | 内容 |
|----------|------|
| 同じブランチの重複チェックアウト | 通常は不可（`--force` で回避可能だが非推奨） |
| サブモジュールの制限 | スーパープロジェクトでの複数チェックアウトは非推奨 |
| メインworktreeの削除 | 不可 |
| `.git` ディレクトリ内への保存 | Gitが内部構造と混同して削除することがある（非推奨） |

## ベストプラクティス

1. `git worktree prune` で定期的にクリーンアップ
2. worktreeのパス名は用途がわかりやすいものにする
3. 一時的に利用不可のworktreeは `lock` で保護
4. `--force` オプションは必要最小限に留める
5. 保存先は**兄弟ディレクトリ**（プロジェクトと同じ親ディレクトリ配下）が推奨

## Gitエイリアスの設定（効率化）

```ini
# ~/.gitconfig に追加
[alias]
    # worktree追加（ブランチ名だけ指定）
    wta = "!f() { \
        branch=\"$1\"; \
        safe_branch=$(echo \"$branch\" | sed 's/\\//-/g'); \
        path=\"../$safe_branch\"; \
        if git show-ref --verify --quiet \"refs/heads/$branch\"; then \
            git worktree add \"$path\" \"$branch\"; \
        else \
            git worktree add -b \"$branch\" \"$path\"; \
        fi; \
    }; f"

    # ブランチ名で削除
    wtr = "!f() { \
        branch=\"$1\"; \
        worktree_path=$(git worktree list --porcelain | grep -B2 \"branch refs/heads/$branch\" | grep \"worktree\" | cut -d' ' -f2); \
        if [ -n \"$worktree_path\" ]; then \
            git worktree remove ${2:+--force} \"$worktree_path\"; \
        fi; \
    }; f"

    # 一覧表示
    wtl = worktree list
```

使い方：

```bash
git wta feature-x      # 新規または既存ブランチのworktree作成
git wtl                # 一覧
git wtr feature-x      # 削除
```

## 関連記事

- [[Git Worktreeを活用した並列開発パターン]]
- [[Claude CodeスキルによるGit Worktree運用自動化]]

引用元: [Git Worktreeをわかりやすく解説](https://zenn.dev/hiraoku/articles/56f4f9ffc6d186)
