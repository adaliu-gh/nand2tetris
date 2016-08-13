commandtypes = {'label': 'C_LABEL', 'goto': 'C_GOTO', 'if-goto': 'C_IFGOTO',
                    'function': 'C_FUNCTION', 'push': 'C_PUSH', 'pop': "C_POP",'return':"C_RETURN",'call':'C_CALL'}
arithmetics = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'not', 'or']


def commandType(command):
    if command in arithmetics:
        ctype= "C_ARITHMETIC"
    else:
        ctype= commandtypes[command]
    return ctype


def arg1(line, type):
    if type == "C_ARITHMETIC" or type=='C_RETURN':
        return line.split()[0]
    else:
        return line.split()[1]


def arg2(line):
    return int(line.split()[2])


def removeun(line):
    line = line.replace('\n', '')
    if '/' in line:
        line = line.split('/')[0]
    line = line.strip()
    return line
