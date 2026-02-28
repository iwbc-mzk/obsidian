---
tags:
  - article
  - Python
source: https://stackoverflow.com/questions/50951955/pytesseract-tesseractnotfound-error-tesseract-is-not-installed-or-its-not-i
created: 2026-02-28 Sat 20:44
updated: 2026-02-28 Sat 20:44
---

# PytesseractのTesseractNotFoundError解決方法

## エラー内容

```text
TesseractNotFoundError: tesseract is not installed or it's not in your path
```

pytesseractはPythonのラッパーライブラリであり、Tesseract OCRバイナリが別途インストールされていないと動作しない。

## 原因

`pip install pytesseract` しただけでは不十分。TesseractのOCRバイナリ本体を別途インストールし、パスを通す必要がある。

## 解決手順

### ステップ1: Tesseractバイナリのインストール

#### Windows

[UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki) からインストーラーをダウンロードしてインストール。

デフォルトインストールパス（変更される場合があるため確認すること）：
```
C:\Users\USER\AppData\Local\Tesseract-OCR\
```

または：
```
C:\Program Files\Tesseract-OCR\
```

#### Linux (Ubuntu)

```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install libtesseract-dev
```

#### Mac

```bash
brew install tesseract
```

#### Conda (全OS共通)

```bash
conda install -c conda-forge tesseract
```

### ステップ2: Pythonスクリプトにパスを設定

TesseractがシステムのPATH環境変数に含まれていない場合、スクリプト内で明示的にパスを指定する。

```python
import pytesseract

# Windowsの場合
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# または（32bitインストール先の場合）
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

# ユーザーフォルダ配下にインストールした場合
import getpass
username = getpass.getuser()
pytesseract.pytesseract.tesseract_cmd = f'C:\\Users\\{username}\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'
```

### ステップ3: 動作確認

```python
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

im = Image.open("sample.jpg")
text = pytesseract.image_to_string(im, lang='eng')
print(text)
```

## Windows でインストールパスを調べる

```bash
# コマンドプロンプトで実行
where tesseract
```

または Anaconda 環境でインストール先を探す場合：

```python
import os
for r, s, f in os.walk("/"):
    for i in f:
        if "tesseract" in i:
            print(os.path.join(r, i))
```

## 言語ファイルが見つからない場合

`lang` パラメータで指定した言語がインストールされていない場合にも同様のエラーが出ることがある。

```bash
# インストール済み言語の確認
tesseract --list-langs

# 日本語を追加する場合（Linux）
sudo apt-get install tesseract-ocr-jpn

# スペイン語を追加する場合（Linux）
sudo apt-get install tesseract-ocr-spa
```

## 画像前処理を含む完全なサンプルコード

```python
import cv2
import numpy as np
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_string(img_path):
    # 画像の読み込み
    img = cv2.imread(img_path)

    # グレースケール変換
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ノイズ除去（膨張・収縮）
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # 一時ファイルに保存してOCR
    cv2.imwrite("processed.png", img)
    result = pytesseract.image_to_string(Image.open("processed.png"))
    return result

print(get_string("image.png"))
```

## よくあるミス

- バックスラッシュのエスケープ忘れ → raw文字列 `r'...'` を使う
  ```python
  # NG: \t がタブとして解釈される
  pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\tesseract.exe'

  # OK
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```
- `pip install pytesseract` のみでバイナリ未インストール → Tesseractバイナリを別途インストールすること
