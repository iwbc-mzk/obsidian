---
tags:
  - article
  - ClaudeCode
  - Obsidian
source: https://dev.classmethod.jp/articles/obsidian-claude-clip/
created: 2026-02-28 Sat 12:15
updated: 2026-02-28 Sat 12:17
---

# Obsidian Web ClipperとClaude Code Skillで技術記事を自動整理する

Obsidian Web ClipperでWebページをMarkdown形式で保存し、Claude Codeのカスタムskill（`/clip`）でAIが記事内容を読み取り、カテゴリ別フォルダに自動整理する仕組み。

## 仕組みの全体像

```text
① ブラウザで記事をクリップ（Obsidian Web Clipper）
  ↓ Markdown形式で保存
② Obsidian Vault の Clippings/ に蓄積
  ↓ 記事が溜まったら...
③ Claude Code で /clip を実行
  ↓ AIが記事の内容を読み取り、カテゴリを判定
④ 04_Articles/ 配下に自動整理
     AWS/IAM/
     Terraform/Basics/
     GCP/CloudRun/
```

## /clip Skillの定義例

`~/.claude/skills/clip/SKILL.md` に配置するスキル定義：

```markdown
---
name: clip
description: Obsidian Web Clipperで保存された記事を読み取り、内容に基づいてカテゴリ・サブカテゴリを判定し、~/Documents/articles/ 配下にフォルダ階層を作成して自動整理する。
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash(mkdir *)
  - Bash(mv *)
  - Bash(ls *)
---

# Web Clip 記事整理スキル

Obsidian Web Clipperで保存されたMarkdown記事を読み取り、
内容を解析してカテゴリ別に自動整理する。

## パス設定

- **入力元**: `/Users/{ユーザー名}/Documents/obsidian/06_Articles`
- **整理先**: `/Users/{ユーザー名}/Documents/articles`

## ワークフロー

### 1. 未整理ファイルの検出

入力元フォルダ内の `.md` ファイルを全て取得する。
ファイルが0件なら「整理対象の記事はありません」と報告して終了。

### 2. 各ファイルの内容解析

各mdファイルを読み取り、以下を判定する:

#### カテゴリ（第1階層フォルダ）

記事の主要な技術領域を判定する。例:
- `AWS` - Amazon Web Services関連
- `GCP` - Google Cloud Platform関連
- `Azure` - Microsoft Azure関連
- `Terraform` - Terraform / IaC関連
- `Kubernetes` - Kubernetes / コンテナオーケストレーション関連
- その他、記事の内容に適した名前で新規作成

#### サブカテゴリ（第2階層フォルダ）

カテゴリ内の具体的なサービスや分野を判定する。例:
- AWS → `IAM`, `EC2`, `Lambda`, `S3`, `S3Tables` 等
- GCP → `IAM`, `CloudRun`, `GKE`, `BigQuery` 等
- Terraform → `Basics`, `Modules`, `State` 等

### 3. フォルダ作成とファイル移動

フォルダがなければ自動作成し、ファイルを移動する。

### 4. 処理結果レポート

整理結果をテーブル形式で表示する。

```

### 設計のポイント

1. **allowed-toolsの制限**: 必要最小限のツールのみ許可。意図しないファイル操作を防止
2. **カテゴリの柔軟性**: 定義済みカテゴリに限定せず、記事内容に応じて新規カテゴリも自動判断
3. **レポート出力**: 処理結果をテーブル形式で表示して確認しやすくする

### カテゴリ・サブカテゴリの例

| カテゴリ | サブカテゴリ例 |
|---------|--------------|
| AWS | IAM, EC2, Lambda, S3, S3Tables |
| GCP | IAM, CloudRun, GKE, BigQuery |
| Terraform | Basics, Modules, State |

## 実行例

```text
> /clip

3件のmdファイルが見つかりました。内容を読んで分類します。

| ファイル名 | カテゴリ | サブカテゴリ | 移動先 |
|-----------|---------|------------|-------|
| 知識ゼロからTerraform...md | Terraform | Basics | Terraform/Basics/ |
| Amazon S3 Tables...md | AWS | S3Tables | AWS/S3Tables/ |
```

## launchdによる自動化（macOS）の注意点

`claude -p "/clip を実行して"` の非対話モードと `launchd` の `WatchPaths` を組み合わせた自動化は、macOSのTCC（Transparency, Consent, and Control）セキュリティ制限により `~/Documents` フォルダへのアクセスが拒否される場合がある。

手動で `/clip` を実行する運用がシンプルで確実。

## 関連

- [[Claude Codeの三つの要素 - Skill・Agent・MCPの役割分担]]
- [[業務の繰り返しパターンをClaude Code Skillで可視化・自動化する]]
