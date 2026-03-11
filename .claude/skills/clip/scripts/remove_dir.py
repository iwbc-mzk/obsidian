import shutil
import argparse
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
    "06_ReadingNotes",
    "Clippings",
]


def get_args():
    parser = argparse.ArgumentParser(
        prog="remove_dir.py",
        description="Obsidian Valut内のフォルダ全削除を行うスクリプト",
    )
    parser.add_argument(
        "target_dir",
        metavar="TARGET_DIR",
        type=str,
        help="削除対象のフォルダパス。Valutのルートパスからの相対パス（例: ./.tmp/）",
    )

    return parser.parse_args()


def remove_directory(target_dir: str):
    """
    Obsidian Valut内のフォルダ全削除を行うスクリプト
    Args:
        target_dir (str): 削除対象のフォルダパス。Valutのルートからの相対パス（例: ./.tmp/）
    Raises:
        ValueError: 削除対象のフォルダパスが絶対パスの場合
        ValueError: 解決後のパスがVault外を指している場合
        ValueError: 削除対象のフォルダが除外リストに含まれている場合
        ValueError: 削除対象のフォルダが見つからない場合
    """
    if Path(target_dir).is_absolute():
        raise ValueError(
            f"削除対象のフォルダパスはVaultのルートからの相対パスで指定してください: {target_dir}"
        )

    target_dir_abs_path = (VAULT_ABS_PATH / target_dir).resolve()

    if not target_dir_abs_path.is_relative_to(VAULT_ABS_PATH):
        raise ValueError(
            f"Vault外のパスは削除できません: {target_dir_abs_path}"
        )

    target_parts = target_dir_abs_path.relative_to(VAULT_ABS_PATH).parts
    for ex_dir in EXCLUDE_DIRS:
        if ex_dir in target_parts:
            raise ValueError(
                f"削除対象のフォルダは除外リストに含まれているため、削除をスキップします: {target_dir} (除外リスト: {EXCLUDE_DIRS})"
            )

    if not target_dir_abs_path.exists():
        raise ValueError(f"削除対象のフォルダが見つかりません: {target_dir_abs_path}")

    shutil.rmtree(target_dir_abs_path)
    print(f"削除完了: {target_dir_abs_path}")


def main():
    args = get_args()
    remove_directory(**vars(args))


if __name__ == "__main__":
    main()
