# Packages/User/FC_Main.py
import sys
import importlib

print("[FC] Loading FC_Main.py...")

# --- 核心：手動強制重新載入子模組，解決 ImportError 問題 ---
# 定義所有在 Flyc 資料夾下的模組
FC_SUBMODULES = [
    "User.Flyc.FC_file_management",
    "User.Flyc.FC_reveal_alias_path",
    "User.Flyc.FC_terminal",
    "User.Flyc.FC_git_conflict",
    "User.Flyc.FC_smart_fold",
    "User.Flyc.FC_TabSpaces" # 從分支合併進來的新模組
]

for mod_name in FC_SUBMODULES:
    if mod_name in sys.modules:
        print(f"[FC] Force reloading: {mod_name}")
        importlib.reload(sys.modules[mod_name])

# --- 正式匯入 ---

# 1. 檔案管理相關功能
from .Flyc.FC_file_management import (
    CopyAllOpenPathsCommand,
    OpenFilesByRegexCommand,
    OpenSelectedFilesCommand,
    RegexSyntaxListener,
    FcOpenSettingsCommand
)

# 2. 路徑跳轉與工具
from .Flyc.FC_reveal_alias_path import (
    RevealAliasPathCommand,
    CopyActiveFileNameCommand,
    CopyActiveRelativePathCommand,
    JumpToLastTabCommand,
    CloneToNewPaneCommand
)

# 3. Terminal 指令
from .Flyc.FC_terminal import (
    RunStylelintFixCommand,
    RunEslintFixCommand,
    RunStagedLintCommand
)

# 4. Git 衝突處理
from .Flyc.FC_git_conflict import (
    FcFoldGitConflictsCommand
)

# 5. 智慧折疊
from .Flyc.FC_smart_fold import (
    FcSmartFoldCommand
)

# 6. Tab 與縮排處理 (從戲言之二分支合併)
from .Flyc.FC_TabSpaces import ChangeTabSizeCommand

# 提示：如果你之後在 Flyc 資料夾內新增了新的 .py 檔案或指令類別，
# 記得要在這裡補上 import 並加入 FC_SUBMODULES，指令才會在 Sublime Text 中生效喔！

print("[FC] All modules loaded successfully.")
