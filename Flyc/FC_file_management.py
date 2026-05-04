import os
import re
import sublime
import sublime_plugin

# ==========================================
# 1. 一次複製全部開啟的檔案的檔案路徑
# ==========================================
class CopyAllOpenPathsCommand(sublime_plugin.WindowCommand):
    def run(self, relative=False):
        paths = []
        folders = self.window.folders()
        
        for view in self.window.views():
            file_path = view.file_name()
            if not file_path:
                continue
            
            # 正規化路徑
            real_file_path = os.path.realpath(file_path)
            
            if relative:
                rel_path = real_file_path
                for folder in folders:
                    real_folder = os.path.realpath(folder)
                    if real_file_path.startswith(real_folder):
                        rel_path = os.path.relpath(real_file_path, real_folder).replace('\\', '/')
                        break
                paths.append(rel_path)
            else:
                paths.append(real_file_path)
        
        if paths:
            # 移除重複 (同一個檔案可能開多個 tab)
            unique_paths = list(dict.fromkeys(paths))
            content = "\n".join(unique_paths)
            sublime.set_clipboard(content)
            sublime.status_message(f"Copied {len(unique_paths)} paths")
        else:
            sublime.status_message("No open files with paths")

# ==========================================
# 2. 一次開啟符合正規表達式的所有檔案
# ==========================================
class OpenFilesByRegexCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel("Enter Regex to open files:", "", self.on_done, None, None)

    def on_done(self, pattern):
        if not pattern:
            return
        
        try:
            regex = re.compile(pattern)
        except Exception as e:
            sublime.error_message(f"Invalid Regex: {str(e)}")
            return

        # 讀取設定 (可擴充 ignore 邏輯)
        settings = sublime.load_settings("Flyc/FC_FileManagement.sublime-settings")
        ignore_patterns = settings.get("ignore_patterns", [
            "node_modules", ".git", "__pycache__", ".DS_Store", "dist", "build"
        ])
        
        folders = self.window.folders()
        if not folders:
            sublime.status_message("No folders in project")
            return

        matched_files = []
        
        for root_folder in folders:
            for root, dirs, files in os.walk(root_folder):
                # 過濾目錄 (原地修改 dirs 以跳過)
                dirs[:] = [d for d in dirs if d not in ignore_patterns]
                
                for file in files:
                    if file in ignore_patterns:
                        continue
                        
                    # 取得相對路徑來做匹配，這比較實用
                    rel_path = os.path.relpath(os.path.join(root, file), root_folder)
                    if regex.search(rel_path) or regex.search(file):
                        matched_files.append(os.path.join(root, file))

        if not matched_files:
            sublime.status_message("No files matched the regex")
            return

        count = len(matched_files)
        if count > 50: # 安全閥
            if not sublime.ok_cancel_dialog(f"Found {count} files. Are you sure you want to open them all?", "Open All"):
                return
        elif not sublime.ok_cancel_dialog(f"Open {count} matched files?", "Open"):
            return

        for f in matched_files:
            self.window.open_file(f)

# ==========================================
# 3. 一次開啟所選擇的所有檔名 (支援 Newline 分隔)
# ==========================================
class OpenSelectedFilesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window = self.view.window()
        if not window:
            return

        # 取得所有選擇區塊
        for sel in self.view.sel():
            if sel.empty():
                continue
            
            text = self.view.substr(sel)
            # 支援 newline 分隔並 trim
            file_names = [f.strip() for f in text.split("\n") if f.strip()]
            
            for name in file_names:
                self.open_file_by_name(window, name)

    def open_file_by_name(self, window, name):
        # 1. 嘗試當作絕對路徑
        if os.path.isabs(name) and os.path.exists(name):
            window.open_file(name)
            return

        # 2. 嘗試相對於當前檔案
        current_file = self.view.file_name()
        if current_file:
            base_dir = os.path.dirname(current_file)
            candidate = os.path.normpath(os.path.join(base_dir, name))
            if os.path.exists(candidate):
                window.open_file(candidate)
                return

        # 3. 嘗試相對於專案目錄
        for folder in window.folders():
            candidate = os.path.normpath(os.path.join(folder, name))
            if os.path.exists(candidate):
                window.open_file(candidate)
                return
        
        # 4. 如果都找不到，嘗試在專案中搜尋 (模糊匹配檔名)
        sublime.status_message(f"File not found: {name}")

# ==========================================
# 4. 自動根據檔名正則切換 Syntax (回答使用者的問題)
# ==========================================
class RegexSyntaxListener(sublime_plugin.EventListener):
    def on_load(self, view):
        self.apply_regex_syntax(view)
        
    def on_post_save(self, view):
        self.apply_regex_syntax(view)

    def apply_regex_syntax(self, view):
        file_name = view.file_name()
        if not file_name:
            return
            
        settings = sublime.load_settings("Flyc/FC_FileManagement.sublime-settings")
        mappings = settings.get("regex_syntax_mappings", [])
        
        # mappings 格式: [{"pattern": "\\.config$", "syntax": "Packages/JSON/JSON.sublime-syntax"}]
        for mapping in mappings:
            pattern = mapping.get("pattern")
            syntax = mapping.get("syntax")
            if pattern and syntax:
                if re.search(pattern, file_name):
                    view.set_syntax_file(syntax)
                    break
