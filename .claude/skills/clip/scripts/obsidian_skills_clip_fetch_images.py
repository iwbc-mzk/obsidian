#!/usr/bin/env python3
"""
fetch_images.py
Obsidian Web Clipperで保存されたMarkdownから画像URLを抽出し、
画像ファイルとしてローカル保存・メタ情報をJSONに出力するスクリプト。

出力構造:
  /tmp/clipping_images/          (--output で変更可)
  images.json                # メタ情報（local_path・alt・前後テキストなど）
  files/
      0001.png
      0002.jpg
      ...

images.json の各要素:
  {
    "url":            "元画像のURL",
    "alt":            "altテキスト",
    "media_type":     "image/png",
    "local_path":     "/tmp/clipping_images/files/0001.png",  // 取得成功時のみ
    "context_before": "画像直前のテキスト",
    "context_after":  "画像直後のテキスト",
    "error":          "fetch_failed"  // 取得失敗時のみ
  }

使い方:
  python3 fetch_images.py <markdownファイルパス> [オプション]

例:
  python3 fetch_images.py article.md
  python3 fetch_images.py article.md --max-images 20
  python3 fetch_images.py article.md --output /tmp/my_images/images.json
  python3 fetch_images.py article.md --timeout 30 --max-images 5
"""

import sys
import argparse
import re
import json
import urllib.request
import urllib.error
from pathlib import Path

DEFAULT_OUTPUT     = "/tmp/clipping_images/images.json"
DEFAULT_MAX_IMAGES = 30
DEFAULT_TIMEOUT    = 10


def extract_images_from_markdown(md_text: str) -> list[dict]:
    """
    Markdownから画像情報を抽出する。
    画像の前後2行をコンテキストとして合わせて取得する。
    """
    lines = md_text.splitlines()
    images = []
    pattern = re.compile(r'!\[([^\]]*)\]\((https?://[^\)]+)\)')

    for i, line in enumerate(lines):
        for match in pattern.finditer(line):
            alt = match.group(1).strip()
            url = match.group(2).strip()

            before_lines = [
                l.strip() for l in lines[max(0, i-3):i]
                if l.strip() and not l.strip().startswith('!')
            ]
            after_lines = [
                l.strip() for l in lines[i+1:min(len(lines), i+4)]
                if l.strip() and not l.strip().startswith('!')
            ]

            images.append({
                "url":            url,
                "alt":            alt,
                "context_before": " ".join(before_lines[-2:]),
                "context_after":  " ".join(after_lines[:2]),
            })

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


def download_image(url: str, dest_path: Path, timeout: int) -> tuple:
    """
    URLから画像をダウンロードして dest_path に保存する。
    MIMEタイプに合わせて拡張子を補正したPathを返す。
    失敗した場合は (None, "") を返す。
    """
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; ImageFetcher/1.0)"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content_type = response.headers.get("Content-Type", "")
            raw = response.read()

        media_type = guess_media_type(url, content_type)

        ext_map = {
            "image/jpeg": ".jpg",
            "image/png":  ".png",
            "image/gif":  ".gif",
            "image/webp": ".webp",
        }
        dest_path = dest_path.with_suffix(ext_map.get(media_type, ".jpg"))
        dest_path.write_bytes(raw)

        return dest_path, media_type

    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
        print(f"  [SKIP] {url}: {e}", file=sys.stderr)
        return None, ""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fetch_images.py",
        description="Obsidian Web ClipperのMarkdownから画像をダウンロードしてファイル保存・メタ情報をJSONに出力する",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  python3 fetch_images.py article.md
  python3 fetch_images.py article.md --max-images 20
  python3 fetch_images.py article.md --output /tmp/my_images/images.json
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
        "--output", "-o",
        metavar="OUTPUT_JSON",
        type=Path,
        default=Path(DEFAULT_OUTPUT),
        help=f"出力JSONファイルパス（画像はJSONと同じフォルダの files/ に保存） (デフォルト: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--max-images", "-n",
        metavar="N",
        type=int,
        default=DEFAULT_MAX_IMAGES,
        help=f"取得する最大画像数・トークン節約のため上限を設ける (デフォルト: {DEFAULT_MAX_IMAGES})",
    )
    parser.add_argument(
        "--timeout", "-t",
        metavar="SECONDS",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"HTTPタイムアウト秒数 (デフォルト: {DEFAULT_TIMEOUT})",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    md_path: Path     = args.markdown
    output_file: Path = args.output
    max_images: int   = args.max_images
    timeout: int      = args.timeout

    if not md_path.exists():
        parser.error(f"ファイルが見つかりません: {md_path}")

    # 画像保存先: JSONと同じディレクトリの files/ サブフォルダ
    files_dir = output_file.parent / "files"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    files_dir.mkdir(parents=True, exist_ok=True)

    md_text = md_path.read_text(encoding="utf-8")
    images_meta = extract_images_from_markdown(md_text)

    if not images_meta:
        print("画像URLが見つかりませんでした。")
        output_file.write_text(json.dumps([], ensure_ascii=False, indent=2), encoding="utf-8")
        sys.exit(0)

    print(f"画像を {len(images_meta)} 件検出。最大 {max_images} 件を処理します。")
    print(f"保存先: {files_dir}")

    results = []
    for i, meta in enumerate(images_meta[:max_images]):
        url = meta["url"]
        print(f"  [{i+1}/{min(len(images_meta), max_images)}] 取得中: {url}")

        # ファイル名は連番（拡張子はダウンロード後にMIMEタイプから確定）
        dest_path = files_dir / f"{i+1:04d}.tmp"
        saved_path, media_type = download_image(url, dest_path, timeout)

        if saved_path:
            results.append({
                "url":            url,
                "alt":            meta["alt"],
                "media_type":     media_type,
                "local_path":     str(saved_path),
                "context_before": meta["context_before"],
                "context_after":  meta["context_after"],
            })
            print(f"         OK -> {saved_path.name} ({media_type})")
        else:
            # 取得失敗してもメタ情報だけ残す
            results.append({
                "url":            url,
                "alt":            meta["alt"],
                "media_type":     None,
                "local_path":     None,
                "context_before": meta["context_before"],
                "context_after":  meta["context_after"],
                "error":          "fetch_failed",
            })

    output_file.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    success = sum(1 for r in results if r.get("local_path"))
    print(f"\n完了: {success}/{len(results)} 件取得 -> {output_file}")


if __name__ == "__main__":
    main()