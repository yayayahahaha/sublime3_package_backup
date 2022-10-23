# Sublime Text Package Backup

### Main Flow

1. install sublime text
   https://www.sublimetext.com/

2. use `cmd + shift + p` open panel then type `Install Package Control` to install [`Package Control`](https://packagecontrol.io/)

3. use `cmd + shift + p` open panel again then type `Preferences: Browse Packages` to open file system of packages' located place
   document: https://www.sublimetext.com/docs/3/revert.html

4. close sublime text

5. in file system, remove `User` folder

6. git clone `{this_repository_name}`

7. rename folder `{this_repository_name}` to `User`

8. cd `{this_repository_name}` folder

9. restart sublime text

10. happy hunting

### Other Info

顯示執行的 `command`, 可以用於顯示客製化 `key_bindings`

> 但依舊無法顯示所有套件的行為

```py
# 開啟console panel: ctrl + `
sublime.log_commands(True)
```
