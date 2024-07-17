const path = require('path')
const fs = require('fs')
require('colors') // 改 nodejs console 的顏色
// https://blog.logrocket.com/using-console-colors-node-js/#colors-js

const disabledFolderName = 'disabled-snippets'
const disabledFolderPath = path.resolve(__dirname, disabledFolderName)
const disabledMark = '___DISABLED___'
const snippetFolderName = 'sublime-snippet'
const snippetFolderPath = path.resolve(__dirname, snippetFolderName)

const snippetEndRegexp = /\.sublime-snippet$/
const snippetDisbledEndRegexp = new RegExp(`\.sublime-snippet${disabledMark}$`)

start()
function start() {
  if (!isDir(disabledFolderPath)) {
    console.log(`${disabledFolderName} 需為一個資料夾!`.red)
    return
  }

  // make snippets disabled part
  const disabledFiles = readFilesRecursively(disabledFolderPath)
    .filter(fileName => snippetEndRegexp.test(fileName))
    .map(fileName => path.resolve(disabledFolderPath, fileName))

  disabledFiles.forEach(filePath =>
    fs.renameSync(filePath, `${filePath}${disabledMark}`)
  )
  console.log(`一共 disabled 了 ${disabledFiles.length} 個檔案`)

  const snippetFiles = readFilesRecursively(snippetFolderPath)
    .filter(fileName => snippetDisbledEndRegexp.test(fileName))
    .map(fileName => path.resolve(snippetFolderPath, fileName))
  snippetFiles.forEach(filePath =>
    fs.renameSync(filePath, filePath.replace(disabledMark, ''))
  )
  console.log(`一共 enable 了 ${snippetFiles.length} 個檔案`)
}

function readFilesRecursively(pathStr, list = []) {
  fs.readdirSync(pathStr).forEach(name => {
    const fullPath = path.join(pathStr, name)
    isDir(fullPath) ? readFilesRecursively(fullPath, list) : list.push(fullPath)
  })
  return list
}
function isDir(path) {
  return fs.lstatSync(path).isDirectory()
}
