import shutil
import argparse
import os
from pathlib import Path

# Obsidian Vaultのルートパスを取得
VAULT_ABS_PATH = Path(__file__).parent.parent.parent.parent.parent.resolve()


EXCLUDE_DIRS = [
    ".claude",
    ".github",
    ".obsidian",
    ".mkdocs",
    ".vscode",
    "00_Index",
    "01_Assets",
    "02_Daily",
    "03_MOC",
    "04_Articles",
    "05_Templates",
    "Clippings",
]


def get_args():
    parse = argparse.ArgumentParser(
        prog="remove_dir.py",
        description="Obsidian Valut内のフォルダ全削除を行うスクリプト",
    )
    parse.add_argument(
        "target_dir",
        metavar="TARGET_DIR",
        type=str,
        help="削除対象のフォルダパス。Valutのルートパスからの相対パス（例: ./.tmp/）",
    )

    return parse.parse_args()


def remove_directory(target_dir: str):
    """
    Obsidian Valut内のフォルダ全削除を行うスクリプト
    Args:
        dir_path (str): 削除対象のフォルダパス。Valutのルートパスからの相対パス（例: ./.tmp/）
     Raises:
        ValueError: 削除対象のフォルダパスがVaultのルートからの相対パスでない場合
        ValueError: 削除対象のフォルダが除外リストに含まれている場合
    """
    if os.path.isabs(target_dir):
        raise ValueError(
            f"削除対象のフォルダパスはVaultのルートからの相対パスで指定してください: {target_dir}"
        )

    for ex_dir in EXCLUDE_DIRS:
        if ex_dir in target_dir:
            raise ValueError(
                f"削除対象のフォルダは除外リストに含まれているため、削除をスキップします: {target_dir} (除外リスト: {EXCLUDE_DIRS})"
            )

    target_dir_abs_path = VAULT_ABS_PATH / target_dir
    shutil.rmtree(target_dir_abs_path)
    print(f"削除完了: {target_dir_abs_path}")


def main():
    args = get_args()
    remove_directory(**vars(args))


if __name__ == "__main__":
    main()
