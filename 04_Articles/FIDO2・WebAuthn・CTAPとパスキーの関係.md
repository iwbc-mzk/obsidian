---
tags:
  - article
  - セキュリティ
  - パスキー
  - 認証
  - FIDO2
  - WebAuthn
created: 2026-03-01
updated: 2026-03-04 Wed 22:49
---

# FIDO2・WebAuthn・CTAPとパスキーの関係

パスキー、FIDO2、WebAuthnは密接に関連しており、**FIDO2という標準規格の枠組みの中で、WebAuthnなどの技術を用いて実現される具体的な認証資格情報（鍵）がパスキー**である。

## 全体像

```
FIDO2（全体を支える標準規格）
├── WebAuthn（ブラウザ ↔ Webサイト間のAPI）
└── CTAP（クライアント端末 ↔ 外部認証器間のプロトコル）
         ↓
    パスキー（FIDO2規格に基づいて作成される具体的な暗号鍵のペア）
```

建築の比喩：
- **FIDO2**：家（認証システム）を建てるための建築基準・設計図
- **WebAuthn / CTAP**：設計図を実現するための具体的な工法や部品の規格
- **パスキー**：その規格に沿って作られた、ユーザーが実際に持ち歩く「物理的な鍵」に代わるデジタルな鍵

## 各要素の役割

### FIDO2：全体を支える標準規格

FIDOアライアンスとW3Cによって策定された、パスワードに依存しない安全な認証を実現するための広範な標準規格（技術的枠組み）。パスキーはこのFIDO2の仕組みを基盤として動作する。

FIDO2は主に以下の2つの重要な技術仕様で構成される：
- **WebAuthn（Web Authentication API）**
- **CTAP（Client to Authenticator Protocol）**

### WebAuthn：ブラウザとサイトをつなぐ窓口

ウェブブラウザやOSがウェブサイト（リライング・パーティ）と通信し、パスキーを登録・管理するための**標準API（インターフェース）**。

- ウェブサイト側はこのAPIを呼び出すことで、ユーザーのデバイスに対してパスキーの生成や認証の要求を送れる
- 現在、主要なブラウザやOSのほとんどがWebAuthnに対応している

```javascript
// WebAuthnを使ったパスキー登録の例（概略）
const credential = await navigator.credentials.create({
  publicKey: {
    challenge: serverChallenge,        // サーバーから受け取ったチャレンジ
    rp: { name: "Example Site", id: "example.com" },  // リライング・パーティ情報
    user: { id: userId, name: "user@example.com", displayName: "User" },
    pubKeyCredParams: [{ type: "public-key", alg: -7 }],  // ES256アルゴリズム
    authenticatorSelection: { userVerification: "required" }
  }
});
// credential.response.attestationObject → サーバーへ送信して登録完了
```

```javascript
// WebAuthnを使ったパスキー認証の例（概略）
const assertion = await navigator.credentials.get({
  publicKey: {
    challenge: serverChallenge,  // 使い捨てのランダムデータ
    allowCredentials: [{ type: "public-key", id: credentialId }],
    userVerification: "required"
  }
});
// assertion.response.signature → サーバーへ送信して検証
```

### CTAP：デバイスと認証器をつなぐ通信手段

PCなどのクライアント端末が、外部の認証器（スマートフォンやハードウェアセキュリティキー等）と通信して認証を行うための**プロトコル（通信規約）**。

- PCでログインする際に手元のスマートフォンで本人確認を行う「クロスデバイス認証（QRコードを使ったハイブリッド認証）」などはCTAPの仕組みを利用している

### パスキー：ユーザーが手にする「鍵」そのもの

FIDO2規格に基づいて作成される**具体的な認証資格情報（デジタルな鍵）**の名称。

- 技術的には「公開鍵暗号方式」を用いた暗号鍵のペア（秘密鍵 + 公開鍵）を指す
- ユーザーにとっては、デバイスのロック解除と同じ操作（生体認証やPIN）でパスワードを入力せずにログインできる「機能名・製品名」として馴染みがある

## 実装の観点

ウェブサービスが「パスキーに対応する」ことは、技術的には「FIDO2規格（WebAuthn API等）を実装する」ことと同義。

## 関連

- [[パスキーの認証の仕組み]]
- [[公開鍵暗号の一方向性と量子コンピュータへの耐性]]

引用元: NotebookLM
