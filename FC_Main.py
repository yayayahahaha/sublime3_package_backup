# Packages/User/FC_Main.py
# 這是你個人外掛的總入口檔案，負責從 Flyc 資料夾載入所有功能

# 1. 檔案管理相關功能
from .Flyc.FC_file_management import (
    CopyAllOpenPathsCommand,
    OpenFilesByRegexCommand,
    OpenSelectedFilesCommand,
    RegexSyntaxListener
)

# 2. 路徑跳轉與基礎工具 (原本的 reveal_alias_path.py)
from .Flyc.FC_reveal_alias_path import (
    RevealAliasPathCommand,
    CopyActiveFileNameCommand,
    CopyActiveRelativePathCommand,
    JumpToLastTabCommand,
    CloneToNewPaneCommand
)

# 3. Terminal 指令 (原本的 fc_terminal.py)
from .Flyc.FC_terminal import (
    RunStylelintFixCommand,
    RunEslintFixCommand
)

# 提示：如果你之後在 Flyc 資料夾內新增了新的 .py 檔案或指令類別，
# 記得要在這裡補上 import，指令才會在 Sublime Text 中生效喔！
