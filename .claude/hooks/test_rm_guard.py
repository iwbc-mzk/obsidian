"""
rm-guard.py の単体テスト

実行方法:
    python .claude/hooks/test_rm_guard.py
    python -m pytest .claude/hooks/test_rm_guard.py -v
"""

from __future__ import annotations

import importlib.util
import json
import sys
from io import StringIO
from pathlib import Path
from unittest import TestCase, main as unittest_main
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# rm-guard モジュールをハイフン付きファイル名からロード
# ---------------------------------------------------------------------------

_HOOKS_DIR = Path(__file__).parent
_spec = importlib.util.spec_from_file_location(
    "rm_guard", _HOOKS_DIR / "rm-guard.py"
)
rm_guard = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rm_guard)

# ---------------------------------------------------------------------------
# テスト共通ヘルパー
# ---------------------------------------------------------------------------

VAULT_ROOT: Path = rm_guard.VAULT_ROOT

# vault の外にある絶対パス（存在しなくてよい）
OUTSIDE_PATH = str(VAULT_ROOT.parent / "_rm_guard_test_outside" / "file.txt")

# テスト用の保護パスリスト（実際の rm-guard.json の一部）
TEST_PROTECTED = [".git", ".claude", "04_Articles", "CLAUDE.md"]


def vp(rel: str) -> str:
    """vault root からの相対パスを解決した文字列を返す"""
    return str((VAULT_ROOT / rel).resolve())


# ---------------------------------------------------------------------------
# normalize_path
# ---------------------------------------------------------------------------


class TestNormalizePath(TestCase):

    def test_empty_string_returns_none(self):
        self.assertIsNone(rm_guard.normalize_path(""))

    def test_short_flag_returns_none(self):
        self.assertIsNone(rm_guard.normalize_path("-rf"))

    def test_long_flag_returns_none(self):
        self.assertIsNone(rm_guard.normalize_path("--force"))

    def test_windows_absolute_path(self):
        p = rm_guard.normalize_path(str(VAULT_ROOT))
        self.assertEqual(p, VAULT_ROOT)

    def test_git_bash_drive_path_converted(self):
        # /c/Users/... -> C:/Users/...
        p = rm_guard.normalize_path("/c/Users")
        self.assertIsNotNone(p)
        self.assertEqual(p.drive.upper(), "C:")

    def test_git_bash_drive_only(self):
        # /c -> C:/
        p = rm_guard.normalize_path("/c")
        self.assertIsNotNone(p)
        self.assertEqual(p.drive.upper(), "C:")

    def test_git_bash_path_with_subdir(self):
        p = rm_guard.normalize_path("/c/Windows/System32")
        self.assertIsNotNone(p)
        self.assertIn("Windows", str(p))

    def test_relative_path_resolved_from_vault(self):
        p = rm_guard.normalize_path("Clippings/note.md")
        expected = (VAULT_ROOT / "Clippings" / "note.md").resolve()
        self.assertEqual(p, expected)

    def test_home_path(self):
        p = rm_guard.normalize_path("~/test_rm_guard.txt")
        expected = (Path.home() / "test_rm_guard.txt").resolve()
        self.assertEqual(p, expected)

    def test_home_path_prefix_only_not_matched(self):
        # "~foo" は home ディレクトリではない → 相対パスとして処理
        p = rm_guard.normalize_path("~foo/bar")
        # エラーにならず Path オブジェクトが返れば OK
        self.assertIsNotNone(p)


# ---------------------------------------------------------------------------
# is_within_vault
# ---------------------------------------------------------------------------


class TestIsWithinVault(TestCase):

    def test_vault_root_itself(self):
        self.assertTrue(rm_guard.is_within_vault(VAULT_ROOT))

    def test_direct_child_inside_vault(self):
        self.assertTrue(rm_guard.is_within_vault(VAULT_ROOT / "Clippings"))

    def test_deeply_nested_file_inside_vault(self):
        self.assertTrue(
            rm_guard.is_within_vault(VAULT_ROOT / ".claude" / "hooks" / "rm-guard.py")
        )

    def test_parent_of_vault_is_outside(self):
        self.assertFalse(rm_guard.is_within_vault(VAULT_ROOT.parent))

    def test_sibling_dir_is_outside(self):
        sibling = VAULT_ROOT.parent / "_sibling_of_vault"
        self.assertFalse(rm_guard.is_within_vault(sibling))

    def test_absolute_system_path_is_outside(self):
        self.assertFalse(rm_guard.is_within_vault(Path("C:/Windows")))

    def test_path_with_vault_name_prefix_is_outside(self):
        # vault が "obsidian" なら "obsidian_backup" は外
        fake = VAULT_ROOT.parent / (VAULT_ROOT.name + "_backup")
        self.assertFalse(rm_guard.is_within_vault(fake))


