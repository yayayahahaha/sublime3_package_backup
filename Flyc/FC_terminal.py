import os
import subprocess
import threading
import sublime
import sublime_plugin

# ==========================================
# 核心基底類別 (負責處理所有底層邏輯)
# ==========================================
class BaseTerminalCommand(sublime_plugin.WindowCommand):
    
    def execute_terminal(self, cmd_template):
        # 1. 抓取當前變數
        variables = self.window.extract_variables()
        
        # 優先順序：當前檔案所在資料夾 > 專案第一個資料夾
        cwd = variables.get("file_path")
        if not cwd and variables.get("folder"):
            cwd = variables.get("folder")
        
        # 如果還是沒有 (例如沒開檔案也沒開資料夾)，就報錯
        if not cwd:
            sublime.error_message("無法確定執行目錄。")
            return
        
        # 2. 處理字串替換
        cmd_string = sublime.expand_variables(cmd_template, variables)

        # 3. 建立並開啟面板
        panel_name = "fc_terminal"
        panel = self.window.create_output_panel(panel_name)
        panel.settings().set("word_wrap", True)
        self.window.run_command("show_panel", {"panel": "output." + panel_name})
        
        # 4. 處理 Mac 的環境變數 PATH
        env = os.environ.copy()
        # 確保常用路徑都在裡面，避免找不到 git 或 node
        env["PATH"] = "/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:" + env.get("PATH", "")

        # 5. 啟動背景執行緒
        threading.Thread(target=self._run_process, args=(cmd_string, cwd, env, panel)).start()

    def _run_process(self, cmd_string, cwd, env, panel):
        try:
            # 在執行指令前，先切換到 git root (如果有的話)
            # 這樣 git diff --staged 才能抓到整個專案的檔案
            final_cmd = f"cd \"{cwd}\" && if git rev-parse --show-toplevel > /dev/null 2>&1; then cd $(git rev-parse --show-toplevel); fi; {cmd_string}"

            process = subprocess.Popen(
                ["bash", "-c", final_cmd], 
                cwd=cwd, 
                env=env,
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                text=True, 
                bufsize=1
            )

            for line in process.stdout:
                sublime.set_timeout(lambda l=line: self._append_to_panel(panel, l), 0)

            process.wait()
            sublime.set_timeout(lambda: self._append_to_panel(panel, f"\n[執行結束，代碼: {process.returncode}]\n"), 0)

        except Exception as e:
            sublime.set_timeout(lambda: self._append_to_panel(panel, f"\n[發生錯誤: {str(e)}]\n"), 0)

    def _append_to_panel(self, panel, text):
        panel.run_command("append", {"characters": text, "scroll_to_end": True})


# ==========================================
# 你自訂的具體指令 (繼承基底，只覆寫字串)
# ==========================================

# 1. 執行 Stylelint
class RunStylelintFixCommand(BaseTerminalCommand):
    def run(self):
        # 只要在這裡定義好你的字串，然後丟給父類別執行即可
        # 也可以用 ${project_path} 確保在專案根目錄執行相對路徑腳本
        cmd = "echo '[FC]執行 stylelint fix: ${file}'; npx stylelint \"${file}\" --fix"
        self.execute_terminal(cmd)

# 2. 執行 ESLint (範例)
class RunEslintFixCommand(BaseTerminalCommand):
    def run(self):
        cmd = "echo '[FC]執行 ESLint fix: ${file}'; npx eslint \"${file}\" --fix"
        self.execute_terminal(cmd)

# 3. 同時執行 ESLint 與 Stylelint (僅針對 Git Staged 檔案)
class RunStagedLintCommand(BaseTerminalCommand):
    def run(self):
        cmd = """
        JS_FILES=$(git diff --staged --diff-filter=d --name-only -- "*.vue" "*.js" "*.ts" "*.jsx" "*.tsx");
        if [ -n "$JS_FILES" ]; then
            echo "[FC] 正在修復已暫存的 JS/Vue 檔案...";
            npx eslint --fix $JS_FILES;
            if [ $? -ne 0 ]; then
                echo "\\n[❌] ESLint 執行失敗，請檢查配置或程式碼錯誤。";
                exit 1;
            fi
        else
            echo "[FC] 無發現已暫存的 JS/Vue 檔案";
        fi;

        CSS_FILES=$(git diff --staged --diff-filter=d --name-only -- "*.vue" "*.less" "*.css" "*.scss");
        if [ -n "$CSS_FILES" ]; then
            echo "[FC] 正在修復已暫存的 Style 檔案...";
            npx stylelint --fix $CSS_FILES;
            if [ $? -ne 0 ]; then
                echo "\\n[❌] Stylelint 執行失敗，請檢查配置或程式碼錯誤。";
                exit 1;
            fi
        else
            echo "[FC] 無發現已暫存的 Style 檔案";
        fi;
        echo "\\n[✅] Staged 檔案修復處理完成";
        """
        self.execute_terminal(cmd)