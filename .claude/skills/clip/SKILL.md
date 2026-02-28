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
  - Bash(rm ./Clippings/*)
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

各mdファイルを読み取り以下のように整理する。

- 内容を精査しZettelkasten方式で記事を分割する
- Markdown含めコード例や記載例などは可能な限り記載する（例: AWSのIAMに関する記事なら、記事中のIAMのコード例を含める）
  (記事の内容を再現するために必要なコード例は必ず含める。コード例がない場合は、内容を理解するために必要なコード例を生成して含める)
- 分割した記事は整理先フォルダに格納する
- フォルダは新規作成しない
- ファイル名は分割した内容を反映させる
- ファイルはテンプレート（`./05_Template/Article.md`）に基づいて作成する
- 各種メタデータ（タイトル、タグ、テゴリ、サブカテゴリなど）を適切に反映させる

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

整理が完了したら、入力元フォルダ内の元のmdファイルを削除する。 -->

### 5. 処理結果レポート

整理結果をテーブル形式で表示する。