# ---------------------------------------------------------------------------
# find_protected
# ---------------------------------------------------------------------------


class TestFindProtected(TestCase):

    def test_exact_match_directory(self):
        path = (VAULT_ROOT / ".git").resolve()
        result = rm_guard.find_protected(path, TEST_PROTECTED)
        self.assertEqual(result, ".git")

    def test_child_of_protected_directory(self):
        path = (VAULT_ROOT / "04_Articles" / "subdir" / "file.md").resolve()
        result = rm_guard.find_protected(path, TEST_PROTECTED)
        self.assertEqual(result, "04_Articles")

    def test_deeply_nested_child_of_protected(self):
        path = (VAULT_ROOT / ".claude" / "hooks" / "rm-guard.py").resolve()
        result = rm_guard.find_protected(path, TEST_PROTECTED)
        self.assertEqual(result, ".claude")

    def test_exact_match_file(self):
        path = (VAULT_ROOT / "CLAUDE.md").resolve()
        result = rm_guard.find_protected(path, TEST_PROTECTED)
        self.assertEqual(result, "CLAUDE.md")

    def test_unprotected_path_returns_none(self):
        path = (VAULT_ROOT / "Clippings" / "note.md").resolve()
        result = rm_guard.find_protected(path, TEST_PROTECTED)
        self.assertIsNone(result)

    def test_empty_protected_list(self):
        path = (VAULT_ROOT / ".git").resolve()
        result = rm_guard.find_protected(path, [])
        self.assertIsNone(result)

    def test_directory_with_similar_prefix_not_matched(self):
        # "04_Articles_backup" は "04_Articles" ではない
        path = (VAULT_ROOT / "04_Articles_backup" / "file.md").resolve()
        result = rm_guard.find_protected(path, TEST_PROTECTED)
        self.assertIsNone(result)

    def test_first_matching_entry_is_returned(self):
        # 複数マッチする場合は先頭を返す
        # ".claude" と ".claude/hooks" の両方が保護リストにあるケース
        protected = [".claude/hooks", ".claude"]
        path = (VAULT_ROOT / ".claude" / "hooks" / "test.py").resolve()
        result = rm_guard.find_protected(path, protected)
        self.assertEqual(result, ".claude/hooks")


# ---------------------------------------------------------------------------
# split_compound_command
# ---------------------------------------------------------------------------


class TestSplitCompoundCommand(TestCase):

    def test_single_simple_command(self):
        result = rm_guard.split_compound_command("rm file.txt")
        self.assertEqual(result, [["rm", "file.txt"]])

    def test_and_operator(self):
        result = rm_guard.split_compound_command("rm a.txt && rm b.txt")
        self.assertEqual(result, [["rm", "a.txt"], ["rm", "b.txt"]])

    def test_or_operator(self):
        result = rm_guard.split_compound_command("rm a.txt || echo done")
        self.assertEqual(result, [["rm", "a.txt"], ["echo", "done"]])

    def test_semicolon(self):
        result = rm_guard.split_compound_command("ls; rm file.txt")
        self.assertEqual(result, [["ls"], ["rm", "file.txt"]])

    def test_pipe(self):
        result = rm_guard.split_compound_command("echo list | rm -")
        self.assertEqual(len(result), 2)

    def test_newline_separator(self):
        result = rm_guard.split_compound_command("rm a.txt\nrm b.txt")
        self.assertEqual(result, [["rm", "a.txt"], ["rm", "b.txt"]])

    def test_empty_segments_are_skipped(self):
        result = rm_guard.split_compound_command("  &&  ")
        self.assertEqual(result, [])

    def test_quoted_path_preserved_as_single_token(self):
        result = rm_guard.split_compound_command('rm "path/to/my file.md"')
        self.assertEqual(result, [["rm", "path/to/my file.md"]])

    def test_three_chained_commands(self):
        result = rm_guard.split_compound_command("a && b && c")
        self.assertEqual(len(result), 3)

    def test_command_with_flags(self):
        result = rm_guard.split_compound_command("rm -rf dir/")
        self.assertEqual(result, [["rm", "-rf", "dir/"]])

    def test_non_rm_command_parsed(self):
        result = rm_guard.split_compound_command("ls -la")
        self.assertEqual(result, [["ls", "-la"]])


# ---------------------------------------------------------------------------
# check_parts: rm コマンド
# ---------------------------------------------------------------------------


