from JackTokenizer import *
from SymbolTable import *
from VMwriter import *

def compileClass(tokens, tokennumber, filename, length):
    variables = []
    classes = []
    types = []
    subroutines = []

    ifin = [0]
    whin = [0]
    ops = {'+':'add', '-':'sub', '/':'call Math.divide 2', '*':'call Math.multiply 2', '&':'and', '<':'lt', '|':'or', '>':'gt', '=':'eq'}
    returntype=['']
    classname=os.path.basename(filename).split('.')[0]
    vmConstructor(filename)
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
            id=tokens[tokennumber[0]]
            tablestatus=kindOf(tokens[tokennumber[0]])
            if tablestatus=='NONE':
                m = tokennumber[0]
                while tokens[m-1]==',':
                    m = m - 2
                type = tokens[m-1]

                m = tokennumber[0]
                while True:
                    if tokens[m-2]=='(':
                        kind = 'argument'
                        break
                    elif tokens[m - 2]=='field':
                        kind = 'field'
                        break
                    elif tokens[m - 2]=='variable':
                        kind = 'variable'
                        break
                    elif tokens[m - 2]=='static':
                        kind = 'static'
                        break
                    else:
                        m = m - 1

                defineid(id, type, kind)
        inc()
        return

    def compileSubroutineName():
        subroutinename='%s.%s'%(classname,tokens[tokennumber[0]])
        if subroutinename not in subroutines:
            subroutines.append(subroutinename)
        inc()
        return subroutinename

    def compileClassVarDec():

        kind = tokens[tokennumber[0]]
        inc()
        compileType()
        while tokens[tokennumber[0]]!=';':
            if tokens[tokennumber[0]] == ',':
                inc()
            else:
                compileVarName()
        inc()
        return

    def compileStatements():

        def compileExpression():

            def compileExpressionList():
                argnumber=0
                while not (tokennumber[0]==length or tokens[tokennumber[0]]==')'):
                    if tokens[tokennumber[0]] == ',':
                        inc()
                    else:
                        compileExpression()
                        argnumber+=1
                return argnumber

            def compileSubroutineCall():
                argnumber=0
                if tokens[tokennumber[0] + 1] == '.':
                    prefix=tokens[tokennumber[0]]
                    inc()
                    inc()
                    if kindOf(prefix)!='NONE':
                        writePush(kindOf(prefix),indexOf(prefix))
                        writePop('pointer', 0)
                        writePush('pointer', 0)
                        subroutinename='%s.%s'%(typeOf(prefix),tokens[tokennumber[0]])
                        argnumber=1
                    else:
                        subroutinename=prefix+'.'+tokens[tokennumber[0]]
                    inc()
                else:
                    subroutinename=compileSubroutineName()
                inc()
                argnumber=argnumber+compileExpressionList()
                inc()
                writeCall(subroutinename, argnumber)
                return


            def compileTerm():
                if tokens[tokennumber[0]] in ['-', '~']:
                    inc()
                    compileTerm()
                    if tokens[tokennumber[0]] =='-':
                        writeArithmetic('neg')
                    else:
                        writeArithmetic('not')
                elif tokens[tokennumber[0]] == '(':
                    inc()
                    compileExpression()
                    inc()
                elif tokens[tokennumber[0] + 1] in ['(', '.']:
                    compileSubroutineCall()
                elif kindOf(tokens[tokennumber[0]])!='NONE':
                    kind=kindOf(tokens[tokennumber[0]])
                    type=typeOf(tokens[tokennumber[0]])
                    index=indexOf(tokens[tokennumber[0]])
                    if type=='Array':
                        writePush(kind, index)
                        inc()
                        inc()
                        compileExpression()
                        writeArithmetic('add')
                        writePop('pointer',1)
                        writePush('that', 0)
                        inc()
                    else:
                        writePush(kind, index)
                        inc()
                elif tokenType(tokens[tokennumber[0]])=='stringConstant':
                    nofstring=len(tokens[tokennumber[0]])-2
                    writePush('constant', nofstring)
                    writeCall('String.new', 1)
                    for s in tokens[tokennumber[0]][1:-1]:
                        writePush('constant', ord(s))
                        writeCall('String.appendChar', 2)
                    inc()
                elif tokenType(tokens[tokennumber[0]])=='integerConstant':
                    writePush('constant', int(tokens[tokennumber[0]]))
                    inc()
                elif tokens[tokennumber[0]] == '}':
                    return
                elif tokens[tokennumber[0]] in ['true','false','null','this']:
                    if tokens[tokennumber[0]]=='true':
                        writePush('constant', 1)
                        writeArithmetic('neg')
                    elif tokens[tokennumber[0]]=='false':
                        writePush('constant', 0)
                    elif tokens[tokennumber[0]]=='null':
                        writePush('constant', 0)
                    else:
                        writePush('pointer', 0)
                    inc()

                return

            compileTerm()
            while tokens[tokennumber[0]] in ops:
                op=tokens[tokennumber[0]]
                inc()
                compileTerm()
                writecommon(ops[op])

            return

        def compileExpressionList():
                argnumber=0
                while not (tokennumber[0]==length or tokens[tokennumber[0]] ==')' ):
                    if tokens[tokennumber[0]] == ',':
                        inc()
                    else:
                        compileExpression()
                        argnumber+=1
                return argnumber

        def compileSubroutineCall():
            argnumber=0
            if tokens[tokennumber[0] + 1] == '.':
                prefix=tokens[tokennumber[0]]
                inc()
                inc()
                if kindOf(prefix)!='NONE':
                    writePush(kindOf(prefix),indexOf(prefix))
                    writePop('pointer', 0)
                    writePush('pointer', 0)
                    subroutinename='%s.%s'%(typeOf(prefix),tokens[tokennumber[0]])
                    argnumber=1
                else:
                    subroutinename=prefix+'.'+tokens[tokennumber[0]]
                inc()
            else:
                subroutinename=compileSubroutineName()
            inc()
            argnumber=argnumber+compileExpressionList()
            inc()
            writeCall(subroutinename, argnumber)
            return


        def compileLet():
            inc()
            lethead=tokennumber[0]
            while tokens[tokennumber[0]]!='=':
                inc()
            inc()
            compileExpression()
            tokennumber[0]=lethead
            id=tokens[lethead]
            kind=kindOf(id)
            index=indexOf(id)
            type=typeOf(id)
            if type=='Array':
                writePush(kind, index)
                inc()
                inc()
                compileExpression()
                writeArithmetic('add')
                writePop('pointer',1)
                writePop('that', 0)
                return
            elif type=='field':
                writePop('this', index)
            else:
                writePop(kind, index)
            while tokens[tokennumber[0]]!=';':
                inc()
            inc()
            return

        def compileIf():
            inc()
            inc()
            compileExpression()
            inc()
            inc()
            writeIf('if%i'%ifin[0])
            writeGoto('else%i'%ifin[0])
            writeLabel('if%i'%ifin[0])
            compileStatements()
            inc()
            writeGoto('endif%i'%ifin[0])
            writeLabel('else%i'%ifin[0])
            if tokens[tokennumber[0]] == 'else':
                inc()
                inc()
                compileStatements()
                inc()
            writeLabel('endif%i'%ifin[0])
            ifin[0]+=1
            return

        def compileWhile():
            writeLabel('whilehead%i'%whin[0])
            inc()
            inc()
            compileExpression()
            writeIf('whilebody%i'%whin[0])
            writeGoto('endwhile%i'%whin[0])
            inc()
            inc()
            writeLabel('whilebody%i'%whin[0])
            compileStatements()
            inc()
            writeGoto('whilehead%i'%whin[0])
            writeLabel('endwhile%i'%whin[0])
            whin[0]+=1
            return

        def compileDo():
            inc()
            compileSubroutineCall()
            inc()
            return

        def compileReturn():
            inc()
            if tokens[tokennumber[0]] != ';':
                compileExpression()
            inc()
            if returntype[0]=='void':
                writePush('constant', 0)
            writeReturn()
            return

        while True:

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
            else:
                break
        return

    def compileVarDec():
        inc()
        compileType()
        localnumber=0
        while tokens[tokennumber[0]]!=';':
            if tokens[tokennumber[0]] == ',':
                inc()
            else:
                compileVarName()
                localnumber+=1
        inc()
        return localnumber

    def calculatelocal():
        inc()
        localnumber=0
        while tokens[tokennumber[0]]=='var':
            localnumber+=compileVarDec()
        return localnumber

    def compileSubroutineBody():
        inc()
        while tokens[tokennumber[0]]=='var':
            compileVarDec()
        while tokens[tokennumber[0]]!='}':
            compileStatements()
        inc()
        return


    def compileParameterList():
        argnumber=0
        while tokens[tokennumber[0]]!=')':
            if tokens[tokennumber[0]] == ',':
                inc()
            else:
                compileType()
                compileVarName()
                argnumber+=1
        return argnumber

    def compileSubroutineDec():

        # if tokens[tokennumber[0]]=='method':
        #     argnumber=1
        # else:
        #     argnumber=0
        inc()
        returntype[0]=tokens[tokennumber[0]]
        # if tokens[tokennumber[0]]!='void':

        #     compileType()


        inc()
        name=compileSubroutineName()
        inc()
        bodybegin=tokennumber[0]
        argnumber=calculatelocal()
        tokennumber[0]=bodybegin
        inc()
        writeFunction(name, argnumber)
        if name.endswith('.new'):
            size=varCount('field')
            writeFunction('Memory.alloc', size)
            writePop('pointer', 0)
            writePush('pointer', 0)
        compileSubroutineBody()

        return

    inc()
    compileClassName()
    inc()
    while tokens[tokennumber[0]]!='}':
        if tokens[tokennumber[0]] in ['static', 'field']:
            compileClassVarDec()
        # elif tokens[tokennumber[0]] in ['constructor', 'function', 'method', 'void']:
        #     compileSubroutineDec()
        else:
            compileSubroutineDec()
    return
