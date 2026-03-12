"""
rm-guard.py - PreToolUse hook for Bash tool

rm / rmdir / mv コマンドを監視し、以下を保証する:
  1. 操作対象が Obsidian vault 内のパスであること
  2. .claude/rm-guard.json に指定された保護パスに触れないこと

ブロック時: エラーメッセージを stdout に出力して exit 2
  -> Claude Code が Claude へのフィードバックとして渡す
ログ: .claude/logs/rm-guard.log に記録
"""

from __future__ import annotations

import json
import re
import shlex
import sys
from datetime import datetime
from pathlib import Path

# vault_guard モジュールをロード (同じディレクトリに配置)
sys.path.insert(0, str(Path(__file__).parent))
from vault_guard import (
    VAULT_ROOT,
    CONFIG_FILE,
    load_config,
    normalize_path,
    is_within_vault,
    find_protected,
    check_path,
)

LOG_FILE = VAULT_ROOT / ".claude" / "logs" / "rm-guard.log"

CONTROLLED_COMMANDS = {"rm", "rmdir", "mv"}


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------


def log_blocked(command: str, reason: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] BLOCKED | {reason} | command: {command!r}\n")


# ---------------------------------------------------------------------------
# Command parsing
# ---------------------------------------------------------------------------


def split_compound_command(command: str) -> list[list[str]]:
    """&&, ||, ;, |, 改行 で区切られた複合コマンドを分解してトークンリストにする。"""
    segments = re.split(r"(?:&&|\|\||[;|\n])", command)
    result = []
    for seg in segments:
        seg = seg.strip()
        if not seg:
            continue
        try:
            parts = shlex.split(seg)
        except ValueError:
            parts = seg.split()
        if parts:
            result.append(parts)
    return result


def check_parts(parts: list[str], protected_paths: list[str]) -> str | None:
    """コマンドトークンを検証し、問題があれば理由を返す。問題なければ None。"""
    if not parts:
        return None

    # コマンド名を取得 (/usr/bin/rm -> rm)
    cmd = Path(parts[0]).name
    if cmd not in CONTROLLED_COMMANDS:
        return None

    args = parts[1:]
    # フラグ (-f, -rf, --force など) を除外してターゲットを抽出
    targets = [a for a in args if not a.startswith("-")]

    if not targets:
        return None

    if cmd == "mv":
        # mv の場合: 最後の引数が移動先、残りが移動元
        if len(targets) < 2:
            return None
        dest_str = targets[-1]
        dest = normalize_path(dest_str)
        if dest is None:
            return f"移動先パスを解析できませんでした: '{dest_str}'"
        if not is_within_vault(dest):
            return f"移動先 '{dest_str}' が vault 外のパスです"

        for src_str in targets[:-1]:
            src = normalize_path(src_str)
            if src is None:
                continue
            hit = find_protected(src, protected_paths)
            if hit:
                return f"移動元 '{src_str}' は保護されたパスです (設定: {hit})"

    else:
        # rm / rmdir: 全ターゲットをチェック
        for target_str in targets:
            reason = check_path(target_str, protected_paths)
            if reason:
                return reason

    return None


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    # Windows では stdout が cp932 になるため UTF-8 に固定する
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    if data.get("tool_name") != "Bash":
        sys.exit(0)

    command: str = data.get("tool_input", {}).get("command", "")
    if not command:
        sys.exit(0)

    # 制御対象コマンドが含まれない場合は早期終了
    cmd_tokens = set(re.findall(r"\brm\b|\brmdir\b|\bmv\b", command))
    if not cmd_tokens:
        sys.exit(0)

    config = load_config()
    protected_paths: list[str] = config.get("protected_paths", [])

    for parts in split_compound_command(command):
        reason = check_parts(parts, protected_paths)
        if reason:
            log_blocked(command, reason)
            print(f"[rm-guard] 操作がブロックされました: {reason}")
            sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
