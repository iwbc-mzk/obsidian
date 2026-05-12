---
tags:
  - article
  - Python
  - PyTorch
  - AI
  - CUDA
aliases: []
slug: c1d6e0f9-f2a3-4b58-6789-0d1e2f3a4b59
created: 2026-05-11
updated: 2026-05-11 Mon 23:45
---

# PyTorchのインストール手順（CUDA・GPU対応）

## 概要

PyTorch をインストールするには GPU の型番・CUDA のバージョン・ドライバのバージョンの互換性を確認する必要がある。以下の手順で進める。

対象：Windows + NVIDIA GPU 環境

## 手順1: CUDAの確認

まず CUDA がインストール済みか確認する。

```bash
nvcc --version
```

出力例（CUDA 12.3 の場合）：

```
nvcc: NVIDIA (R) Cuda compiler driver
Cuda compilation tools, release 12.3, V12.3.103
```

- インストール済みであれば [手順8](#手順8-pytorchのインストール) へ
- インストールされていなければ手順2から進む

## 手順2: GPUの型番の確認

タスクマネージャーの「パフォーマンス」タブ → GPU で確認する。

![[pytorch-gpu-taskmanager.png|500]]

出典: [PyTorchのインストール手順](https://zenn.dev/ledmirage/articles/8ead5b31a42f1d)

## 手順3: GPUのマイクロアーキテクチャの確認

Wikipedia の CUDA 対応表などで、GPU 型番のマイクロアーキテクチャを調べる。

![[pytorch-gpu-microarchitecture.png|600]]

出典: [PyTorchのインストール手順](https://zenn.dev/ledmirage/articles/8ead5b31a42f1d)

例：GTX 1660 SUPER → **Turing**

## 手順4: 互換性のあるCUDAのバージョンを確認

同表の上段で、マイクロアーキテクチャに対応する CUDA バージョンを調べる。

![[pytorch-cuda-compat-table.png|600]]

出典: [PyTorchのインストール手順](https://zenn.dev/ledmirage/articles/8ead5b31a42f1d)

例：Turing → CUDA 10.0 〜 12.8 に対応

基本的に使える最新バージョンをインストールする。

## 手順5: GPUドライバのバージョンの確認

NVIDIA Control Panel → ヘルプ → システム情報 で確認。

![[pytorch-driver-version.png|500]]

出典: [PyTorchのインストール手順](https://zenn.dev/ledmirage/articles/8ead5b31a42f1d)

## 手順6: GPUドライバの互換性の確認

NVIDIA の公式ページで CUDA バージョンとドライババージョンの互換性を確認する。

![[pytorch-cuda-driver-compat.png|600]]

出典: [PyTorchのインストール手順](https://zenn.dev/ledmirage/articles/8ead5b31a42f1d)

例：CUDA 12.8 を使うには Windows ドライバ >= 572.61 が必要。

ドライバが古い場合は NVIDIA の公式から更新する。

## 手順7: CUDA Toolkitのインストール

NVIDIA の CUDA Toolkit ダウンロードページから OS・アーキテクチャ・バージョンを選んでダウンロード。

![[pytorch-cuda-download.png|600]]

出典: [PyTorchのインストール手順](https://zenn.dev/ledmirage/articles/8ead5b31a42f1d)

## 手順8: PyTorchのインストール

PyTorch 公式サイトのインストールコマンド生成ツールで環境を選択してコマンドを取得する。

![[pytorch-install-command.png|600]]

出典: [PyTorchのインストール手順](https://zenn.dev/ledmirage/articles/8ead5b31a42f1d)

インストールコマンド例（CUDA 12.1 の場合）：

```bash
# CUDA 12.1
pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu121
```

> **ポイント:** ぴったりの CUDA バージョンが見つからない場合は、使用中の CUDA バージョン以下（メジャーバージョンは合わせる）の PyTorch をインストールすればよい。

## 手順9: 動作確認

```python
import torch
print(torch.__version__)        # バージョン確認
print(torch.cuda.is_available()) # GPUが使えるか確認（Trueなら OK）
x = torch.rand(5, 3)            # ランダムなテンソルを作成
print(x)
```

## まとめ：インストール手順のフロー

```
CUDAインストール済み？
├─ Yes → 手順8へ（PyTorchをインストール）
└─ No → GPU型番確認 → マイクロアーキテクチャ確認
         → 互換CUDAバージョン確認 → ドライバ互換確認
         → （必要なら）ドライバ更新 → CUDA Toolkitインストール
         → 手順8へ
```

引用元: [PyTorchのインストール手順](https://zenn.dev/ledmirage/articles/8ead5b31a42f1d)
