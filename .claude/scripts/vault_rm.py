"""
vault_rm.py - Vault-safe file/directory deletion script

使い方:
    python .claude/scripts/vault_rm.py <パス> [<パス> ...]

- Vault 内かつ保護パス外のファイル・ディレクトリのみ削除する
- ファイル・シンボリックリンク: os.remove
- ディレクトリ: shutil.rmtree（空でなくても削除）
- 各パスの処理結果を出力する
- 1 件でも失敗した場合は exit 1、全件成功なら exit 0
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

# vault_guard モジュールをロード (.claude/hooks/ 配下)
sys.path.insert(0, str(Path(__file__).parent.parent / "hooks"))
from vault_guard import VAULT_ROOT, check_path, load_config, normalize_path


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------


def delete_target(path_str: str, protected_paths: list[str]) -> tuple[bool, str]:
    """パスを検証して削除する。(成功フラグ, メッセージ) を返す。"""
    reason = check_path(path_str, protected_paths)
    if reason:
        return False, reason

    path = normalize_path(path_str)
    assert path is not None  # check_path が通過している時点で None にならない

    if not path.exists() and not path.is_symlink():
        return False, f"'{path_str}' は存在しません"

    try:
        if path.is_file() or path.is_symlink():
            os.remove(path)
        else:
            shutil.rmtree(path)
        return True, str(path)
    except Exception as e:
        return False, f"削除に失敗しました: {path} ({e})"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    if len(sys.argv) < 2:
        print("使い方: vault_rm.py <パス> [<パス> ...]", file=sys.stderr)
        sys.exit(1)

    config = load_config()
    protected_paths: list[str] = config.get("protected_paths", [])

    has_failure = False
    for path_str in sys.argv[1:]:
        ok, message = delete_target(path_str, protected_paths)
        if ok:
            print(f"[OK] {message}")
        else:
            print(f"[NG] {message}", file=sys.stderr)
            has_failure = True

    sys.exit(1 if has_failure else 0)


if __name__ == "__main__":
    main()
