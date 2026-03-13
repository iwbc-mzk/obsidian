"""
既存のObsidianノートにUUID slugを一括追加するスクリプト。
対象: 03_MOC/, 04_Articles/, 06_ReadingNotes/ 配下の全.mdファイル
冪等: slug未設定のファイルのみ処理する
"""
import re
import uuid
from pathlib import Path

TARGET_DIRS = [
    Path("03_MOC"),
    Path("04_Articles"),
    Path("06_ReadingNotes"),
]

FRONTMATTER_PATTERN = re.compile(r"^---\r?\n(.*?)\r?\n---", re.DOTALL)
HAS_SLUG_PATTERN = re.compile(r"^slug\s*:", re.MULTILINE)


def add_slug(md_path: Path) -> bool:
    """ファイルに slug を追加する。追加した場合 True を返す。"""
    content = md_path.read_bytes().decode("utf-8")

    # 既に slug があればスキップ
    if HAS_SLUG_PATTERN.search(content):
        return False

    new_slug = str(uuid.uuid4())
    # 改行コードを検出（CRLF / LF）
    crlf = "\r\n" if "\r\n" in content else "\n"

    fm_match = FRONTMATTER_PATTERN.match(content)
    if fm_match:
        # フロントマターあり: 先頭行（---）の直後に slug を挿入
        insert_pos = len("---" + crlf)
        new_content = (
            content[:insert_pos]
            + f"slug: {new_slug}{crlf}"
            + content[insert_pos:]
        )
    else:
        # フロントマターなし: 先頭にフロントマターを作成
        new_content = f"---{crlf}slug: {new_slug}{crlf}---{crlf}{crlf}" + content

    md_path.write_bytes(new_content.encode("utf-8"))
    return True


def main():
    added = 0
    skipped = 0

    for target_dir in TARGET_DIRS:
        if not target_dir.exists():
            print(f"[SKIP] {target_dir} が見つかりません")
            continue

        for md_path in sorted(target_dir.rglob("*.md")):
            if add_slug(md_path):
                print(f"[ADD]  {md_path}")
                added += 1
            else:
                print(f"[SKIP] {md_path}")
                skipped += 1

    print(f"\n完了: {added} ファイルに slug を追加, {skipped} ファイルをスキップ")


if __name__ == "__main__":
    main()
