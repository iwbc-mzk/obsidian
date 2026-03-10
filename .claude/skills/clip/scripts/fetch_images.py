#!/usr/bin/env python3
"""
fetch_images.py
Obsidian Web Clipperで保存されたMarkdownから画像URLを抽出し、
base64エンコードしてJSONファイルに保存するスクリプト。

使い方:
  python3 fetch_images.py <markdownファイルパス> [オプション]

例:
  python3 fetch_images.py article.md
  python3 fetch_images.py article.md --max-images 20
  python3 fetch_images.py article.md --output /tmp/my_images/result.json
  python3 fetch_images.py article.md --timeout 30 --max-images 5
"""

import sys
import argparse
import re
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path

DEFAULT_OUTPUT = f"{Path(__file__)}/tmp/clipping_images.json"
DEFAULT_MAX_IMAGES = 20
DEFAULT_TIMEOUT = 10


def extract_images_from_markdown(md_text: str) -> list[dict]:
    """
    Markdownから画像情報を抽出する。
    画像の前後2行をコンテキストとして合わせて取得する。
    """
    lines = md_text.splitlines()
    images = []
    pattern = re.compile(r"!\[([^\]]*)\]\((https?://[^\)]+)\)")

    for i, line in enumerate(lines):
        for match in pattern.finditer(line):
            alt = match.group(1).strip()
            url = match.group(2).strip()

            # 前後のテキスト行を取得（空行・画像行を除く）
            before_lines = [
                l.strip()
                for l in lines[max(0, i - 3) : i]
                if l.strip() and not l.strip().startswith("!")
            ]
            after_lines = [
                l.strip()
                for l in lines[i + 1 : min(len(lines), i + 4)]
                if l.strip() and not l.strip().startswith("!")
            ]

            images.append(
                {
                    "url": url,
                    "alt": alt,
                    "context_before": " ".join(before_lines[-2:]),
                    "context_after": " ".join(after_lines[:2]),
                }
            )

    return images


def guess_media_type(url: str, content_type: str = "") -> str:
    """URLとContent-TypeからMIMEタイプを判定する。"""
    if content_type:
        for mime in ["image/jpeg", "image/png", "image/gif", "image/webp"]:
            if mime in content_type:
                return mime

    url_lower = url.lower().split("?")[0]
    if url_lower.endswith(".jpg") or url_lower.endswith(".jpeg"):
        return "image/jpeg"
    if url_lower.endswith(".png"):
        return "image/png"
    if url_lower.endswith(".gif"):
        return "image/gif"
    if url_lower.endswith(".webp"):
        return "image/webp"
    return "image/jpeg"  # fallback


def fetch_image_as_base64(url: str, timeout: int) -> tuple[str, str]:
    """
    URLから画像をダウンロードしてbase64文字列とmedia_typeを返す。
    失敗した場合は (None, None) を返す。
    """
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (compatible; ImageFetcher/1.0)"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content_type = response.headers.get("Content-Type", "")
            raw = response.read()

        media_type = guess_media_type(url, content_type)
        encoded = base64.standard_b64encode(raw).decode("utf-8")
        return encoded, media_type

    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
        print(f"  [SKIP] {url}: {e}", file=sys.stderr)
        return None, None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fetch_images.py",
        description="Obsidian Web ClipperのMarkdownから画像をダウンロードしてbase64 JSONに保存する",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  python3 fetch_images.py article.md
  python3 fetch_images.py article.md --max-images 20
  python3 fetch_images.py article.md --output /tmp/my_images/result.json
  python3 fetch_images.py article.md --timeout 30 --max-images 5
        """,
    )
    parser.add_argument(
        "markdown",
        metavar="MARKDOWN_FILE",
        type=Path,
        help="処理対象のMarkdownファイルパス",
    )
    parser.add_argument(
        "--output",
        "-o",
        metavar="OUTPUT_JSON",
        type=Path,
        default=Path(DEFAULT_OUTPUT),
        help=f"出力JSONファイルパス (デフォルト: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--max-images",
        "-n",
        metavar="N",
        type=int,
        default=DEFAULT_MAX_IMAGES,
        help=f"取得する最大画像数・トークン節約のため上限を設ける (デフォルト: {DEFAULT_MAX_IMAGES})",
    )
    parser.add_argument(
        "--timeout",
        "-t",
        metavar="SECONDS",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"HTTPタイムアウト秒数 (デフォルト: {DEFAULT_TIMEOUT})",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    md_path: Path = args.markdown
    output_file: Path = args.output
    max_images: int = args.max_images
    timeout: int = args.timeout

    if not md_path.exists():
        parser.error(f"ファイルが見つかりません: {md_path}")

    md_text = md_path.read_text(encoding="utf-8")
    images_meta = extract_images_from_markdown(md_text)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    if not images_meta:
        print("画像URLが見つかりませんでした。")
        output_file.write_text(
            json.dumps([], ensure_ascii=False, indent=2), encoding="utf-8"
        )
        sys.exit(0)

    print(f"画像を {len(images_meta)} 件検出。最大 {max_images} 件を処理します。")

    results = []
    for i, meta in enumerate(images_meta[:max_images]):
        url = meta["url"]
        print(f"  [{i+1}/{min(len(images_meta), max_images)}] 取得中: {url}")
        data, media_type = fetch_image_as_base64(url, timeout)

        if data:
            results.append(
                {
                    "url": url,
                    "alt": meta["alt"],
                    "media_type": media_type,
                    "data": data,
                    "context_before": meta["context_before"],
                    "context_after": meta["context_after"],
                }
            )
            print(f"         OK ({media_type})")
        else:
            # 取得失敗してもメタ情報だけ残す
            results.append(
                {
                    "url": url,
                    "alt": meta["alt"],
                    "media_type": None,
                    "data": None,
                    "context_before": meta["context_before"],
                    "context_after": meta["context_after"],
                    "error": "fetch_failed",
                }
            )

    output_file.write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n完了: {output_file} に {len(results)} 件保存しました。")


if __name__ == "__main__":
    main()
