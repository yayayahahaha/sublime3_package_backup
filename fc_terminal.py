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
        # 1. 抓取當前變數 (處理 ${file}, ${folder} 等)
        variables = self.window.extract_variables()
        cwd = variables.get("file_path", variables.get("folder"))
        
        # 2. 將模板字串替換成真實路徑
        cmd_string = sublime.expand_variables(cmd_template, variables)

        # 3. 建立並開啟底部的 Output Panel
        panel_name = "my_custom_terminal"
        panel = self.window.create_output_panel(panel_name)
        panel.settings().set("word_wrap", True)
        self.window.run_command("show_panel", {"panel": "output." + panel_name})
        
        # 4. 處理 Mac 的環境變數 PATH
        env = os.environ.copy()
        env["PATH"] = "/usr/local/bin:/opt/homebrew/bin:" + env.get("PATH", "")

        # 5. 啟動背景執行緒
        threading.Thread(target=self._run_process, args=(cmd_string, cwd, env, panel)).start()

    def _run_process(self, cmd_string, cwd, env, panel):
        try:
            # 統一交給 bash 執行，這樣才能支援 echo 和 && 或 ; 這類語法
            process = subprocess.Popen(
                ["bash", "-c", cmd_string], 
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