class TestCheckPartsRm(TestCase):

    def test_safe_vault_path_allowed(self):
        result = rm_guard.check_parts(["rm", vp("Clippings/note.md")], TEST_PROTECTED)
        self.assertIsNone(result)

    def test_protected_directory_blocked(self):
        result = rm_guard.check_parts(["rm", vp("04_Articles/file.md")], TEST_PROTECTED)
        self.assertIsNotNone(result)
        self.assertIn("保護", result)

    def test_protected_file_blocked(self):
        result = rm_guard.check_parts(["rm", vp("CLAUDE.md")], TEST_PROTECTED)
        self.assertIsNotNone(result)
        self.assertIn("保護", result)

    def test_vault_external_path_blocked(self):
        result = rm_guard.check_parts(["rm", OUTSIDE_PATH], TEST_PROTECTED)
        self.assertIsNotNone(result)
        self.assertIn("vault 外", result)

    def test_flag_only_no_targets_allowed(self):
        result = rm_guard.check_parts(["rm", "-rf"], TEST_PROTECTED)
        self.assertIsNone(result)

    def test_flag_before_safe_path_allowed(self):
        result = rm_guard.check_parts(["rm", "-f", vp("Clippings/note.md")], TEST_PROTECTED)
        self.assertIsNone(result)

    def test_flag_before_protected_path_blocked(self):
        result = rm_guard.check_parts(["rm", "-rf", vp(".git")], TEST_PROTECTED)
        self.assertIsNotNone(result)

    def test_multiple_safe_paths_allowed(self):
        result = rm_guard.check_parts(
            ["rm", vp("Clippings/a.md"), vp("Clippings/b.md")],
            TEST_PROTECTED,
        )
        self.assertIsNone(result)

    def test_mixed_safe_and_protected_blocked(self):
        result = rm_guard.check_parts(
            ["rm", vp("Clippings/safe.md"), vp("04_Articles/blocked.md")],
            TEST_PROTECTED,
        )
        self.assertIsNotNone(result)

    def test_empty_protected_list_allows_any_vault_path(self):
        result = rm_guard.check_parts(["rm", vp(".git/config")], [])
        self.assertIsNone(result)

    def test_empty_parts_returns_none(self):
        result = rm_guard.check_parts([], TEST_PROTECTED)
        self.assertIsNone(result)

    def test_nested_protected_child_blocked(self):
        result = rm_guard.check_parts(["rm", vp(".claude/hooks/rm-guard.py")], TEST_PROTECTED)
        self.assertIsNotNone(result)

    def test_relative_safe_path_via_normalize(self):
        # 相対パスは VAULT_ROOT 基点で解釈される
        result = rm_guard.check_parts(["rm", "Clippings/note.md"], TEST_PROTECTED)
        self.assertIsNone(result)

    def test_relative_protected_path_via_normalize(self):
        result = rm_guard.check_parts(["rm", "04_Articles/note.md"], TEST_PROTECTED)
        self.assertIsNotNone(result)


# ---------------------------------------------------------------------------
# check_parts: rmdir コマンド
# ---------------------------------------------------------------------------


class TestCheckPartsRmdir(TestCase):

    def test_safe_directory_allowed(self):
        result = rm_guard.check_parts(["rmdir", vp("Clippings")], TEST_PROTECTED)
        self.assertIsNone(result)

    def test_protected_directory_blocked(self):
        result = rm_guard.check_parts(["rmdir", vp(".claude")], TEST_PROTECTED)
        self.assertIsNotNone(result)

    def test_external_directory_blocked(self):
        ext = str(VAULT_ROOT.parent / "_ext_rmdir_test")
        result = rm_guard.check_parts(["rmdir", ext], TEST_PROTECTED)
        self.assertIsNotNone(result)
        self.assertIn("vault 外", result)

    def test_flag_only_no_targets(self):
        result = rm_guard.check_parts(["rmdir", "-p"], TEST_PROTECTED)
        self.assertIsNone(result)


# ---------------------------------------------------------------------------
# check_parts: mv コマンド
# ---------------------------------------------------------------------------


