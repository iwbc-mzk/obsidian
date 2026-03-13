---
slug: 1b0dc1f8-ac9c-4a1b-93fe-81a16f0ad740
tags:
  - article
  - ClaudeCode
  - Hooks
source: https://claude.ai/chat/2e45fdb9-e403-4b39-9002-ec6807b3fe1f
created: 2026-03-11
updated: 2026-03-13 Fri 14:05
---

# Claude Codeのパーミッション評価フローとダイアログ表示条件

Claude Code がツール呼び出しを受けたとき、パーミッションの評価はこの順序で行われる。

## 評価フロー

```
ツール呼び出し
    ↓
PreToolUse フック（deny設定に関わらず発火）
    ↓
deny ルール評価（マッチすればブロック）
    ↓
allow ルール評価（マッチすれば実行）
    ↓
PermissionRequest フック（allow/deny を返せばダイアログなし）
    ↓
どれにも解決されなかった場合 → パーミッションダイアログ表示
```

### 重要なポイント

- **PreToolUse は deny ルールより先に発火する**。`deny` 設定に記載されたコマンドでも PreToolUse フックは実行される。
- PreToolUse フックで `allow` を返しても、その後の `deny` ルールに一致すれば実行はブロックされる（ただし信頼性にバグ報告もあり）。
- 信頼性の高いブロックには、`deny` ルールと `PreToolUse` フック（`exit 2`）を組み合わせることが推奨される。

フックの詳細な使い方は [[Claude Code HooksのPreToolUseとPermissionRequestの違い]] を参照。

---

## パーミッションダイアログが表示される条件

ダイアログは「deny でも allow でもない、未解決の操作」に対して表示される。

### 表示される条件（`default` モード）

- ファイルの編集・書き込み（Edit / Write）
- Bash コマンドの実行
- allow ルールにも deny ルールにも一致しないツール操作
- ask ルールに一致するツール操作

### 表示されない条件

- allow ルールが一致した場合（自動実行）
- deny ルールが一致した場合（自動ブロック）
- PermissionRequest フックが `allow` または `deny` を返した場合

---

## パーミッションモードとダイアログの挙動

| モード | ダイアログの挙動 |
| --- | --- |
| `default` | 未解決の操作でダイアログ表示 |
| `acceptEdits` | ファイル編集はダイアログなし、Bash 等はそのまま |
| `plan` | 読み取りのみ許可、編集・実行はすべてブロック（ダイアログなし） |
| `dontAsk` | 未解決の操作はプロンプトを出さず自動拒否 |
| `bypassPermissions` | すべての操作をプロンプトなしで自動承認 |

---

## deny ルールの信頼性

`deny` ルールは設定した deny ルールが完全に機能しないというバグ報告があり、信頼性のある保護のためには `PreToolUse` フックで `exit 2` を使う方が確実とされている。

セキュリティを強化するには、deny ルールと PreToolUse フックを組み合わせて使うことが推奨される。

---

## ダイアログの「今後は確認しない」オプション

ダイアログには「Yes, and don't ask again for: コマンド名」という選択肢がある。選ぶと `.claude/settings.local.json` に allow ルールとして自動保存され、次回以降は表示されなくなる。

## 関連

- [[Claude Code HooksのPreToolUseとPermissionRequestの違い]]

引用元: Claude
