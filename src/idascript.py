##################################################################################################
# Python module for IDAPython scripts executed via idascript.
#
# Copied from the original idascript utility, with minor changes: http://www.hexblog.com/?p=128
#
##################################################################################################

import os
import sys
import tempfile
import idc
import idaapi
import re

import traceback

__idascript_active__ = False

def exit(code=0):
    global __idascript_active__
    if __idascript_active__:
        idc.qexit(code)

class ToFileStdOut(object):
    def __init__(self, outfile):
        self.outfile = open(outfile, 'w')

    def write(self, text):
        self.outfile.write(text)

    def flush(self):
        self.outfile.flush()

    def isatty(self):
        return False

    def __del__(self):
        self.outfile.close()

def loadAllPythonPlugins():
    plugins_dir = idaapi.idadir('plugins')
    # print("idascript: loading all .py plugins in %s" % plugins_dir)
    files = [f for f in os.listdir(plugins_dir) if re.match(r'.*\.py', f)]
    for path in files:
        idaapi.load_plugin(path)

if len(idc.ARGV) > 1 and idc.ARGV[1] == '__idascript_active__':
    __idascript_active__ = True
    idc.ARGV.pop(1)
    outfile= idc.ARGV.pop(1)

    # Redirect stdout and stderr to the output file
    sys.stdout = sys.stderr = ToFileStdOut(outfile)
    # Make the normal sys.argv and sys.exit function properly
    sys.argv = idc.ARGV
    sys.exit = idc.qexit

    try:
        loadAllPythonPlugins()
    except Exception as e:
        traceback.print_exc()
        exit(1)

    # Wait for IDA's auto analysis to finish
    idaapi.auto_wait()

