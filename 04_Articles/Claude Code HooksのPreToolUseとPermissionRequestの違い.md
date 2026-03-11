---
tags:
  - article
  - ClaudeCode
  - Hooks
source: https://claude.ai/chat/2e45fdb9-e403-4b39-9002-ec6807b3fe1f
created: 2026-03-11
updated: 2026-03-11 Wed 22:54
---

# Claude Code HooksのPreToolUseとPermissionRequestの違い

Claude Code の Hooks には `PreToolUse` と `PermissionRequest` の2種類がある。両者はツール実行前に介入できる点は共通だが、**発火タイミングと役割が異なる**。

## 比較まとめ

| | `deny` ルール | `PreToolUse` フック | `PermissionRequest` フック |
| --- | --- | --- | --- |
| **仕組み** | 宣言的なパターンマッチング | カスタムスクリプトによる動的判断 | パーミッションダイアログ直前に介入 |
| **柔軟性** | グロブパターンのみ | 任意のロジック（引数の中身まで検査可能） | 任意のロジック |
| **発火タイミング** | ツール呼び出し後すぐ | deny ルールより前 | allow/deny どちらにも解決されなかった場合 |
| **用途** | シンプルなブロックルール | 複雑な条件判断・入力書き換え・ログ記録 | ダイアログ表示の自動化・委任 |

評価フローの詳細は [[Claude Codeのパーミッション評価フローとダイアログ表示条件]] を参照。

---

## PreToolUse

ツール呼び出しの**最初**に発火する。`deny` ルールよりも先に評価されるため、あらゆる操作をフックで制御できる。

### 設定の基本構造

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/your-script.sh"
          }
        ]
      }
    ]
  }
}
```

### フックが受け取るデータ（stdin）

```json
{
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": { "command": "rm -rf /tmp/old" },
  "session_id": "abc123",
  "cwd": "/home/user/project"
}
```

### スクリプトからの応答（stdout）

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "安全な操作です",
    "updatedInput": { "command": "rm -rf /tmp/old --dry-run" },
    "additionalContext": "Claudeへの追加情報"
  }
}
```

- `permissionDecision`: `allow` / `block` / `ask_user`
- `updatedInput`: ツール入力を書き換える（オプション）

### exit code による制御

| exit code | 動作 |
| --- | --- |
| `0` | 成功。stdout の JSON で詳細制御 |
| `2` | **ブロック**。ツール実行を停止、stderr がエラーメッセージになる |
| その他 | 非ブロッキングエラー（実行は継続） |

### 実用例：危険コマンドのブロック

```bash
#!/bin/bash
INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command')

# rm -rf を含むコマンドをブロック
if echo "$CMD" | grep -q "rm -rf"; then
  echo "危険なコマンドをブロックしました: $CMD" >&2
  exit 2
fi
exit 0
```

---

## PermissionRequest

パーミッションダイアログが**表示される直前**に発火する。`allow` にも `deny` にも解決されなかった操作に対してのみ呼び出される。matcher には引数レベルのパターンも使える。

### 設定の基本構造

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "Bash(npm test*)",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/validate.sh"
          }
        ]
      }
    ]
  }
}
```

### フックが受け取るデータ（stdin）

```json
{
  "hook_event_name": "PermissionRequest",
  "tool_name": "Bash",
  "tool_input": { "command": "npm test -- --coverage" },
  "session_id": "abc123"
}
```

### スクリプトからの応答（stdout）

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": { "command": "npm test" }
    }
  }
}
```

- `behavior`: `allow` / `deny` / `ask_user`
- フックが何も返さず `exit 0` で終了した場合は、デフォルトの挙動（ユーザーへのプロンプト表示）にフォールスルー

### 実用例：npm test を自動承認するスクリプト

```bash
#!/bin/bash
INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command')

if echo "$CMD" | grep -q "^npm test"; then
  echo '{"hookSpecificOutput":{"hookEventName":"PermissionRequest","decision":{"behavior":"allow"}}}'
  exit 0
fi

# それ以外はユーザーに委ねる
echo '{"hookSpecificOutput":{"hookEventName":"PermissionRequest","decision":{"behavior":"ask_user"}}}'
exit 0
```

---

## matcher の書き方

```
"Bash"              → Bashツールのみ
"Write|Edit"        → WriteまたはEdit
"*"                 → すべてのツール
"Bash(npm test*)"   → npm test で始まるBashコマンドのみ（PermissionRequestで有効）
"mcp__memory__.*"   → memoryサーバーのMCPツールすべて
```

**注意：matcher は大文字・小文字を区別する**（`"bash"` では `Bash` ツールにマッチしない）。

---

## 設定ファイルの場所

フックは3段階のレベルで管理できる。

| ファイル | 適用範囲 |
| --- | --- |
| `~/.claude/settings.json` | ユーザー全体のグローバル設定 |
| `.claude/settings.json` | リポジトリ内のプロジェクト共有設定（Git管理可能） |
| `.claude/settings.local.json` | コミットしたくない個人用ローカル設定 |

## 関連

- [[Claude Codeのパーミッション評価フローとダイアログ表示条件]]
- [[Claude Codeの三つの要素 - Skill・Agent・MCPの役割分担]]

引用元: Claude
