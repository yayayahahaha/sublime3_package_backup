# Sublime Text 3 Package Backup

1. install sublime text3
https://www.sublimetext.com/3

2. install package control
https://packagecontrol.io/
```python
import urllib.request,os,hashlib; h = '6f4c264a24d933ce70df5dedcf1dcaee' + 'ebe013ee18cced0ef93d5f746d80ef60'; pf = 'Package Control.sublime-package'; ipp = sublime.installed_packages_path(); urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) ); by = urllib.request.urlopen( 'http://packagecontrol.io/' + pf.replace(' ', '%20')).read(); dh = hashlib.sha256(by).hexdigest(); print('Error validating download (got %s instead of %s), please try manual install' % (dh, h)) if dh != h else open(os.path.join( ipp, pf), 'wb' ).write(by)
```

3. go to
Windows: `C:\Users\<userName>\AppData\Roaming\Sublime Text 3\Packages\User`
or
Mac: `~/Library/ApplicationSupport/Sublime Text 3/Packages/User`
comments: https://www.sublimetext.com/docs/3/revert.html

4. remove all file in it

5. git init

6. git remote add origin <this_repostory>

7. git fetch

8. git checkout maseter

9. restart sublime text 3

10. happy hunting
