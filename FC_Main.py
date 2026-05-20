import sys
import importlib

# 定義需要重新載入的模組清單
MODULES_TO_RELOAD = [
    ".Flyc.FC_file_management",
    ".Flyc.FC_reveal_alias_path",
    ".Flyc.FC_terminal",
    ".Flyc.FC_git_conflict"  # 新增
]

for module_name in MODULES_TO_RELOAD:
    full_module_name = "User" + module_name
    if full_module_name in sys.modules:
        importlib.reload(sys.modules[full_module_name])

# -----------------------------------------------------------
# 正式引入
# -----------------------------------------------------------

from .Flyc.FC_file_management import (
    CopyAllOpenPathsCommand,
    OpenFilesByRegexCommand,
    OpenSelectedFilesCommand,
    RegexSyntaxListener
)

from .Flyc.FC_reveal_alias_path import (
    RevealAliasPathCommand,
    CopyActiveFileNameCommand,
    CopyActiveRelativePathCommand,
    JumpToLastTabCommand,
    CloneToNewPaneCommand
)

from .Flyc.FC_terminal import (
    RunStylelintFixCommand,
    RunEslintFixCommand,
    RunStagedLintCommand
)

# 4. Git 衝突處理
from .Flyc.FC_git_conflict import (
    FcFoldGitConflictsCommand
)
