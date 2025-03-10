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


def main(output_dir: str):
    # 参考元
    # https://tick-taku.com/blog/obsidian_mkdocs_githubactions_netlify_snk/#mkdocs-html
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

        # Obsidian形式の埋め込みリンクの修正のために、filesの後に実行する必要あり
        assets_embedded_links: set = set(
            map(
                lambda x: f"![[{os.path.basename(x)}]]",
                glob.glob(f"{output_dir}/{FILE_DIR}/*"),
            )
        )
        docs: dict = conf["docs"]
        pattern = r"\!\[\[.*]]"
        for from_, to_ in docs.items():
            output_path = f"{output_dir}/{to_}"
            shutil.copytree(from_, output_path, dirs_exist_ok=True)

            markdowns = glob.glob(f"{output_path}/*.md", recursive=True)
            for md in markdowns:
                md_path = Path(md)
                content = md_path.read_text(encoding="utf-8")

                contents_embedded_links: set[str] = set(re.findall(pattern, content))
                doc_embedded_links = contents_embedded_links.difference(
                    assets_embedded_links
                )
                image_with_size_pattern = r"!\[\[.*\|[0-9]+x?[0-9]*]]"
                for embedded_link in doc_embedded_links:
                    if re.search(image_with_size_pattern, embedded_link):
                        # 画像サイズ指定ありだとmkdocsでhtmlにしたときにサイズが反映されない、かつ文字列として{with="300"}のように表示されてしまう
                        # そのためサイズ指定を取り除く
                        idx = embedded_link.rfind("|")
                        print(idx)
                        content = content.replace(
                            embedded_link, f"{embedded_link[:idx]}]]"
                        )
                    else:
                        # 埋め込みリンクの!を削除
                        content = content.replace(embedded_link, embedded_link[1:])

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--local",
        help="ローカル試験用。.mkdocs配下にdocsフォルダを作成する。",
        action="store_true",
    )
    args = parser.parse_args()
    output_dir: str = f"{PREFERENCE_DIR}/{DOCKS_DIR}" if args.local else DOCKS_DIR
    main(output_dir)
