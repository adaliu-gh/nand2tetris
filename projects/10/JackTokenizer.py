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
        return 'keyword'
    elif token in SYMBOLES:
        return 'symbol'
    elif token.isdigit():
        return 'integerConstant'
    elif token.startswith('"') and token.endswith('"'):
        return 'stringConstant'
    else:
        return 'identifier'


def keyword(token):
    return token


def symbol(token):
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

writetokens = {'keyword': keyword, 'identifier': identifier,
               'symbol': symbol, 'integerConstant': intVal, 'stringConstant': stringVal}


def writetoken(token, f):
    t = tokenType(token)
    f.write('<%s> %s </%s>\n' % (t, writetokens[t](token), t))


def tokenizer(jackfile, tokens):

    while True:
        line = jackfile.readline()
        if not line:
            break
        if '/*' in line:
            while not '*/' in line:
                line = jackfile.readline()
            continue
        line = purifier(line)
        if not line:
            continue
        temp = gettokens(line)
        for i in temp:
            tokens.append(i)
