#!/usr/bin/env python

import os
import sys
import stat
from pathlib import Path
TARGET = 'idascript'
IDA_INSTALL_PATH = ''

try:
    IDA_INSTALL_PATH = Path(sys.argv[1])
except:
    pass

if not os.path.isdir(IDA_INSTALL_PATH):
    print("Absolute path to your IDA install directory: ",)
    IDA_INSTALL_PATH = Path(sys.stdin.readline().strip())
    print("")

if sys.platform == 'win32':
    BIN_INSTALL_PATH = os.path.join(IDA_INSTALL_PATH.as_posix(), TARGET)
else:
    try:
        BIN_INSTALL_PATH = os.path.join(os.getenv("PATH").split(':')[0], TARGET)
    except:
        BIN_INSTALL_PATH = '/usr/local/bin/' + TARGET

files = [(os.path.join('src', TARGET), BIN_INSTALL_PATH), (os.path.join('src', TARGET + '.py'), os.path.join(IDA_INSTALL_PATH.as_posix(), 'python', TARGET + '.py'))]

replacements = [('%%IDA_INSTALL_PATH%%', IDA_INSTALL_PATH.as_posix())]

print("Installing idascript to '%s'" % BIN_INSTALL_PATH)
print("Installing support files to '%s'" % IDA_INSTALL_PATH.as_posix())

for (srcname, dstname) in files:
    data = open(srcname).read()

    for (replaceme, withme) in replacements:
        data = data.replace(replaceme, withme)

    open(dstname, 'w').write(data)
    os.chmod(dstname, (stat.S_IROTH | stat.S_IXOTH | stat.S_IRWXU))

