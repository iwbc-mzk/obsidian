---
name: clip
description: Obsidian Web Clipperで保存された記事を読み取り、適切に記事を整理する。内容に基づいてカテゴリ・サブカテゴリを判定し、/04_Articles 配下にフォルダ階層を作成して自動整理する。
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

- **入力元**: `./Clippings`
- **整理先**: `./04_Articles`
- **カテゴリ分類先**: `./05_MOC`

## ワークフロー

### 1. 未整理ファイルの検出

入力元フォルダ内の `.md` ファイルを全て取得する。
ファイルが0件なら「整理対象の記事はありません」と報告して終了。

### 2. 各ファイルの内容解析

各mdファイルを読み取り、内容を精査しZettelkasten方式で記事を分割する。
分割した情報は整理先フォルダに格納する。
フォルダは新規作成せず、ファイル名は分割した内容を反映させる。
作成するファイルはテンプレート（`./05_Template`）に基づいて作成し、各種めたデータ（タイトル、タグ、カテゴリ、サブカテゴリなど）を適切に反映させる。

### 3. カテゴリ・サブカテゴリ判定

#### カテゴリ

分割したそれぞれの記事の主要な技術領域を判定する。
判定したカテゴリのMOCファイルに記事のリンクを追加する。
適したMOCがない場合は新規作成する。

例:

- `AWS` - Amazon Web Services関連
- `GCP` - Google Cloud Platform関連
- `Azure` - Microsoft Azure関連
- `Terraform` - Terraform / IaC関連
- `Kubernetes` - Kubernetes / コンテナオーケストレーション関連
- その他、記事の内容に適した名前で新規作成

#### サブカテゴリ

カテゴリ内の具体的なサービスや分野を判定する。
判定したサブカテゴリはMOC内でカテゴリの下に階層化して整理する。

例:

- AWS → `IAM`, `EC2`, `Lambda`, `S3`, `S3Tables` 等
- GCP → `IAM`, `CloudRun`, `GKE`, `BigQuery` 等
- Terraform → `Basics`, `Modules`, `State` 等

<!-- ### 4. Clip記事の削除

フォルダがなければ自動作成し、ファイルを移動する。 -->

### 5. 処理結果レポート

整理結果をテーブル形式で表示する。
