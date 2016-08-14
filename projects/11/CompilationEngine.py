from JackTokenizer import *
from SymbolTable import *
from VMwriter import *
def compileClass(tokens, tokennumber, filename, length):
    variables = []
    classes = []
    types = []
    subroutines = []
    methods = []
    ifin = [0]
    whin = [0]
    ops = {'+': 'add', '-': 'sub', '/': 'call Math.divide 2',
           '*': 'call Math.multiply 2', '&': 'and', '<': 'lt', '|': 'or', '>': 'gt', '=': 'eq'}
    returntype = ['']
    classname = os.path.basename(filename).split('.')[0]
    vmConstructor(filename)
    startNewTable()
    def inc():
        tokennumber[0] += 1
        return
    def compileClassName():
        if tokens[tokennumber[0]] not in classes:
            classes.append(tokens[tokennumber[0]])
        inc()
        return
    def compileType():
        if tokens[tokennumber[0]] not in types:
            types.append(tokens[tokennumber[0]])
        if tokens[tokennumber[0]] in ['int', 'char', 'boolean']:
            inc()
        else:
            compileClassName()
        return
    def compileVarName():
        if (tokens[tokennumber[0]] not in classes) or (tokens[tokennumber[0]] not in subroutines):
            id = tokens[tokennumber[0]]
            tablestatus = kindOf(tokens[tokennumber[0]])
            if tablestatus == 'NONE':
                m = tokennumber[0]
                while tokens[m - 1] == ',':
                    m = m - 2
                type = tokens[m - 1]
                m = tokennumber[0]
                while True:
                    if tokens[m - 2] == '(':
                        kind = 'argument'
                        break
                    elif tokens[m - 2] == 'field':
                        kind = 'field'
                        break
                    elif tokens[m - 2] == 'var':
                        kind = 'local'
                        break
                    elif tokens[m - 2] == 'static':
                        kind = 'static'
                        break
                    else:
                        m = m - 1
                defineid(id, type, kind)
        inc()
        return
    def compileSubroutineName():
        subroutinename = '%s.%s' % (classname, tokens[tokennumber[0]])
        if subroutinename not in subroutines:
            subroutines.append(subroutinename)
        inc()
        return subroutinename
    def compileClassVarDec():
        kind = tokens[tokennumber[0]]
        inc()
        compileType()
        while tokens[tokennumber[0]] != ';':
            if tokens[tokennumber[0]] == ',':
                inc()
            else:
                compileVarName()
        inc()
        return
    def compileStatements():
        def compileExpression():
            def compileExpressionList():
                argnumber = 0
                while not (tokennumber[0] == length or tokens[tokennumber[0]] == ')'):
                    if tokens[tokennumber[0]] == ',':
                        inc()
                    else:
                        compileExpression()
                        argnumber += 1
                return argnumber
            def compileSubroutineCall():
                argnumber = 0
                k = 0
                if tokens[tokennumber[0] + 1] == '.':
                    prefix = tokens[tokennumber[0]]
                    inc()
                    inc()
                    kind = kindOf(prefix)
                    index = indexOf(prefix)
                    if kind != 'NONE':
                        if kind == 'field':
                            writePush('this', index)
                        else:
                            writePush(kind, index)
                        subroutinename = '%s.%s' % (
                            typeOf(prefix), tokens[tokennumber[0]])
                        argnumber = 1
                    else:
                        subroutinename = prefix + '.' + tokens[tokennumber[0]]
                    inc()
                else:
                    subroutinename = compileSubroutineName()
                    argnumber=1
                    writePush('pointer', 0)
                inc()
                argnumber = argnumber + compileExpressionList()
                inc()
                print(subroutinename)
                writeCall(subroutinename, argnumber)
                return
            def compileTerm():
                if tokens[tokennumber[0]] in ['-', '~']:
                    symbol = tokens[tokennumber[0]]
                    inc()
                    compileTerm()
                    if symbol == '-':
                        writeArithmetic('neg')
                    else:
                        writeArithmetic('not')
                elif tokens[tokennumber[0]] == '(':
                    inc()
                    compileExpression()
                    inc()
                elif tokens[tokennumber[0] + 1] in ['(', '.']:
                    compileSubroutineCall()
                elif kindOf(tokens[tokennumber[0]]) != 'NONE':
                    kind = kindOf(tokens[tokennumber[0]])
                    type = typeOf(tokens[tokennumber[0]])
                    index = indexOf(tokens[tokennumber[0]])
                    if tokens[tokennumber[0] + 1] == '[':
                        writePush(kind, index)
                        if tokens[tokennumber[0]] == 'ball':
                            print(23)
                        inc()
                        inc()
                        compileExpression()
                        writeArithmetic('add')
                        writePop('pointer', 1)
                        writePush('that', 0)
                        inc()
                    elif kind == 'field':
                        writePush('this', index)
                        inc()
                    else:
                        writePush(kind, index)
                        if tokens[tokennumber[0]] == 'ball':
                            print(23)
                        inc()
                elif tokenType(tokens[tokennumber[0]]) == 'stringConstant':
                    nofstring = len(tokens[tokennumber[0]]) - 2
                    writePush('constant', nofstring)
                    writeCall('String.new', 1)
                    for s in tokens[tokennumber[0]][1:-1]:
                        writePush('constant', ord(s))
                        writeCall('String.appendChar', 2)
                    inc()
                elif tokenType(tokens[tokennumber[0]]) == 'integerConstant':
                    writePush('constant', int(tokens[tokennumber[0]]))
                    inc()
                elif tokens[tokennumber[0]] == '}':
                    return
                elif tokens[tokennumber[0]] in ['true', 'false', 'null', 'this']:
                    if tokens[tokennumber[0]] == 'true':
                        writePush('constant', 1)
                        writeArithmetic('neg')
                    elif tokens[tokennumber[0]] == 'false':
                        writePush('constant', 0)
                    elif tokens[tokennumber[0]] == 'null':
                        writePush('constant', 0)
                    else:
                        writePush('pointer', 0)
                    inc()
                return
            compileTerm()
            while tokens[tokennumber[0]] in ops:
                op = tokens[tokennumber[0]]
                inc()
                compileTerm()
                writecommon(ops[op])
            return
        def compileExpressionList():
            argnumber = 0
            while not (tokennumber[0] == length or tokens[tokennumber[0]] == ')'):
                if tokens[tokennumber[0]] == ',':
                    inc()
                else:
                    compileExpression()
                    argnumber += 1
            return argnumber
        def compileSubroutineCall():
            argnumber = 0
            if tokens[tokennumber[0] + 1] == '.':
                prefix = tokens[tokennumber[0]]
                inc()
                inc()
                kind = kindOf(prefix)
                index = indexOf(prefix)
                if kindOf(prefix) != 'NONE':
                    if kind == 'field':
                        writePush('this', index)
                    else:
                        writePush(kind, index)
                    subroutinename = '%s.%s' % (
                        typeOf(prefix), tokens[tokennumber[0]])
                    argnumber = 1
                else:
                    subroutinename = prefix + '.' + tokens[tokennumber[0]]
                inc()
            else:
                subroutinename = compileSubroutineName()
                argnumber=1
                writePush('pointer',0)
            inc()
            argnumber = argnumber + compileExpressionList()
            inc()
            print(subroutinename)
            writeCall(subroutinename, argnumber)
            return
        def compileLet():
            inc()
            lethead = tokennumber[0]
            while tokens[tokennumber[0]] != '=':
                inc()
            inc()
            compileExpression()
            letbody = tokennumber[0]
            tokennumber[0] = lethead
            id = tokens[lethead]
            kind = kindOf(id)
            index = indexOf(id)
            type = typeOf(id)
            if tokens[tokennumber[0] + 1] == '[':
                writePush(kind, index)
                inc()
                inc()
                compileExpression()
                writeArithmetic('add')
                writePop('pointer', 1)
                writePop('that', 0)
            elif kind == 'field':
                writePop('this', index)
            else:
                writePop(kind, index)
            while tokens[tokennumber[0]] != ';':
                inc()
            assert tokens[tokennumber[0]] == ';'
            inc()
            return
        def compileIf():
            inc()
            inc()
            compileExpression()
            inc()
            inc()
            iflabel = ifin[0]
            writeIf('if%i' % iflabel)
            writeGoto('else%i' % iflabel)
            writeLabel('if%i' % iflabel)
            ifin[0] += 1
            compileStatements()
            inc()
            if tokens[tokennumber[0]] == 'else':
                writeGoto('endif%i'%iflabel)
                writeLabel('else%i' % iflabel)
                inc()
                inc()
                compileStatements()
                inc()
                writeLabel('endif%i'%iflabel)
            else:
                writeLabel('else%i' % iflabel)
            return
        def compileWhile():
            whlabel = whin[0]
            writeLabel('whilehead%i' % whlabel)
            inc()
            inc()
            compileExpression()
            writeArithmetic('not')
            writeIf('endwhile%i' % whlabel)
            inc()
            inc()
            whin[0] += 1
            compileStatements()
            inc()
            writeGoto('whilehead%i' % whlabel)
            writeLabel('endwhile%i' % whlabel)
            return
        def compileDo():
            inc()
            compileSubroutineCall()
            writePop('temp', 0)
            inc()
            return
        def compileReturn():
            inc()
            if tokens[tokennumber[0]] != ';':
                compileExpression()
            inc()
            if returntype[0] == 'void':
                writePush('constant', 0)
            writeReturn()
            return
        while tokens[tokennumber[0]] != '}':
            if tokens[tokennumber[0]] == 'let':
                compileLet()
            elif tokens[tokennumber[0]] == 'if':
                compileIf()
            elif tokens[tokennumber[0]] == 'while':
                compileWhile()
            elif tokens[tokennumber[0]] == 'do':
                compileDo()
            elif tokens[tokennumber[0]] == 'return':
                compileReturn()
        assert tokens[tokennumber[0]] == '}'
        return
    def compileVarDec():
        inc()
        compileType()
        localnumber = 0
        while tokens[tokennumber[0]] != ';':
            if tokens[tokennumber[0]] == ',':
                inc()
            else:
                compileVarName()
                localnumber += 1
        inc()
        return localnumber
    def calculatelocal():
        inc()
        inc()
        localnumber = 0
        while tokens[tokennumber[0]] == 'var':
            localnumber += compileVarDec()
        return localnumber
    def compileSubroutineBody():
        while tokens[tokennumber[0]] != '}':
            compileStatements()
        inc()
        return
    def compileParameterList():
        argnumber = 0
        while tokens[tokennumber[0]] != ')':
            if tokens[tokennumber[0]] == ',':
                inc()
            else:
                compileType()
                compileVarName()
                argnumber += 1
        return argnumber
    def compileSubroutineDec():
        startSubroutine()
        functiontype = tokens[tokennumber[0]]
        inc()
        returntype[0] = tokens[tokennumber[0]]
        inc()
        name = compileSubroutineName()
        inc()
        bodybegin = tokennumber[0]
        if functiontype=='method':
            defineid('method', 'method', 'argument')
        compileParameterList()
        argnumber = calculatelocal()
        writeFunction(name, argnumber)
        if functiontype == 'method':
            writePush('argument', 0)
            writePop('pointer', 0)
            methods.append(name)
        if name.endswith('.new'):
            size = varCount('field')
            if size == 0:
                size = 1
            writePush('constant', size)
            writeCall('Memory.alloc', 1)
            writePop('pointer', 0)
        compileSubroutineBody()
        return
    inc()
    compileClassName()
    inc()
    while tokens[tokennumber[0]] != '}':
        if tokens[tokennumber[0]] in ['static', 'field']:
            compileClassVarDec()
        else:
            compileSubroutineDec()
    return