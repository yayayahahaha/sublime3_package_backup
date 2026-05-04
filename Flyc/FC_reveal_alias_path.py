import os
import sublime
import sublime_plugin

# 1. 處理 @/ 與相對路徑 (./ 或 ../) 的跳轉
class RevealAliasPathCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sel = self.view.sel()[0]
        if sel.empty():
            return
        
        text = self.view.substr(sel).strip()
        if not text:
            return

        if text.startswith("@/"):
            text = "src/" + text[2:]
        elif text.startswith("./") or text.startswith("../"):
            current_file = self.view.file_name()
            if current_file:
                current_dir = os.path.dirname(current_file)
                abs_path = os.path.normpath(os.path.join(current_dir, text))
                
                folders = self.view.window().folders()
                for folder in folders:
                    if abs_path.startswith(folder):
                        text = os.path.relpath(abs_path, folder).replace('\\', '/')
                        break
                else:
                    text = abs_path

        self.view.window().run_command("show_overlay", {"overlay": "goto", "text": text})


# 2. 複製當前檔案名稱 (修正版：雙重抓取)
class CopyActiveFileNameCommand(sublime_plugin.WindowCommand):
    def run(self):
        # 優先使用 active_view()，這對文字檔最準確
        view = self.window.active_view()
        file_path = view.file_name() if view else None
        
        # 如果抓不到 (例如圖片檔)，再退回使用變數抓取
        if not file_path:
            variables = self.window.extract_variables()
            file_path = variables.get("file")
            
        if file_path:
            file_name = os.path.basename(file_path)
            sublime.set_clipboard(file_name)
            sublime.status_message("Copied File Name: " + file_name)
            print("[Debug - Copy Name] 成功複製:", file_name)
        else:
            sublime.status_message("Copy Failed: No active file")
            print("[Debug - Copy Name] 失敗: 找不到檔案路徑")


# 3. 複製當前檔案相對路徑 (修正版：強制路徑正規化)
class CopyActiveRelativePathCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        file_path = view.file_name() if view else None
        
        if not file_path:
            variables = self.window.extract_variables()
            file_path = variables.get("file")
            
        if file_path:
            rel_path = file_path
            folders = self.window.folders()
            
            # 透過 realpath 消除 Mac 系統可能的 symlink 或大小寫字串差異
            real_file_path = os.path.realpath(file_path)
            
            for folder in folders:
                real_folder = os.path.realpath(folder)
                
                # 使用正規化後的路徑進行比對
                if real_file_path.startswith(real_folder):
                    rel_path = os.path.relpath(real_file_path, real_folder).replace('\\', '/')
                    break
                    
            sublime.set_clipboard(rel_path)
            sublime.status_message("Copied Relative Path: " + rel_path)
            print("[Debug - Copy RelPath] 成功複製:", rel_path)
        else:
            sublime.status_message("Copy Failed: No active file")
            print("[Debug - Copy RelPath] 失敗: 找不到檔案路徑")


# 4. 像瀏覽器一樣跳到最後一個 Tab
class JumpToLastTabCommand(sublime_plugin.WindowCommand):
    def run(self):
        current_group = self.window.active_group()
        views = self.window.views_in_group(current_group)
        if views:
            self.window.focus_view(views[-1])


# 5. 複製當前檔案並開在新的分割面板
class CloneToNewPaneCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.run_command("clone_file")
        self.window.run_command("new_pane")