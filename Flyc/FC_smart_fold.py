import sublime
import sublime_plugin

# VERSION: 1.1.2 - Integrated Onion Fold
class FcSmartFoldCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print("\n[FC Smart Fold] 🚀 v1.1.2 Triggered")
        
        view = self.view
        # 1. 紀錄初始折疊狀態 (紀錄每個區域的起始與結束位置)
        old_folds = set((f.a, f.b) for f in view.folded_regions())
        original_sel = list(view.sel())

        # --- 步驟 1: 讓 Sublime 內建邏輯先跑 ---
        view.run_command("move_to", {"to": "eol"})
        view.run_command("expand_selection", {"to": "brackets"})
        view.run_command("fold")
        
        # 2. 取得新的折疊狀態
        new_folds = set((f.a, f.b) for f in view.folded_regions())
        
        # 如果折疊的集合發生了任何變化 (增加、合併、範圍變大)
        if new_folds != old_folds:
            print("[FC] 折疊範圍已更新，停止。")
            return

        # --- 步驟 2: 如果內建邏輯完全沒反應，代表需要手動向上尋找 ---
        print("[FC] 內建邏輯無反應，啟動智慧父層搜尋...")
        view.sel().clear()
        view.sel().add_all(original_sel)
        
        self.fold_one_parent_only(view)

    def fold_one_parent_only(self, view):
        sel = view.sel()[0]
        cur_row, _ = view.rowcol(sel.b)
        
        line_text = view.substr(view.line(sel.b))
        cur_indent = self.get_indent(line_text)
        
        for row in range(cur_row - 1, -1, -1):
            pt = view.text_point(row, 0)
            r_region = view.line(pt)
            r_text = view.substr(r_region)
            
            if not r_text.strip(): continue
            
            r_indent = self.get_indent(r_text)
            
            if r_indent < cur_indent:
                # 找到第一個縮排更淺的行
                if view.is_folded(r_region):
                    print(f"[FC] 行 {row + 1} 已折疊，繼續往上找...")
                    cur_indent = r_indent
                    continue
                
                # 執行折疊並立即停止
                print(f"[FC] 智慧搜尋找到父層行 {row + 1}，執行折疊")
                view.sel().clear()
                view.sel().add(sublime.Region(pt))
                view.run_command("fold")
                
                # 將游標移到行末 (EOL)
                view.run_command("move_to", {"to": "eol"})
                return 

    def get_indent(self, text):
        if not text.strip(): return 9999
        tab_size = self.view.settings().get("tab_size", 4)
        expanded = text.expandtabs(tab_size)
        return len(expanded) - len(expanded.lstrip())
