# Packages/User/Flyc/editor_cmds.py (或者是你現有的 py 檔)
import sublime
import sublime_plugin

class ChangeTabSizeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # 取得當前檔案的 Tab 寬度，預設給 4
        current_size = self.view.settings().get("tab_size", 4)
        
        # 呼叫視窗底部的輸入面板
        # 參數依序為：提示文字、預設文字、輸入完成的 callback、輸入改變的 callback、取消的 callback
        self.view.window().show_input_panel(
            "請輸入 Tab 寬度 (空白數量):", 
            str(current_size), 
            self.on_done, 
            None, 
            None
        )

    def on_done(self, user_input):
        try:
            # 嘗試將輸入的字串轉換為整數
            new_size = int(user_input)
            
            if new_size > 0:
                # 設定新的 tab_size
                self.view.settings().set("tab_size", new_size)
                sublime.status_message(f"成功！已將 Tab 寬度設為: {new_size}")
            else:
                sublime.status_message("設定失敗：Tab 寬度必須大於 0")
                
        except ValueError:
            # 如果輸入的不是數字 (例如不小心打了英文字母)
            sublime.status_message("設定失敗：請輸入有效的數字")