---
tags:
  - article
  - MCP
  - AIエージェント
  - プロトコル
created: 2026-03-03
updated: 2026-03-04 Wed 10:46
---

# MCPのプロトコル仕様・トランスポート・コアプリミティブ

MCPは通信セマンティクスと物理転送を分離することで高度な相互運用性を確保している。

## プロトコル層（Protocol Layer）

**JSON-RPC 2.0** を採用。

- 双方向の通知（Notification）やリクエスト・レスポンスモデルをサポート
- ステートフルなセッション管理を実現
- 一貫した通信スキーマでの機能実行が可能

```json
// JSON-RPC 2.0 リクエスト例（ツール呼び出し）
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "read_file",
    "arguments": {
      "path": "/workspace/src/main.py"
    }
  }
}

// レスポンス例
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "def main():\n    print('Hello, World!')"
      }
    ]
  }
}
```

## トランスポート層（Transport Layer）

物理的な通信チャネルを定義する。2つの方式が標準的に利用される。

| 方式 | 通信メカニズム | 主な用途・技術的特徴 |
|------|--------------|-------------------|
| **Stdio** | 標準入力/標準出力（Standard I/O） | 同一マシン上のプロセス間通信。ローカル環境での実行に最適化され、極めて低遅延 |
| **Streamable HTTP (SSE)** | HTTP POST + Server-Sent Events | リモートサーバー間通信。OAuth等の認証をサポートし、クラウド経由の接続に必須 |

```python
# Stdioトランスポートの使用例（Python MCP SDK）
import mcp.server.stdio
from mcp.server import Server

app = Server("my-server")

@app.list_resources()
async def list_resources():
    return [
        Resource(uri="file:///data.txt", name="Data File", mimeType="text/plain")
    ]

if __name__ == "__main__":
    import asyncio
    asyncio.run(mcp.server.stdio.run(app))
```

## MCPの3つのコアプリミティブ

MCPの機能はAIが認識可能な3要素に抽象化される。

### リソース（Resources）

**読み取り専用のデータ。**ファイル内容やDBレコードの取得など、副作用を伴わない情報提供に特化。

```json
// リソース定義例
{
  "uri": "github://repos/owner/repo/contents/README.md",
  "name": "README",
  "description": "プロジェクトの説明ファイル",
  "mimeType": "text/markdown"
}
```

### ツール（Tools）

**実行可能な関数。**APIを介したレコード更新やファイルの作成など、外部システムの状態を変更する「副作用（Side Effects）」を伴う操作を定義。

```json
// ツール定義例
{
  "name": "create_issue",
  "description": "GitHubにIssueを作成する",
  "inputSchema": {
    "type": "object",
    "properties": {
      "title": { "type": "string", "description": "Issueのタイトル" },
      "body":  { "type": "string", "description": "Issueの本文" }
    },
    "required": ["title"]
  }
}
```

### プロンプト（Prompts）

**再利用可能な対話テンプレート。**AIモデルと外部環境の相互作用を構造化する。

## 高度なアーキテクチャ機能

| 機能 | 説明 |
|------|------|
| **Roots** | サーバーがアクセス可能なファイルシステム境界を制限し、最小権限の原則（Least Privilege）を強制 |
| **Sampling** | サーバー側からLLMに対して補完リクエストを行うことを許可し、エージェント的な推論ループをサポート |
| **Elicitation** | 実行中に不足している情報をユーザーに対して動的に要求する（問い返す）ワークフローを可能にする |

## 関連

- [[MCPの概要とNxM問題]]
- [[MCPのアーキテクチャとコンポーネント構成]]
- [[MCPとRAGの比較とハイブリッドアーキテクチャ]]

引用元: NotebookLM
