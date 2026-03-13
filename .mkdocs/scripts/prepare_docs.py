import yaml
import shutil
import os
import argparse
import glob
import re
from pathlib import Path


PREFERENCE_DIR = ".mkdocs"
DOCKS_DIR = "docs"
FILE_DIR = "Assets"

# フロントマターを取得するパターン
FRONTMATTER_PATTERN = re.compile(r"^---\r?\n(.*?)\r?\n---", re.DOTALL)
# [[Title]] [[Title|Display]] [[Title#anchor]] [[Title#anchor|Display]]
WIKILINK_PATTERN = re.compile(r"\[\[([^\]|#\n]+?)(?:#([^\]|\n]*?))?(?:\|([^\]\n]*?))?\]\]")


def extract_slug(md_path: Path) -> str | None:
    content = md_path.read_text(encoding="utf-8")
    fm_match = FRONTMATTER_PATTERN.match(content)
    if not fm_match:
        return None
    try:
        fm = yaml.safe_load(fm_match.group(1))
        if isinstance(fm, dict):
            return fm.get("slug")
    except yaml.YAMLError:
        pass
    return None


def build_slug_map(docs: dict) -> dict[str, tuple[str, str]]:
    slug_map: dict[str, tuple[str, str]] = {}
    for from_dir, to_section in docs.items():
        source_path = Path(from_dir)
        if not source_path.exists():
            continue
        for md_path in source_path.rglob("*.md"):
            slug = extract_slug(md_path)
            if slug:
                slug_map[md_path.stem.lower()] = (slug, to_section)
    return slug_map


def resolve_wikilinks(content: str, current_section: str, slug_map: dict) -> str:
    def replace_wikilink(m: re.Match) -> str:
        title = m.group(1).strip()
        anchor = m.group(2)
        display = m.group(3)

        slug_entry = slug_map.get(title.lower())
        if slug_entry is None:
            return m.group(0)

        slug, target_section = slug_entry

        if not current_section:
            link_path = f"{target_section}/{slug}.md"
        elif current_section == target_section:
            link_path = f"{slug}.md"
        else:
            link_path = f"../{target_section}/{slug}.md"

        if anchor:
            link_path += f"#{anchor}"

        label = display if display else title
        return f"[{label}]({link_path})"

    return WIKILINK_PATTERN.sub(replace_wikilink, content)


def inject_title(content: str, original_stem: str) -> str:
    fm_match = FRONTMATTER_PATTERN.match(content)
    if not fm_match:
        return content

    try:
        fm = yaml.safe_load(fm_match.group(1))
        if not isinstance(fm, dict) or "title" in fm:
            return content
    except yaml.YAMLError:
        return content

    safe_title = original_stem.replace("\\", "\\\\").replace('"', '\\"')
    crlf = "\r\n" if "\r\n" in content else "\n"
    insert_pos = len("---" + crlf)
    return (
        content[:insert_pos]
        + f"title: \"{safe_title}\"{crlf}"
        + content[insert_pos:]
    )


def main(output_dir: str):
    shutil.rmtree(output_dir, ignore_errors=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(f"{output_dir}/scripts", exist_ok=True)

    with open(f"{PREFERENCE_DIR}/conf.yml") as conf_file:
        conf: dict = yaml.safe_load(conf_file)
        shutil.copy(f"{PREFERENCE_DIR}/mkdocs.yml", "./")

        if "index" in conf:
            index = conf["index"]
            shutil.copy(index, f"{output_dir}/{os.path.basename(index)}")

        if "logo" in conf:
            logo = conf["logo"]
            shutil.copy(logo, f"{output_dir}/{os.path.basename(logo)}")

        if "favicon" in conf:
            favicon = conf["favicon"]
            shutil.copy(favicon, f"{output_dir}/{os.path.basename(favicon)}")

        if "custom_theme" in conf:
            theme = conf["custom_theme"]
            shutil.copytree(f"{PREFERENCE_DIR}/{theme}", theme, dirs_exist_ok=True)

        if "files" in conf:
            for file in conf["files"]:
                shutil.copytree(
                    file,
                    f"{output_dir}/{FILE_DIR}",
                    dirs_exist_ok=True,
                )

        assets_embedded_links: set = set(
            map(
                lambda x: f"![[{os.path.basename(x)}]]",
                glob.glob(f"{output_dir}/{FILE_DIR}/*"),
            )
        )
        docs: dict = conf["docs"]

        # 第1パス: slug マップの構築
        slug_map = build_slug_map(docs)

        # index の wikilinks をルートレベルとして解決
        if "index" in conf:
            index_dest = Path(f"{output_dir}/{os.path.basename(conf['index'])}")
            if index_dest.exists():
                idx_content = index_dest.read_text(encoding="utf-8")
                idx_content = resolve_wikilinks(idx_content, "", slug_map)
                index_dest.write_text(idx_content, encoding="utf-8")

        pattern = r"\!\[\[.*]]"
        for from_, to_ in docs.items():
            output_path = f"{output_dir}/{to_}"
            shutil.copytree(from_, output_path, dirs_exist_ok=True)

            markdowns = Path(output_path).rglob("*.md")
            for md_path in markdowns:
                content = md_path.read_text(encoding="utf-8")

                contents_embedded_links: set[str] = set(re.findall(pattern, content))
                doc_embedded_links = contents_embedded_links.difference(
                    assets_embedded_links
                )
                image_with_size_pattern = r"!\[\[.*\|[0-9]+x?[0-9]*]]"
                for embedded_link in doc_embedded_links:
                    if re.search(image_with_size_pattern, embedded_link):
                        idx = embedded_link.rfind("|")
                        content = content.replace(
                            embedded_link, f"{embedded_link[:idx]}]]"
                        )
                    else:
                        content = content.replace(embedded_link, embedded_link[1:])

                content = resolve_wikilinks(content, to_, slug_map)

                stem = md_path.stem
                slug_entry = slug_map.get(stem.lower())
                if slug_entry:
                    slug, _ = slug_entry
                    content = inject_title(content, stem)
                    slug_path = md_path.parent / f"{slug}.md"
                    md_path.write_text(content, encoding="utf-8")
                    md_path.rename(slug_path)
                else:
                    md_path.write_text(content, encoding="utf-8")

        if "scripts" in conf:
            for script in conf["scripts"]:
                shutil.copy(
                    f"{PREFERENCE_DIR}/scripts/{script}",
                    f"{output_dir}/scripts/{os.path.basename(script)}",
                )

        if "cname" in conf:
            cname_path = conf["cname"]
            if os.path.exists(cname_path):
                shutil.copy(cname_path, output_dir)


def get_args():
    parser = argparse.ArgumentParser(
        prog="prepare_docs.py",
        description="MkDocs用のドキュメントを準備するスクリプト",
    )
    parser.add_argument(
        "--local",
        help="ローカル試験用。.mkdocs配下にdocsフォルダを作成する。",
        action="store_true",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    output_dir: str = f"{PREFERENCE_DIR}/{DOCKS_DIR}" if args.local else DOCKS_DIR
    main(output_dir)
