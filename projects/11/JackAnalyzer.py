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
    basename = os.path.basename(jackfile).split('.')[0]
    outfilename = os.path.join(dirname, '%s.xml' % basename)
    with open(jackfile) as jack:
        global tokens
        tokenizer(jack, tokens)
	tn=len(tokens)
    xml = open(outfilename, 'w')
    tokennumber = [0]
    compileClass(tokens, tokennumber, syntax, len(tokens))
    tokens = []
    n = len(syntax)
    SymbolTable.startNewTable()
    for i in range(n):
        if syntax[i] == '<subroutineDec>\n':
            SymbolTable.startSubroutine()
        xml.write('%s\n'%str(syntax[i]))
        if 'identifier' in syntax[i]:
            id = syntax[i][1]
            tablestatus = SymbolTable.kindOf(id)
            xml.write('%s\n' % tablestatus)
            if tablestatus == 'NONE':                
				if id in subroutines:
                    category = 'subroutine'
				elif id in classes:
                    category = 'class'
                else:
					m = i
                    while ',' in syntax[m - 1]:
                        m = m - 2
                    type = syntax[m - 1][1]
                    
                    m = i
                    while True:
                        if 'parameter' in syntax[m - 2]:
                            kind = 'arg'
                            break
                        elif 'field' in syntax[m - 2]:
                            kind = 'field'
                            break
                        elif 'var' in syntax[m - 2]:
                            kind = 'var'
                            break
                        elif 'static' in syntax[m - 2]:
                            kind = 'static'
                            break
                        else:
                            m = m - 1
                    

                    category = type

                    print('%s %s %s' % (id, type, kind))

                    SymbolTable.define(id, type, kind)
                xml.write('category: %s\n' % category)
		
		
	for i in range(n):
	
	
	
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
