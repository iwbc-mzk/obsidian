---
tags:
  - article
  - ClaudeCode
  - Git
aliases: []
slug: f8a3b7c6-c9d0-1e25-3456-7a8b9c0d1e26
created: 2026-05-11
updated: 2026-05-11 Mon 23:44
---

# Claude CodeスキルによるGit Worktree運用自動化

[[Git Worktreeの基本コマンドと使い方]] の操作を Claude Code のスキルに閉じ込めることで、チーム全員が簡単に並列開発できるようにする手法。

## 課題：手動でのworktree操作の手間

worktreeを作って作業開始するまでに必要なコマンド群：

```bash
# 1. worktreeを作成してブランチを切る
git worktree add .claude/worktrees/fix-login-bug -b fix/login-bug

# 2. 作成したディレクトリに移動
cd .claude/worktrees/fix-login-bug

# 3. 環境ファイルをコピー
cp ../../.env .
cp ../../.env.local .
cp ../../localhost.pem .
cp ../../localhost-key.pem .
cp ../../.claude/settings.local.json .claude/

# 4. 依存パッケージのインストール
npm install
```

4ステップ・8行以上。さらに作業後のクリーンアップも必要。

チームに導入しようとすると「手順が多くて重い腰が上がらない」という反応が多い。

## 解決策：スキルに閉じ込める

Claude Code のスキル（Markdownファイルでワークフローを定義し、スラッシュコマンドとして呼び出す仕組み）を使う。

```
> /git-worktree feature/add-auth
```

この1行だけで以下が自動実行される：

1. メインリポジトリのパスを記録
2. `EnterWorktree` で worktree を作成
3. セッションの作業ディレクトリを自動切り替え
4. `.env` や SSL 証明書などの設定ファイルをコピー

## Claude Code の EnterWorktree / ExitWorktree ツール

Claude Code が提供する2つのビルトインツール：

| ツール | 機能 |
|--------|------|
| `EnterWorktree` | worktree 作成 + セッションのディレクトリ切り替えを一度に実行 |
| `ExitWorktree` | 元のディレクトリに戻る + worktree を残すか削除するかを選択 |

通常の `git worktree add` では作成後に `cd` で移動する必要があるが、`EnterWorktree` なら Claude Code セッション自体が新しい worktree に切り替わる。

## スキル設計の工夫：責任の分離

プロジェクトごとにセットアップ要件が異なるため、2スキルに分離：

```
worktree作成スキル        環境セットアップスキル
（プロジェクト共通）  +   （プロジェクト固有）
```

セットアップスキルはプロジェクトローカルでオーバーライド可能：

```
# プロジェクト固有のセットアップスクリプトがあれば優先
.claude/skills/setup-worktree/setup-worktree.sh  ← プロジェクト固有

# なければプラグインのデフォルトを使う
~/.claude/plugins/.../setup-worktree.sh           ← デフォルト
```

**変わる部分と変わらない部分を分離**することで、各プロジェクトは必要なセットアップだけカスタマイズできる。

## 他のスキルとの連携

エージェントが GitHub Issue を読み取って PR を作成するワークフローとの組み合わせ：

```
1. GitHub Issueを取得
2. git-worktreeスキルでworktreeを作成（ここで活用）
3. Issueの内容に基づいて実装
4. Pull requestを作成
5. worktreeをクリーンアップ
```

複数 Issue を並列処理する場合、Issue 1つにつき worktree が1つ作られ、それぞれが独立したディレクトリで動くためコンフリクトなく並列実行できる。

git-worktree スキルを単体で作っておいたことで、エージェントは「worktreeの作り方」を知らなくても並列開発を実現できる。

## 「複雑さはスキルに閉じ込める」という考え方

- Git worktreeの複雑さは柔軟性の裏返し。排除するのではなく、**露出させないこと**が重要
- スキルに閉じ込める候補：プロジェクト固有のデプロイ手順、複雑なテスト実行コマンド、環境構築手順書など

> 「手順が多くて面倒だけど、やることは毎回同じ」という操作がスキル化の候補

## 関連記事

- [[Git Worktreeの基本コマンドと使い方]]
- [[Git Worktreeを活用した並列開発パターン]]
- [[Claude Codeの三つの要素 - Skill・Agent・MCPの役割分担]]

引用元: [Git worktreeの運用をスキルに委ねる ―複雑さを隠蔽するClaude Codeスキル設計の実践―](https://tech.findy.co.jp/entry/2026/03/23/070000)
