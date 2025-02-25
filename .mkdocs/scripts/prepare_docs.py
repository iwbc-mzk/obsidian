import yaml
import shutil
import os
import argparse


PREFERENCE_DIR = ".mkdocs"
DOCKS_DIR = "docs"


def main(output_dir: str):
    # 参考元
    # https://tick-taku.com/blog/obsidian_mkdocs_githubactions_netlify_snk/#mkdocs-html
    shutil.rmtree(output_dir, ignore_errors=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(f"{output_dir}/scripts", exist_ok=True)

    with open(f"{PREFERENCE_DIR}/conf.yml") as conf_file:
        conf = yaml.safe_load(conf_file)
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

        docs = conf["docs"]
        for from_, to_ in docs.items():
            shutil.copytree(from_, f"{output_dir}/{to_}", dirs_exist_ok=True)

        if "files" in conf:
            for file in conf["files"]:
                shutil.copytree(file, f"{output_dir}/{os.path.basename(file)}")

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
