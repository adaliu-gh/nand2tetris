classtable = {'static': {}, 'field': {}}
methodtable = {'var': {}, 'arg': {}}
symboltable = [classtable, methodtable]


def startSubroutine():
    methodtable = {}
    return


def startNewTable():
    classtable['static'] = {}
    classtable['field'] = {}
    return


def define(name, type, kind):
    index = varCount(kind)
    if kind in ['static', 'field']:
        classtable[kind][name] = [type, index]
    else:
        methodtable[kind][name] = [type, index]


def varCount(kind):
    for i in symboltable:
        if kind in i:
            return len(i[kind])


def kindOf(name):
    for i in symboltable:
        for j in i:
            if name in i[j]:
                return j
    else:
        return 'NONE'


def typeOf(name):
    for i in symboltable:
        for j in i:
            if name in i[j]:
                return i[j][name][0]


def indexOf(name):
    for i in symboltable:
        for j in i:
            if name in i[j]:
                return i[j][name][1]