class TestCheckPartsMv(TestCase):

    def test_safe_source_to_safe_destination(self):
        result = rm_guard.check_parts(
            ["mv", vp("Clippings/a.md"), vp("Clippings/b.md")],
            TEST_PROTECTED,
        )
        self.assertIsNone(result)

    def test_external_destination_blocked(self):
        result = rm_guard.check_parts(
            ["mv", vp("Clippings/a.md"), OUTSIDE_PATH],
            TEST_PROTECTED,
        )
        self.assertIsNotNone(result)
        self.assertIn("vault 外", result)

    def test_protected_source_blocked(self):
        result = rm_guard.check_parts(
            ["mv", vp(".git/config"), vp("Clippings/config")],
            TEST_PROTECTED,
        )
        self.assertIsNotNone(result)
        self.assertIn("保護", result)

    def test_safe_source_protected_destination_not_source_check(self):
        # mv は移動先の保護チェックをしない（移動元のみ）
        result = rm_guard.check_parts(
            ["mv", vp("Clippings/a.md"), vp("04_Articles/a.md")],
            TEST_PROTECTED,
        )
        self.assertIsNone(result)

    def test_only_one_target_skipped(self):
        # 移動先が特定できない場合はスキップ
        result = rm_guard.check_parts(["mv", vp("Clippings/a.md")], TEST_PROTECTED)
        self.assertIsNone(result)

    def test_flag_ignored_correctly(self):
        result = rm_guard.check_parts(
            ["mv", "-n", vp("Clippings/a.md"), vp("Clippings/b.md")],
            TEST_PROTECTED,
        )
        self.assertIsNone(result)

    def test_multiple_sources_one_protected_blocked(self):
        result = rm_guard.check_parts(
            ["mv", vp("Clippings/a.md"), vp(".git/config"), vp("Clippings/dest/")],
            TEST_PROTECTED,
        )
        self.assertIsNotNone(result)


# ---------------------------------------------------------------------------
# check_parts: 制御対象外コマンド
# ---------------------------------------------------------------------------


class TestCheckPartsNonControlled(TestCase):

    def test_ls_command_passes_through(self):
        result = rm_guard.check_parts(["ls", "-la", vp("04_Articles")], TEST_PROTECTED)
        self.assertIsNone(result)

    def test_echo_command_passes_through(self):
        result = rm_guard.check_parts(["echo", "hello"], TEST_PROTECTED)
        self.assertIsNone(result)

    def test_python_command_passes_through(self):
        result = rm_guard.check_parts(["python", "script.py"], TEST_PROTECTED)
        self.assertIsNone(result)

    def test_full_path_rm_binary_recognized(self):
        # /usr/bin/rm のようなフルパス指定でも rm と認識されること
        result = rm_guard.check_parts(["/usr/bin/rm", OUTSIDE_PATH], TEST_PROTECTED)
        self.assertIsNotNone(result)


# ---------------------------------------------------------------------------
# main(): stdin 経由の統合テスト
# ---------------------------------------------------------------------------


