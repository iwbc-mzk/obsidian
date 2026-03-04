---
tags:
  - article
  - RAG
  - AIエージェント
  - LLM
created: 2026-03-03
updated: 2026-03-04 Wed 22:02
---

# RAGの仕組みと処理パイプライン

**RAG（Retrieval-Augmented Generation）**は、LLMのパラメータに含まれない非公開・最新データを検索（Retrieve）し、プロンプトを拡張（Augment）することでハルシネーション（もっともらしい嘘）を劇的に抑制する技術。

## 処理パイプライン

```
生データ
  ↓
【インジェクション】クリーニング → チャンク分割 → ベクトル化 → ベクトルDB格納
                                                                      ↑
ユーザークエリ                                                        ↓
  ↓                                                          【リトリーバル】
【リトリーバル】クエリをベクトル化 → コサイン類似度で類似チャンクを検索
  ↓
【オーグメンテーション】Re-ranking → Context Distillation（蒸留）
  ↓
【ジェネレーション】検索されたコンテキスト + プロンプト → LLMが回答生成
```

## 各フェーズの詳細

### 1. インジェクション（分割・ベクトル化）

1. 生データをクリーニング
2. **チャンク分割**：適切なサイズに分割
3. **埋め込みモデル（Embedding）**を用いてベクトル化
4. ベクトルデータベースへ格納

> **精度向上のポイント**：情報の密度を高めるための「メタデータ・フィルタリング（Metadata Filtering）」の付与が精度向上に寄与する

```python
# チャンク分割・ベクトル化の例（概略）
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# テキストをチャンクに分割
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

# ベクトル化してDBに格納
vectorstore = Chroma.from_documents(
    chunks,
    embedding=OpenAIEmbeddings(),
    metadatas=[{"source": doc.metadata["source"]} for doc in chunks]  # メタデータ付与
)
```

### 2. リトリーバル（検索）

1. クエリをベクトル化
2. **コサイン類似度**等で関連チャンクを抽出

> **高度な手法**：**HyDE（Hypothetical Document Embeddings）** — ユーザーの意図を「予測回答」としてベクトル化してから検索する手法。クエリ文と回答文の埋め込み空間の乖離を補正し、検索精度を向上させる

```python
# HyDE の概念実装例
def hyde_retrieval(query: str, llm, vectorstore):
    # 1. LLMに仮の回答を生成させる
    hypothetical_answer = llm.invoke(f"次の質問に対する回答を生成してください: {query}")
    # 2. 仮の回答をベクトル化して検索
    results = vectorstore.similarity_search(hypothetical_answer, k=5)
    return results
```

### 3. オーグメンテーション（拡張・最適化）

1. **Re-ranking（再ランク付け）**：抽出されたチャンクを関連性の高い順に再配置
2. **Context Distillation（コンテキスト蒸留）**：不要な情報を削ぎ落とし、プロンプトを最適化

### 4. ジェネレーション（生成）

検索された根拠資料に基づいてLLMが回答を生成。これによりハルシネーションを劇的に抑制する。

## RAGの特性まとめ

| 項目 | 内容 |
|------|------|
| **主な目的** | パッシブな知識の接地（グラウンディング） |
| **データの性質** | 静的なドキュメント・ベクトル埋め込み |
| **主な操作** | 検索（Read-only） |
| **解決する課題** | ハルシネーションの抑制 |
| **知識のスコープ** | 長期記憶（非構造化データ中心） |

## 関連

- [[MCPとRAGの比較とハイブリッドアーキテクチャ]]
- [[MCPの概要とNxM問題]]

引用元: NotebookLM
