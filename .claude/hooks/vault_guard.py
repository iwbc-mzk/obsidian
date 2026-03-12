"""
vault_guard.py - Vault path guard utilities (shared module)

Vault パスの安全性チェックに使う共有ユーティリティ。
以下のスクリプトで共用する:
  - rm-guard.py  (PreToolUse フック)
  - vault_rm.py  (Vault 内ファイル削除スクリプト)
"""

from __future__ import annotations

import json
import re
from pathlib import Path

# .claude/hooks/vault_guard.py -> .claude/ -> vault root
VAULT_ROOT = Path(__file__).parent.parent.parent.resolve()
CONFIG_FILE = VAULT_ROOT / ".claude" / "rm-guard.json"


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


def load_config() -> dict:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"protected_paths": []}


# ---------------------------------------------------------------------------
# Path utilities
# ---------------------------------------------------------------------------


def normalize_path(path_str: str) -> Path | None:
    """パス文字列を絶対 Windows Path に変換する。

    対応形式:
      - 通常の Windows パス (C:/... or C:\\...)
      - Git Bash パス (/c/Users/...)
      - ホームディレクトリ (~/)
      - 相対パス (vault root を基点に解決)
    """
    if not path_str or path_str.startswith("-"):
        return None

    # Git Bash drive path: /c/Users/... -> C:/Users/...
    m = re.match(r"^/([a-zA-Z])(/|$)(.*)", path_str)
    if m:
        drive = m.group(1).upper()
        rest = m.group(3)
        path_str = f"{drive}:/{rest}"

    # Home directory
    if path_str.startswith("~/"):
        path_str = str(Path.home()) + path_str[1:]

    try:
        path = Path(path_str)
        if not path.is_absolute():
            path = VAULT_ROOT / path
        return path.resolve()
    except Exception:
        return None


def is_within_vault(path: Path) -> bool:
    try:
        path.relative_to(VAULT_ROOT)
        return True
    except ValueError:
        return False


def find_protected(path: Path, protected_paths: list[str]) -> str | None:
    """path が protected_paths のいずれかに該当すれば、一致した設定パスを返す。"""
    for entry in protected_paths:
        protected = (VAULT_ROOT / entry).resolve()
        try:
            if path == protected or path.is_relative_to(protected):
                return entry
        except Exception:
            pass
    return None


def check_path(path_str: str, protected_paths: list[str]) -> str | None:
    """パス文字列を検証し、削除が許可されない場合は理由を返す。問題なければ None。

    チェック内容:
      1. パスが解析できること
      2. Vault 内のパスであること
      3. 保護パスに該当しないこと
    """
    path = normalize_path(path_str)
    if path is None:
        return f"パスを解析できませんでした: '{path_str}'"
    if not is_within_vault(path):
        return f"削除対象 '{path_str}' が vault 外のパスです"
    hit = find_protected(path, protected_paths)
    if hit:
        return f"削除対象 '{path_str}' は保護されたパスです (設定: {hit})"
    return None
