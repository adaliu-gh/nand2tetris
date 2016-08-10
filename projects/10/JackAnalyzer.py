from CompilationEngine import *
from JackTokenizer import *
import os
import sys

tokens = []


def jackanalyzer(jackfile):
    basename = os.path.basename(jackfile).split('.')[0]
    outfilename = os.path.join(dirname, '%s.xml' % basename)
    with open(jackfile) as jack:
        tokens = []
        tokenizer(jack, tokens)
    xml = open(outfilename, 'w')
    tokennumber = [0]
    compileClass(tokens, tokennumber, xml, len(tokens))
    xml.close()
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
