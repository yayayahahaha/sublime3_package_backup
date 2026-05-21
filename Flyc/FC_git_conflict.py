import sublime
import sublime_plugin
import re

class FcFoldGitConflictsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        # 取得所有行
        lines = view.lines(sublime.Region(0, view.size()))
        conflict_marker_lines = []
        
        # 偵測 4 個或以上重複字元開頭的行： <, |, =, >
        marker_pattern = re.compile(r'^(<{4,}|\|{4,}|={4,}|>{4,})')
        
        for line_region in lines:
            text = view.substr(line_region)
            if marker_pattern.match(text):
                conflict_marker_lines.append(line_region)
        
        # 遍歷標記行進行折疊
        for i in range(len(conflict_marker_lines) - 1):
            curr_marker = conflict_marker_lines[i]
            next_marker = conflict_marker_lines[i+1]
            
            curr_text = view.substr(curr_marker)
            
            # 如果目前是開始標記 (<<<<) 或中間標記 (||||, ====)
            if curr_text.startswith("<<<<") or \
               curr_text.startswith("||||") or \
               curr_text.startswith("===="):
                
                # 取得當前標記行的下一行開頭位置
                # 我們從當前行的「換行符號之後」開始折疊
                fold_start = curr_marker.end() + 1
                # 折疊到下一個標記行的「前一個字元」(即下一個標記行上方的換行符號)
                fold_end = next_marker.begin() - 1
                
                if fold_end > fold_start:
                    fold_region = sublime.Region(fold_start, fold_end)
                    view.fold(fold_region)
                    
        sublime.status_message("Git conflicts content folded.")
