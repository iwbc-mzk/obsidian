---
slug: 8d226c97-e287-425a-a1d0-e25cf8a67a22
tags:
  - article
  - MCP
  - AIエージェント
  - セキュリティ
created: 2026-03-03
updated: 2026-03-13 Fri 14:05
---

# MCPのセキュリティとAIエージェントの将来展望

MCPによる実行能力の拡大はセキュリティリスクの増大を意味する。強力な実行パスを保護するための対策と、MCPの将来展望を整理する。

## セキュリティリスク

MCPによって外部システムへの操作能力を持つAIエージェントが実現される一方で、以下のリスクへの対策が必須となる。

| リスク | 説明 |
|--------|------|
| **間接的なプロンプトインジェクション** | MCPサーバーが返すデータにLLMの行動を操作するコードが埋め込まれる攻撃 |
| **コマンドインジェクション** | MCPツールの引数に悪意のあるコマンドが注入される攻撃 |
| **データ漏洩（Data Exfiltration）** | ツールの組み合わせによって意図しない機密データが外部に送出されるリスク |

## セキュリティ対策

### Human-in-the-Loop（HITL）の義務化

機密性の高い操作（ファイル削除、外部APIへのPOST等）では、AI単独での実行を禁止し、必ず人間の確認ステップを挟む。

```python
# HITL実装の概念例
class SecureMCPTool:
    SENSITIVE_OPERATIONS = ["delete_file", "send_email", "create_payment"]

    async def execute_tool(self, tool_name: str, args: dict, user_consent: bool = False):
        if tool_name in self.SENSITIVE_OPERATIONS:
            if not user_consent:
                raise RequiresUserApproval(
                    f"'{tool_name}' は機密性の高い操作です。実行を許可しますか？"
                )
        return await self._run(tool_name, args)
```

### 厳格なサーバーサンドボックス化

- **Roots機能の活用**：MCPサーバーがアクセス可能なファイルシステム境界を最小権限の原則（Least Privilege）に基づいて制限
- サーバーを独立したプロセス・コンテナで実行し、ホストOSへの影響を最小化

### OAuthベースの権限管理

- MCPのStreamable HTTP（SSE）トランスポートではOAuth等の認証をサポート
- アクセストークンのスコープを「必要最小限の権限」に絞る

```yaml
# OAuth スコープ設定例
mcp_server:
  transport: streamable_http
  auth:
    type: oauth2
    scopes:
      - "github:read"       # 読み取りのみ許可
      # - "github:write"   # 書き込みは明示的に必要な場合のみ追加
```

## 将来展望

### Linux Foundation傘下への寄贈

2025年12月、Anthropic社はMCPを**Linux Foundation**傘下の**Agentic AI Foundation（AAIF）**へ寄贈。

- オープンなガバナンス体制のもとで業界標準としての地位を確立
- 特定ベンダーへの依存から独立したオープンな標準化が進む

### 応用領域の拡大

- **物理AI（Physical AI）**：ロボティクスや製造ラインなど、物理世界との統合
- **ソブリンAI（Sovereign AI）**：各国・組織が独自に制御可能なAIシステムへの応用

### エージェントの進化

RAGとMCPの統合により、AIエージェントは単なるチャットボットから以下へ進化する：

1. **自律的な情報収集**（RAGによる長期記憶）
2. **プロアクティブなアクション実行**（MCPによる実行能力）
3. **人間との協調判断**（HITLによる安全性確保）

## 関連

- [[MCPの概要とNxM問題]]
- [[MCPとRAGの比較とハイブリッドアーキテクチャ]]
- [[MCPのプロトコル仕様・トランスポート・コアプリミティブ]]

引用元: NotebookLM
