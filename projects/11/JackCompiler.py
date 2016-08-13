from CompilationEngine import *
from JackTokenizer import *
from VMwriter import *
import SymbolTable
import os
import sys

tokens = []

syntax = []

classtable = {}
methodtable = {}
symboltable = [classtable, methodtable]


def jackanalyzer(jackfile):
    print('%s'%jackfile)
    basename = os.path.basename(jackfile).split('.')[0]
    outfilename = os.path.join(dirname, '%s.vm' % basename)
    with open(jackfile) as jack:
        global tokens
        tokenizer(jack, tokens)
    # for i in tokens:
    #     print(i)
    tokennumber = [0]
    print('get tokens successfully!')
    compileClass(tokens, tokennumber, outfilename, len(tokens))
    print('compile successfully!!!')
    tokens = []
    print('%s' % outfilename)
    print('DONE!!!\n\n')

if len(sys.argv) < 2:
    print('Usage: [file/path]')
    sys.exit()

abspath = os.path.abspath(sys.argv[1])
tokenfolder = os.path.abspath('myxmls')

if os.path.isdir(sys.argv[1]):
    for foldername, subfolders, filenames in os.walk(abspath):
        for filename in filenames:
            if filename.endswith('.jack'):
                dirname = os.path.join(
                    tokenfolder, os.path.basename(foldername))
                if not os.path.exists(dirname):
                    os.mkdir(dirname)
                filepath = os.path.join(os.path.abspath(foldername), filename)
                jackanalyzer(filepath)
else:
    dirname = tokenfolder
    jackanalyzer(abspath)
