import sys
import os

KEYWORDS = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char',
            'boolean', 'void', 'true', 'false', 'null', 'this', 'that', 'let', 'do', 'if', 'else', 'while', 'return']
SYMBOLES = ['{', '}', '(', ')', '[', ']', '.', ',', ';',
            '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']


def gettokens(line):
    tokens = []
    length = len(line)
    i = 0
    while i < length:
        if line[i] in SYMBOLES:
            tokens.append(line[i])

        elif line[i] == '"':
            string = '"'
            while True:
                i += 1
                string += line[i]
                if line[i] == '"':
                    break
            tokens.append(string)

        elif line[i] != ' ':
            string = ''
            while i < length:
                if line[i] == ' ' or line[i] in SYMBOLES or line[i] == '"':
                    break
                string += line[i]
                i += 1
            tokens.append(string)
            continue
        i += 1
    return tokens


def tokenType(token):
    if token in KEYWORDS:
        return 'KEYWORD'
    elif token in SYMBOLES:
        return 'SYMBOL'
    elif token.isdigit():
        return 'INI_CONST'
    elif token.startswith('"') and token.endswith('"'):
        return 'STRING_CONST'
    else:
        return 'IDENTIFIER'


def keyword(token):
    return token


def symbol(token, line):
    if token == '<':
        token = '&lt;'
    elif token == '>':
        token = '&gt;'
    elif token == '&':
        token = '&amp;'
    return token


def identifier(token):
    return token


def intVal(token):
    return int(token)


def stringVal(token):
    return token.replace('"', '')


def purifier(line):
    if '//' in line:
        line = line.split('//')[0]
    line = line.strip()
    return line


def tokenizer(jackfile):
    print('beginning tokenizing %s ...' % jackfile)
    basename = os.path.basename(jackfile).split('.')[0]
    outfilename = os.path.join(dirname, '%sT.xml' % basename)
    print('output to %s......' % outfilename)
    with open(jackfile) as jack:
        xml = open(outfilename, 'w')
        xml.write('<tokens>\n')
        while True:
            line = jack.readline()
            if not line:
                break
            if '/*' in line:
                while not '*/' in line:
                    line = jack.readline()
                continue
            line = purifier(line)
            if not line:
                continue
            tokens = gettokens(line)
            for i in tokens:
                t = tokenType(i)
                if t == 'KEYWORD':
                    xml.write('\t<keyword> %s </keyword>\n' % keyword(i))
                elif t == 'SYMBOL':
                    xml.write('\t<symbol> %s </symbol>\n' % symbol(i, line))
                elif t == 'INI_CONST':
                    xml.write(
                        '\t<integerConstant> %i </integerConstant>\n' % intVal(i))
                elif t == 'STRING_CONST':
                    xml.write(
                        '\t<stringConstant> %s </stringConstant>\n' % stringVal(i))
                elif t == 'IDENTIFIER':
                    xml.write('\t<identifier> %s </identifier>\n' %
                              identifier(i))
    xml.write('</tokens>')
    xml.close()
    print('DONE!')


if len(sys.argv) < 2:
    print('Usage: [file/path]')
    sys.exit()

abspath = os.path.abspath(sys.argv[1])
tokenfolder = os.path.abspath('testtokenizer')

if os.path.isdir(sys.argv[1]):
    for foldername, subfolders, filenames in os.walk(abspath):
        for filename in filenames:
            if filename.endswith('.jack'):
                dirname = os.path.join(
                    tokenfolder, os.path.basename(foldername))
                if not os.path.exists(dirname):
                    os.mkdir(dirname)
                filepath = os.path.join(os.path.abspath(foldername), filename)
                tokenizer(filepath)
else:
    tokenizer(abspath)