class TestMain(TestCase):
    """main() をスタブ経由で統合テストする。

    load_config・log_blocked をモックし、stdin に JSON を流し込んで
    SystemExit のコードを検証する。
    """

    def _run(self, tool_name: str, command: str) -> int:
        """main() を実行して exit コードを返す"""
        payload = json.dumps(
            {"tool_name": tool_name, "tool_input": {"command": command}}
        )
        mock_config = {"protected_paths": TEST_PROTECTED}
        with patch("sys.stdin", StringIO(payload)), \
             patch.object(rm_guard, "load_config", return_value=mock_config), \
             patch.object(rm_guard, "log_blocked", MagicMock()), \
             patch("builtins.print"), \
             self.assertRaises(SystemExit) as ctx:
            rm_guard.main()
        return ctx.exception.code

    # --- 正常終了 (exit 0) ---

    def test_non_bash_tool_exits_0(self):
        self.assertEqual(self._run("Read", f'rm "{vp("Clippings/note.md")}"'), 0)

    def test_write_tool_exits_0(self):
        self.assertEqual(self._run("Write", f'rm -rf "{vp(".claude")}"'), 0)

    def test_empty_command_exits_0(self):
        self.assertEqual(self._run("Bash", ""), 0)

    def test_non_rm_command_exits_0(self):
        self.assertEqual(self._run("Bash", "ls -la"), 0)

    def test_python_command_exits_0(self):
        self.assertEqual(self._run("Bash", "python script.py"), 0)

    def test_safe_rm_single_file_exits_0(self):
        self.assertEqual(self._run("Bash", f'rm "{vp("Clippings/note.md")}"'), 0)

    def test_safe_rm_compound_both_safe_exits_0(self):
        a, b = vp("Clippings/a.md"), vp("Clippings/b.md")
        self.assertEqual(self._run("Bash", f'rm "{a}" && rm "{b}"'), 0)

    def test_safe_mv_inside_vault_exits_0(self):
        cmd = f'mv "{vp("Clippings/a.md")}" "{vp("Clippings/b.md")}"'
        self.assertEqual(self._run("Bash", cmd), 0)

    # --- ブロック (exit 2) ---

    def test_protected_rm_exits_2(self):
        self.assertEqual(self._run("Bash", f'rm "{vp("04_Articles/file.md")}"'), 2)

    def test_protected_dir_rm_rf_exits_2(self):
        self.assertEqual(self._run("Bash", f'rm -rf "{vp(".git")}"'), 2)

    def test_external_path_rm_exits_2(self):
        self.assertEqual(self._run("Bash", f'rm "{OUTSIDE_PATH}"'), 2)

    def test_protected_rmdir_exits_2(self):
        self.assertEqual(self._run("Bash", f'rmdir "{vp(".claude")}"'), 2)

    def test_mv_external_destination_exits_2(self):
        cmd = f'mv "{vp("Clippings/a.md")}" "{OUTSIDE_PATH}"'
        self.assertEqual(self._run("Bash", cmd), 2)

    def test_mv_protected_source_exits_2(self):
        cmd = f'mv "{vp(".git/COMMIT_EDITMSG")}" "{vp("Clippings/")}"'
        self.assertEqual(self._run("Bash", cmd), 2)

    def test_compound_safe_then_protected_exits_2(self):
        safe = vp("Clippings/a.md")
        protected = vp("04_Articles/b.md")
        self.assertEqual(self._run("Bash", f'rm "{safe}" && rm "{protected}"'), 2)

    def test_compound_protected_then_safe_exits_2(self):
        # 先にブロック対象が来ても検知される
        protected = vp(".claude/settings.json")
        safe = vp("Clippings/b.md")
        self.assertEqual(self._run("Bash", f'rm "{protected}" && rm "{safe}"'), 2)

    def test_claude_md_rm_exits_2(self):
        self.assertEqual(self._run("Bash", f'rm "{vp("CLAUDE.md")}"'), 2)

    # --- 異常入力 ---

    def test_invalid_json_exits_0(self):
        with patch("sys.stdin", StringIO("not valid json")), \
             self.assertRaises(SystemExit) as ctx:
            rm_guard.main()
        self.assertEqual(ctx.exception.code, 0)

    def test_empty_json_object_exits_0(self):
        with patch("sys.stdin", StringIO("{}")), \
             self.assertRaises(SystemExit) as ctx:
            rm_guard.main()
        self.assertEqual(ctx.exception.code, 0)

    def test_missing_tool_input_exits_0(self):
        payload = json.dumps({"tool_name": "Bash"})
        with patch("sys.stdin", StringIO(payload)), \
             self.assertRaises(SystemExit) as ctx:
            rm_guard.main()
        self.assertEqual(ctx.exception.code, 0)

    # --- ログ ---

    def test_blocked_command_calls_log_blocked_once(self):
        mock_log = MagicMock()
        payload = json.dumps(
            {"tool_name": "Bash", "tool_input": {"command": f'rm "{vp(".git/config")}"'}}
        )
        mock_config = {"protected_paths": TEST_PROTECTED}
        with patch("sys.stdin", StringIO(payload)), \
             patch.object(rm_guard, "load_config", return_value=mock_config), \
             patch.object(rm_guard, "log_blocked", mock_log), \
             patch("builtins.print"), \
             self.assertRaises(SystemExit):
            rm_guard.main()
        mock_log.assert_called_once()

    def test_blocked_log_contains_command_and_reason(self):
        mock_log = MagicMock()
        cmd = f'rm "{vp("04_Articles/note.md")}"'
        payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": cmd}})
        mock_config = {"protected_paths": TEST_PROTECTED}
        with patch("sys.stdin", StringIO(payload)), \
             patch.object(rm_guard, "load_config", return_value=mock_config), \
             patch.object(rm_guard, "log_blocked", mock_log), \
             patch("builtins.print"), \
             self.assertRaises(SystemExit):
            rm_guard.main()
        call_args = mock_log.call_args
        logged_command, logged_reason = call_args[0]
        self.assertIn("rm", logged_command)
        self.assertIsInstance(logged_reason, str)
        self.assertTrue(len(logged_reason) > 0)

    def test_safe_command_does_not_call_log_blocked(self):
        mock_log = MagicMock()
        payload = json.dumps(
            {"tool_name": "Bash", "tool_input": {"command": f'rm "{vp("Clippings/note.md")}"'}}
        )
        mock_config = {"protected_paths": TEST_PROTECTED}
        with patch("sys.stdin", StringIO(payload)), \
             patch.object(rm_guard, "load_config", return_value=mock_config), \
             patch.object(rm_guard, "log_blocked", mock_log), \
             patch("builtins.print"), \
             self.assertRaises(SystemExit):
            rm_guard.main()
        mock_log.assert_not_called()


if __name__ == "__main__":
    unittest_main(verbosity=2)
